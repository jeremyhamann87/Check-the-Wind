#!/usr/bin/env python3
"""
Fetches a rolling ~1 hour window of MRMS composite reflectivity (observed)
frames, appends a raw HRRR forecast (Phase 3 — no blending yet, so expect
a visible "jump" where observed ends and forecast begins), and writes the
combined manifest.json the futurecast map page reads.

Only genuinely new observed frames get downloaded + decoded — anything
already rendered from a previous run is reused as-is, and anything that's
aged out of the window gets deleted. Run it directly:
python3 fetch_mrms.py
"""
import gzip
import json
import os
import shutil
import sys
import tempfile
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone

import requests
import xarray as xr

import config
from render import render_frame

REQUEST_TIMEOUT = 30
S3_NS = {"s3": "http://s3.amazonaws.com/doc/2006-03-01/"}


def _list_page(prefix, start_after=None, continuation_token=None):
    params = {"list-type": "2", "prefix": prefix}
    if start_after:
        params["start-after"] = start_after
    if continuation_token:
        params["continuation-token"] = continuation_token
    resp = requests.get(f"{config.MRMS_BUCKET_URL}/", params=params, timeout=REQUEST_TIMEOUT)
    resp.raise_for_status()
    root = ET.fromstring(resp.text)
    keys = [el.text for el in root.findall("s3:Contents/s3:Key", S3_NS)]
    truncated = (root.findtext("s3:IsTruncated", namespaces=S3_NS) or "").lower() == "true"
    token = root.findtext("s3:NextContinuationToken", namespaces=S3_NS)
    return keys, (token if truncated and token else None)


def list_keys_since(cutoff_dt):
    """All MRMS keys with an observation time >= cutoff_dt (UTC), spanning
    a UTC-day boundary if the window happens to cross midnight."""
    today = datetime.now(timezone.utc).date()
    d = cutoff_dt.date()
    date_strs = []
    while d <= today:
        date_strs.append(d.strftime("%Y%m%d"))
        d += timedelta(days=1)

    all_keys = []
    for date_str in date_strs:
        prefix = f"{config.MRMS_PREFIX}/{date_str}/"
        is_cutoff_day = date_str == cutoff_dt.strftime("%Y%m%d")
        # A small margin before the cutoff hour, so we never miss a file
        # that landed just before the exact cutoff minute.
        start_after = (
            f"{prefix}MRMS_{config.MRMS_PRODUCT}_{date_str}-{max(cutoff_dt.hour - 1, 0):02d}0000"
            if is_cutoff_day else None
        )
        token = None
        while True:
            keys, token = _list_page(prefix, start_after=start_after, continuation_token=token)
            all_keys += keys
            if not token:
                break

    result = []
    for key in all_keys:
        try:
            ts = frame_timestamp_from_key(key)
        except ValueError:
            continue
        if ts >= cutoff_dt:
            result.append(key)
    return sorted(result)


def download_grib(key, dest_dir):
    url = f"{config.MRMS_BUCKET_URL}/{key}"
    gz_path = os.path.join(dest_dir, "frame.grib2.gz")
    grib_path = os.path.join(dest_dir, "frame.grib2")

    with requests.get(url, stream=True, timeout=REQUEST_TIMEOUT) as resp:
        resp.raise_for_status()
        with open(gz_path, "wb") as f:
            shutil.copyfileobj(resp.raw, f)

    with gzip.open(gz_path, "rb") as f_in, open(grib_path, "wb") as f_out:
        shutil.copyfileobj(f_in, f_out)

    return grib_path


def frame_timestamp_from_key(key):
    """MRMS filenames encode the observation time as ..._YYYYMMDD-HHMMSS."""
    stamp = key.rsplit("_", 1)[-1].replace(".grib2.gz", "")
    return datetime.strptime(stamp, "%Y%m%d-%H%M%S").replace(tzinfo=timezone.utc)


def frame_id_for(obs_time):
    return obs_time.strftime("mrms_%Y%m%dT%H%M%SZ")


def existing_frame_ids():
    if not os.path.isdir(config.FRAMES_DIR):
        return set()
    return {
        os.path.splitext(f)[0]
        for f in os.listdir(config.FRAMES_DIR)
        if f.endswith(".png")
    }


def prune_old_frames(keep_ids):
    if not os.path.isdir(config.FRAMES_DIR):
        return
    removed = 0
    for f in os.listdir(config.FRAMES_DIR):
        if not f.endswith(".png"):
            continue
        if os.path.splitext(f)[0] not in keep_ids:
            os.remove(os.path.join(config.FRAMES_DIR, f))
            removed += 1
    if removed:
        print(f"Pruned {removed} frame(s) outside the observed window")


def decode_grib(key):
    """Download + decode one MRMS key, returning (values, lat, lon)."""
    with tempfile.TemporaryDirectory() as tmp:
        grib_path = download_grib(key, tmp)
        ds = xr.open_dataset(grib_path, engine="cfgrib")
        var_name = list(ds.data_vars)[0]
        return ds[var_name].values, ds["latitude"].values, ds["longitude"].values


def render_one(key, obs_time):
    frame_id = frame_id_for(obs_time)
    png_path = os.path.join(config.FRAMES_DIR, frame_id + ".png")
    values, lat, lon = decode_grib(key)
    render_frame(values, lat, lon, png_path, scale=config.RENDER_SCALE)
    return frame_id


def fetch_recent_raw_frames(keys, n):
    """Download + decode the raw dBZ arrays for the most recent `n` of
    `keys` (chronological). Used by the nowcast step, which needs actual
    values (not just the already-rendered PNGs) to estimate motion and
    extrapolate. Returns [(time, values), ...] oldest to newest."""
    recent_keys = keys[-n:]
    out = []
    for key in recent_keys:
        obs_time = frame_timestamp_from_key(key)
        values, _lat, _lon = decode_grib(key)
        out.append((obs_time, values))
    return out


def build_observed_frames():
    cutoff = datetime.now(timezone.utc) - timedelta(minutes=config.OBSERVED_WINDOW_MINUTES)
    print(f"Listing MRMS files since {cutoff.isoformat()}...")
    keys = list_keys_since(cutoff)
    if not keys:
        raise RuntimeError("No MRMS files found in the observed window")
    print(f"  found {len(keys)} file(s) in the last {config.OBSERVED_WINDOW_MINUTES} min")

    have = existing_frame_ids()
    frames = []
    new_count = 0
    for key in keys:
        obs_time = frame_timestamp_from_key(key)
        frame_id = frame_id_for(obs_time)

        if frame_id not in have:
            print(f"  rendering {frame_id}...")
            render_one(key, obs_time)
            new_count += 1

        frames.append({
            "time": obs_time.isoformat(),
            "url": f"frames/{frame_id}.png",
            "bounds": config.MRMS_BOUNDS,
            "kind": "observed",
        })

    print(f"Rendered {new_count} new observed frame(s), reused {len(frames) - new_count} existing")
    return frames, keys


def build_nowcaster(keys, n=6):
    """Decode the most recent `n` observed frames and wrap them into a
    Nowcaster ready to extrapolate + blend with HRRR. Returns None (rather
    than raising) if that's not possible — the forecast then just falls
    back to raw HRRR, which is still a working forecast, only without the
    smoothed transition."""
    if len(keys) < 2:
        print("WARNING: not enough recent observed frames for a nowcast", file=sys.stderr)
        return None
    print(f"Building optical-flow nowcast from the last {min(n, len(keys))} observed frame(s)...")
    timed_values = fetch_recent_raw_frames(keys, n)
    import nowcast
    return nowcast.Nowcaster(timed_values)


def main():
    os.makedirs(config.FRAMES_DIR, exist_ok=True)

    observed_frames, observed_keys = build_observed_frames()

    forecast_frames = []
    hrrr_run_time = None
    try:
        import fetch_hrrr

        nowcaster = build_nowcaster(observed_keys)
        blend_fn = nowcaster.blend_with_hrrr if nowcaster else None
        if blend_fn is None:
            print("Fetching raw HRRR forecast frames (no nowcast blend available)...")
        else:
            print("Fetching HRRR forecast frames + blending with the nowcast...")

        forecast_frames, hrrr_run_time = fetch_hrrr.build_forecast_frames(blend_fn=blend_fn)

        # HRRR only updates hourly and lags behind real time by a bit, so
        # the run available right now can be older than our most recent
        # observed data — drop any "forecast" frame whose valid time isn't
        # actually after what we've already observed, or the timeline
        # would show forecast frames chronologically before the boundary.
        if observed_frames:
            latest_observed_time = observed_frames[-1]["time"]
            before = len(forecast_frames)
            forecast_frames = [f for f in forecast_frames if f["time"] > latest_observed_time]
            dropped = before - len(forecast_frames)
            if dropped:
                print(f"  dropped {dropped} forecast frame(s) already covered by observed data")

        print(f"  got {len(forecast_frames)} forecast frame(s)")
    except Exception as err:  # noqa: BLE001 - forecast is additive; don't break observed-only mode
        print(f"WARNING: HRRR forecast unavailable ({err}) — writing observed-only manifest", file=sys.stderr)

    all_frames = observed_frames + forecast_frames
    keep_ids = {os.path.splitext(os.path.basename(f["url"]))[0] for f in all_frames}
    prune_old_frames(keep_ids)

    manifest = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "product": config.MRMS_PRODUCT,
        "observed_window_minutes": config.OBSERVED_WINDOW_MINUTES,
        "hrrr_run": hrrr_run_time.isoformat() if hrrr_run_time else None,
        "frames": all_frames,
    }
    with open(config.MANIFEST_PATH, "w") as f:
        json.dump(manifest, f, indent=2)
    print(f"Wrote {config.MANIFEST_PATH} ({len(observed_frames)} observed + {len(forecast_frames)} forecast)")


if __name__ == "__main__":
    try:
        main()
    except Exception as err:  # noqa: BLE001 - top-level script, want a clean message
        print(f"ERROR: {err}", file=sys.stderr)
        sys.exit(1)
    else:
        # main() has already written the manifest and flushed everything to
        # disk by this point. On some Linux CI runners, one of the native
        # GRIB/CV extensions (eccodes/cfgrib, opencv) segfaults during
        # normal Python interpreter shutdown (exit code 139) even though
        # all real work already completed successfully. os._exit() skips
        # that teardown path (atexit handlers, GC, module destructors)
        # entirely, so a shutdown-time crash in a dependency can't turn a
        # successful run into a failed CI job.
        sys.stdout.flush()
        sys.stderr.flush()
        os._exit(0)

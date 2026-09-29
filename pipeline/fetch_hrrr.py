"""
Phase 3: fetch raw HRRR composite reflectivity (REFC) forecast frames and
reproject them onto the same plain lat/lon grid the MRMS observed frames
use, so the frontend can treat every frame — observed or forecast — as
just another entry in the same list with the same bounds.

HRRR ships on a Lambert Conformal Conic grid (a flat projected grid, not
plain lat/lon), so each frame gets resampled onto config.MRMS_BOUNDS at
MRMS's own resolution before rendering. This is "raw" HRRR — no blending
or bias-correction yet (that's Phase 4), so don't expect the transition
from the last observed frame to the first forecast frame to look perfectly
seamless. It's expected to visibly "jump" a bit at that boundary for now.
"""
import os
import warnings
from datetime import datetime, timedelta, timezone

import numpy as np
import pyproj
import xarray as xr

import config
from render import render_frame, NO_DATA

# HRRR's CONUS grid definition (read once from a sample GRIB file's
# metadata via eccodes — see README for how these were derived). Fixed
# across every HRRR run, so safe to hardcode rather than re-read it from
# every single file.
HRRR_NX, HRRR_NY = 1799, 1059
HRRR_DX = HRRR_DY = 3000.0  # meters
HRRR_LAT1, HRRR_LON1 = 21.138123, 237.280472 - 360  # first grid point (SW corner)
HRRR_LCC_PROJ4 = "+proj=lcc +lat_1=38.5 +lat_2=38.5 +lat_0=38.5 +lon_0=-97.5 +R=6371229 +units=m +no_defs"

# Forecast horizon: sub-hourly (15 min) steps for hour 1, then hourly out
# to hour 3, matching the "~3-hour forecast" goal and using sub-hourly
# output where HRRR actually provides it.
SUBHOURLY_MINUTES = [15, 30, 45, 60]
HOURLY_STEPS = [2, 3]


def _lcc_transformer():
    return pyproj.Transformer.from_crs("EPSG:4326", HRRR_LCC_PROJ4, always_xy=True)


def _target_grid():
    """The same lat/lon grid config.MRMS_BOUNDS + native MRMS resolution
    describes, so forecast frames line up pixel-for-pixel with observed
    ones (and, come Phase 4, are trivial to blend together)."""
    (south, west), (north, east) = config.MRMS_BOUNDS
    lat = np.linspace(north, south, 3500)  # descending, matches MRMS row order
    lon = np.linspace(west, east, 7000)    # ascending, matches MRMS column order
    return lat, lon


def reproject_to_latlon(values, native_lat, native_lon, target_lat, target_lon):
    """Resample a Lambert-Conformal HRRR field onto a plain lat/lon grid.

    Rather than interpolating from scratch (expensive for ~2M source
    points), this projects the *target* grid's lat/lon into HRRR's own
    flat x/y space, where a nearest-neighbor lookup is just integer index
    math — HRRR's native grid is regular in that space by construction.
    """
    transformer = _lcc_transformer()
    origin_x, origin_y = transformer.transform(HRRR_LON1, HRRR_LAT1)

    lon_grid, lat_grid = np.meshgrid(target_lon, target_lat)
    x, y = transformer.transform(lon_grid, lat_grid)

    col = np.round((x - origin_x) / HRRR_DX).astype(np.int64)
    row = np.round((y - origin_y) / HRRR_DY).astype(np.int64)

    in_bounds = (col >= 0) & (col < HRRR_NX) & (row >= 0) & (row < HRRR_NY)
    out = np.full(lon_grid.shape, NO_DATA, dtype=np.float32)
    out[in_bounds] = values[row[in_bounds], col[in_bounds]]
    return out


def _herbie_frame(run_time, fxx, product, search):
    # Imported lazily — Herbie prints a one-time config banner on first
    # import, which is noisy if this module is imported but unused.
    from herbie import Herbie

    # Herbie wants a naive timestamp string (it treats everything as UTC
    # internally) — handing it a tz-aware datetime makes it choke comparing
    # aware vs. naive timestamps somewhere in its own run-time lookup.
    run_time_str = run_time.strftime("%Y-%m-%d %H:%M")

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        H = Herbie(run_time_str, model="hrrr", product=product, fxx=fxx)
        if not H.grib:
            return None
        path = H.download(search, verbose=False)
        ds = xr.open_dataset(
            str(path), engine="cfgrib",
            backend_kwargs={"filter_by_keys": {"shortName": "refc"}},
        )
    return ds


def latest_hrrr_run():
    """HRRR ships hourly; walk backward from now to find the most recent
    run that's actually been posted yet (the current hour's run usually
    isn't available for a while after the top of the hour)."""
    now = datetime.now(timezone.utc)
    for hours_back in range(0, 6):
        run_time = (now - timedelta(hours=hours_back)).replace(minute=0, second=0, microsecond=0)
        ds = _herbie_frame(run_time, 0, "sfc", ":REFC:")
        if ds is not None:
            return run_time
    raise RuntimeError("No HRRR run found in the last 6 hours")


def build_forecast_frames(blend_fn=None):
    """blend_fn(hrrr_array, valid_time) -> final_array, if given, is
    applied to each reprojected HRRR field before rendering — this is
    where Phase 4's nowcast blending hooks in. When it's given, frames are
    always re-rendered (the blend depends on the latest observed data, so
    a cached PNG from an earlier run is stale); with no blend_fn, frames
    are reused by filename the same way observed ones are, since raw HRRR
    only actually changes when a new model run is posted."""
    os.makedirs(config.FRAMES_DIR, exist_ok=True)
    run_time = latest_hrrr_run()
    print(f"Using HRRR run {run_time.isoformat()}")

    target_lat, target_lon = _target_grid()

    steps = []  # (fxx, product, search_pattern, valid_time)
    for minutes in SUBHOURLY_MINUTES:
        valid_time = run_time + timedelta(minutes=minutes)
        steps.append((1, "subh", f":REFC:.*{minutes} min fcst", valid_time))
    for fxx in HOURLY_STEPS:
        valid_time = run_time + timedelta(hours=fxx)
        steps.append((fxx, "sfc", ":REFC:", valid_time))

    frames = []
    for fxx, product, search, valid_time in steps:
        frame_id = valid_time.strftime("hrrr_%Y%m%dT%H%M%SZ")
        png_path = os.path.join(config.FRAMES_DIR, frame_id + ".png")

        if blend_fn is None and os.path.exists(png_path):
            print(f"  reusing {frame_id}")
        else:
            verb = "blending" if blend_fn else "fetching + reprojecting"
            print(f"  {verb} {frame_id} (F{fxx:02d} {product})...")
            ds = _herbie_frame(run_time, fxx, product, search)
            if ds is None:
                print(f"    not available yet, skipping")
                continue
            values = ds["refc"].values
            native_lat = ds["latitude"].values
            native_lon = ds["longitude"].values
            reprojected = reproject_to_latlon(values, native_lat, native_lon, target_lat, target_lon)
            final = blend_fn(reprojected, valid_time) if blend_fn else reprojected
            render_frame(final, target_lat, target_lon, png_path, scale=config.RENDER_SCALE)

        frames.append({
            "time": valid_time.isoformat(),
            "url": f"frames/{frame_id}.png",
            "bounds": config.MRMS_BOUNDS,
            "kind": "forecast",
        })

    return frames, run_time

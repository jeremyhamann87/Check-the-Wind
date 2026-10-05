# Futurecast pipeline

Fetches weather radar + forecast data and renders it into plain PNG frames
+ a `manifest.json` that the site's `/futurecast/index.html` map page
reads. No server-side code runs when someone visits the page — it's just
static files, same as the rest of the site.

## What it does today (Phases 1–3)

Running `python3 fetch_mrms.py` does the whole pipeline in one go:

1. Keeps a rolling ~1 hour window of **observed** MRMS composite
   reflectivity frames (only fetching genuinely new ones each run, and
   pruning anything that's aged out).
2. Fetches the latest **HRRR forecast** run and appends ~6 hours of
   **forecast** frames after the observed ones — sub-hourly (15 min) steps
   for the first hour, then hourly for hours 2–6.
3. Writes one combined `futurecast/manifest.json` covering both, each
   frame tagged `"kind": "observed"` or `"kind": "forecast"`.

Coverage is CONUS-wide on purpose, not cropped to one city — the map page
pans to wherever the visitor last searched on the main site (same
`localStorage` key `checkTheWind.lastLocation` that `windline.html` uses),
so one shared set of frames works for every visitor everywhere in the
country.

**The forecast is "raw" HRRR for now — no blending yet (that's Phase 4).**
Expect a visible jump in the animation right where observed ends and
forecast begins, since nothing is smoothing that transition. The map page
marks that boundary clearly (a "now" tick on the timeline, two-tone
observed/forecast track, and an Observed/Forecast label) precisely because
that jump is expected at this stage, not a bug.

## Running it locally

```bash
cd pipeline
python3 -m venv .venv        # first time only
source .venv/bin/activate
pip install -r requirements.txt   # first time only
python3 fetch_mrms.py
```

Then open `futurecast/index.html` through a local web server (opening it
as a `file://` URL won't let it fetch `manifest.json`) — e.g. from the
project root:

```bash
python3 -m http.server 8935
```

and visit `http://localhost:8935/futurecast/index.html`.

## How the observed side works

1. **Find new files.** MRMS ships a new CONUS composite reflectivity file
   to NOAA's public (no-login) AWS bucket roughly every 2 minutes, at
   `s3://noaa-mrms-pds/CONUS/MergedReflectivityQCComposite_00.50/<date>/`.
   Rather than listing an entire day's worth of files (~700 of them), the
   script asks S3 to start listing from ~1 hour ago.
2. **Download + decompress.** Files are gzip-compressed GRIB2.
3. **Decode.** `cfgrib` (via `xarray`) reads the GRIB2 file into a 2D grid
   of dBZ (reflectivity) values, 3500 x 7000 pixels at ~1km resolution.
   `-999` marks "no data".
4. **Colorize + write the PNG.** `render.py` maps dBZ values to the
   standard 15-color NWS reflectivity scale. Anything below 5 dBZ — most
   of the grid, on most days — stays fully transparent.

## How the forecast side works

1. **Find the latest HRRR run.** [Herbie](https://herbie.readthedocs.io/)
   handles locating + downloading the right GRIB2 file from NOAA's public
   HRRR bucket, walking backward hour by hour until it finds a run that's
   actually been posted.
2. **Pull composite reflectivity (REFC).** The `subh` (sub-hourly) product
   has REFC at 15/30/45/60-minute steps within hour 1; the regular `sfc`
   product has it hourly after that.
3. **Reproject.** HRRR ships on a Lambert Conformal Conic grid (a flat
   projected grid — each point's lat/lon is computed, not evenly spaced),
   not MRMS's plain lat/lon grid. `fetch_hrrr.py` projects the *target*
   lat/lon grid (the same one MRMS frames use) into HRRR's native x/y
   space with `pyproj`, then does a nearest-neighbor lookup — fast (~1.5s/
   frame) because HRRR's own grid is regular in that space, so it's just
   integer index math once projected. The exact grid parameters (origin,
   spacing, projection) were read directly from a sample GRIB file's
   metadata via `eccodes`, not guessed from memory.
4. **Render the same way observed frames are** — same color table, same
   target grid/bounds, so every frame (observed or forecast) is
   interchangeable to the frontend.

## What's next

- **Phase 4:** blend a pySTEPS optical-flow nowcast (extrapolated from
  recent MRMS frames) with the raw HRRR forecast, weighted more toward
  extrapolation early and more toward HRRR by hours 2–3, so the jump at
  the observed/forecast boundary goes away.
- **Phase 5:** run this on a schedule (GitHub Actions is the leading
  candidate — free, no server to manage) and prune old frames.

## Dependencies

See `requirements.txt`.

- `cfgrib` decodes GRIB2 files (MRMS + HRRR) — it pulls in a bundled build
  of the ecCodes C library (`eccodeslib`), so there's nothing extra to
  install at the OS level.
- `herbie-data` finds and downloads the right HRRR GRIB2 file for a given
  run/forecast-hour without needing to hand-build NOAA bucket URLs.
- `pyproj` handles the Lambert Conformal → lat/lon reprojection for HRRR.

Herbie caches downloaded GRIB files under `~/data/hrrr/` by default (its
own cache directory, separate from this project) — that'll grow over time
and isn't cleaned up automatically yet.

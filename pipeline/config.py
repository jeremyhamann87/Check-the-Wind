"""
Futurecast pipeline configuration.

Coverage is CONUS-wide (not cropped to one place) because the site's map
pans to wherever the visitor searched — see index.html's saved-location
logic. Keeping one shared set of frames for the whole country means the
pipeline never has to know or care where anyone is looking.
"""
import os

# --- Paths -------------------------------------------------------------
PIPELINE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(PIPELINE_DIR)
OUTPUT_DIR = os.path.join(PROJECT_DIR, "futurecast")
FRAMES_DIR = os.path.join(OUTPUT_DIR, "frames")
MANIFEST_PATH = os.path.join(OUTPUT_DIR, "manifest.json")

# --- MRMS source ---------------------------------------------------------
# Public, unsigned NOAA Open Data bucket — no AWS credentials needed.
MRMS_BUCKET = "noaa-mrms-pds"
MRMS_BUCKET_URL = f"https://{MRMS_BUCKET}.s3.amazonaws.com"
MRMS_PRODUCT = "MergedReflectivityQCComposite_00.50"  # composite reflectivity, CONUS, 0.01deg
MRMS_PREFIX = f"CONUS/{MRMS_PRODUCT}"

# --- Frame retention -----------------------------------------------------
# Phase 2: keep a rolling window of observed frames instead of just the
# latest one, and prune anything older than the window on every run.
OBSERVED_WINDOW_MINUTES = 60

# --- Update cadence --------------------------------------------------
# How often the scheduled job runs — matches the cron schedule in
# .github/workflows/deploy.yml. 15 min rather than something more
# aggressive because GitHub Actions can delay very frequent cron triggers
# under load, and MRMS/HRRR data doesn't change fast enough to need less.
UPDATE_INTERVAL_MINUTES = 15

# --- MRMS grid bounds ------------------------------------------------
# The CONUS composite reflectivity grid is the same physical grid on every
# run (3500 x 7000 pixels, 0.01deg resolution) — these bounds don't change
# frame to frame, so there's no need to re-derive them for frames we've
# already rendered in a previous run.
# [[south, west], [north, east]]
MRMS_BOUNDS = [[20.005001, -129.995], [54.995, -60.005002]]

# --- Rendered image size -------------------------------------------------
# Full native MRMS resolution (~1km/pixel, 7000x3500px) — tried downsampling
# to cut file size, but it visibly blurred/blocked storm detail once the
# map was zoomed into a city, so sharpness wins here even though it means
# a bigger download (~1MB/frame, ~30MB for a full hour's loop).
RENDER_SCALE = 1.0

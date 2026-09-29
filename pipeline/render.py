"""
Turns a decoded reflectivity grid (dBZ values) into a transparent PNG using
the standard NWS reflectivity color table, plus the geographic bounds
Leaflet needs to place that PNG on the map.
"""
import numpy as np
from PIL import Image

# Missing/no-coverage sentinel MRMS uses in place of real dBZ values.
NO_DATA = -999.0

# Standard NWS reflectivity color table, in 5 dBZ steps. Anything below the
# first threshold (5 dBZ) is left fully transparent — that's the vast
# majority of the grid on any given day, which is also why the PNG
# compresses down small despite covering the whole country.
# (threshold_dBZ, (R, G, B))
COLOR_TABLE = [
    (5,  (0x63, 0xC8, 0xFF)),
    (10, (0x00, 0x90, 0xF0)),
    (15, (0x00, 0x50, 0xE0)),
    (20, (0x00, 0xFF, 0x00)),
    (25, (0x00, 0xC8, 0x00)),
    (30, (0x00, 0x90, 0x00)),
    (35, (0xFF, 0xFF, 0x00)),
    (40, (0xE8, 0xC0, 0x00)),
    (45, (0xFF, 0x90, 0x00)),
    (50, (0xFF, 0x00, 0x00)),
    (55, (0xD0, 0x00, 0x00)),
    (60, (0xA0, 0x00, 0x00)),
    (65, (0xFF, 0x00, 0xFF)),
    (70, (0xC0, 0x00, 0xC0)),
    (75, (0xFF, 0xFF, 0xFF)),
]


def dbz_to_rgba(values):
    """values: 2D float array of dBZ (with NO_DATA sentinels). Returns a
    (H, W, 4) uint8 RGBA array."""
    h, w = values.shape
    rgba = np.zeros((h, w, 4), dtype=np.uint8)

    valid = values != NO_DATA
    # Below the lowest color-table threshold (or missing): stays transparent.
    for threshold, color in COLOR_TABLE:
        band = valid & (values >= threshold)
        rgba[band, 0] = color[0]
        rgba[band, 1] = color[1]
        rgba[band, 2] = color[2]
        rgba[band, 3] = 255

    return rgba


def render_frame(values, lat, lon, out_path, scale=1.0):
    """Write `values` (2D dBZ array) to `out_path` as a PNG, and return the
    [[south, west], [north, east]] bounds Leaflet's L.imageOverlay expects.

    `lat` is assumed descending (north -> south, matching row order) and
    `lon` is assumed ascending in 0-360 degrees (matching column order) —
    that's the layout MRMS ships, and it maps directly onto image rows/
    columns with no flipping needed.

    `scale` downsamples the output image (e.g. 0.25 = a quarter of the
    native linear resolution, 1/16th the pixels). The native MRMS grid is
    ~1km resolution, which is far finer than anyone can actually see once
    the map is zoomed into a city — downsampling cuts file size a lot for
    a loss of detail that isn't visible at the zoom levels this map uses.
    """
    rgba = dbz_to_rgba(values)
    img = Image.fromarray(rgba, mode="RGBA")
    if scale != 1.0:
        # NEAREST, not a smoothing filter: the color table produces hard-
        # edged, mostly-transparent regions, and a smoothing resize (e.g.
        # LANCZOS) turns those crisp edges into large bands of unique
        # semi-transparent gradient pixels — which compresses far worse
        # despite having fewer total pixels (measured ~5x bigger than
        # NEAREST on the same frame). Blocky edges are also just what
        # radar mosaics conventionally look like at a coarser resolution.
        new_size = (max(1, round(img.width * scale)), max(1, round(img.height * scale)))
        img = img.resize(new_size, Image.NEAREST)
    img.save(out_path, optimize=True)

    def to_signed_lon(l):
        return l - 360 if l > 180 else l

    south, north = float(lat[-1]), float(lat[0])
    west, east = to_signed_lon(float(lon[0])), to_signed_lon(float(lon[-1]))
    return [[south, west], [north, east]]

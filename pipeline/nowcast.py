"""
Phase 4: a simple optical-flow extrapolation nowcast built from recent MRMS
frames, blended with the raw HRRR forecast (Phase 3) so the transition from
observed to forecast doesn't visibly jump — mostly the nowcast in the first
hour, shifting toward HRRR by hours 2-3.

This hand-rolls the same technique pysteps' extrapolation nowcast uses
(dense optical flow -> semi-Lagrangian advection) with OpenCV + scipy,
instead of the pysteps package itself: pysteps ships no prebuilt wheel, and
building it from source needs OpenMP support this machine's system clang
doesn't have. Functionally this is the same approach — track where the
precipitation is moving, then slide the most recent frame along that
motion to project it forward in time.
"""
import cv2
import numpy as np
from scipy.ndimage import map_coordinates

from render import NO_DATA

# MRMS's -999 "missing" sentinel would corrupt optical flow (looks like a
# sharp fake edge) if used directly — replace it with the same "clear sky"
# floor HRRR uses. Doesn't change how anything renders: both floors sit
# well under the 5 dBZ color-table threshold, so both stay transparent.
CLEAR_FLOOR = -10.0


def _clean(values):
    return np.where(values <= NO_DATA, CLEAR_FLOOR, values)


def _to_uint8(values):
    clipped = np.clip(values, 0, 75)
    return (clipped / 75.0 * 255).astype(np.uint8)


def estimate_motion(recent_values):
    """recent_values: list of 2D dBZ arrays, oldest to newest (needs >= 2).
    Returns (u, v): a dense motion field, in pixels per array, estimated
    between the two most recent frames via Farneback dense optical flow."""
    prev_img = _to_uint8(_clean(recent_values[-2]))
    next_img = _to_uint8(_clean(recent_values[-1]))
    flow = cv2.calcOpticalFlowFarneback(
        prev_img, next_img, None,
        pyr_scale=0.5, levels=3, winsize=25, iterations=3,
        poly_n=5, poly_sigma=1.2, flags=0,
    )
    return flow[..., 0], flow[..., 1]  # u = x/column motion, v = y/row motion


def extrapolate(latest_values, u, v, steps):
    """Advect `latest_values` forward by `steps` multiples of the (u, v)
    motion field, via semi-Lagrangian (backward) sampling: each output
    pixel is filled from wherever the motion field says its content came
    from `steps` intervals ago."""
    h, w = latest_values.shape
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    src_x = xx - u * steps
    src_y = yy - v * steps
    cleaned = _clean(latest_values)
    return map_coordinates(cleaned, [src_y, src_x], order=1, mode="constant", cval=CLEAR_FLOOR)


def weight_for_lead_minutes(minutes):
    """How much to trust the nowcast vs. HRRR at a given lead time: mostly
    nowcast early (0.9+ in the first hour), shifting toward HRRR by hours
    2-3 (down to 0.1 at 180 min) — a simple linear decay."""
    return max(0.1, 1.0 - 0.9 * min(minutes, 180) / 180.0)


def blend(nowcast_field, hrrr_field, weight):
    """Pixel-wise weighted average. Falls back to the nowcast alone
    wherever HRRR has no data for that pixel (its domain is smaller than
    the full render bounds, so this matters near the edges)."""
    hrrr_valid = hrrr_field != NO_DATA
    return np.where(hrrr_valid, weight * nowcast_field + (1 - weight) * hrrr_field, nowcast_field)


class Nowcaster:
    """Wraps a stack of recent observed frames into a ready-to-call
    extrapolator: `nowcaster.blend_with_hrrr(hrrr_array, valid_time)`."""

    def __init__(self, timed_values):
        """timed_values: [(datetime, 2D dBZ array), ...] oldest to newest,
        at least 2 entries, ideally more for a steadier motion estimate."""
        if len(timed_values) < 2:
            raise ValueError("Need at least 2 recent frames to estimate motion")
        self.times = [t for t, _ in timed_values]
        self.values = [v for _, v in timed_values]
        self.latest_time = self.times[-1]
        self.latest_values = self.values[-1]

        interval_seconds = (self.times[-1] - self.times[-2]).total_seconds()
        if interval_seconds <= 0:
            raise ValueError("Recent frames are not in chronological order")
        self.interval_minutes = interval_seconds / 60.0

        self.u, self.v = estimate_motion(self.values)

    def extrapolate_to(self, valid_time):
        lead_minutes = (valid_time - self.latest_time).total_seconds() / 60.0
        steps = lead_minutes / self.interval_minutes
        return self.extrapolate_to_minutes(lead_minutes, steps)

    def extrapolate_to_minutes(self, lead_minutes, steps):
        return extrapolate(self.latest_values, self.u, self.v, steps), lead_minutes

    def blend_with_hrrr(self, hrrr_field, valid_time):
        nowcast_field, lead_minutes = self.extrapolate_to(valid_time)
        weight = weight_for_lead_minutes(lead_minutes)
        return blend(nowcast_field, hrrr_field, weight)

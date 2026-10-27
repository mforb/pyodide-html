# Task 8: one reusable function combining arrays and a mask.
import numpy as np


def ranges_within(dx_km, dy_km, limit_km=6.0):
    """Return 2D ranges at or below the limit, in kilometres."""
    # Assume two equally sized 1D lists of numbers; empty lists are allowed.
    dx_km = np.asarray(dx_km, dtype=float)
    dy_km = np.asarray(dy_km, dtype=float)
    # TODO: calculate the ranges, make a mask, then return selected ranges.
    pass


dx = [3.0, -3.0, 0.0, 8.0]
dy = [4.0, 4.0, 6.0, 6.0]
print("Default limit:", ranges_within(dx, dy))
print("Changed limit:", ranges_within(dx, dy, limit_km=5.0))
print("Empty input:", ranges_within([], []))

# Add assertions: expected distances, exactly at the limit,
# negative coordinate differences, zero distance, and empty input.
# np.allclose(actual, expected) compares numeric arrays with a tolerance.

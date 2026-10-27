# Task 6: keep ranges at or below a limit (including the boundary).
import numpy as np

# Data are already in the angle order found in Task 5.
satellite = np.array(["C", "A", "D", "B"])
ranges_km = np.array([6.0, 5.0, 10.0, 5.0])
limit_km = 6.0

# TODO: mask = a comparison between ranges_km and limit_km.
# Select names with satellite[mask] and distances with ranges_km[mask].
# Print names, distances, number selected and mask[0] (the 6 km case).

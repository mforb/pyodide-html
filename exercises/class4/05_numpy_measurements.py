# Task 5: sort toy satellites by horizontal angle, then find their ranges.
# Flat 2D model: receiver at (0, 0); +x east, +y north; distances in km.
# Azimuth is clockwise from north. Angles are supplied, rounded to 0.1 degree.
import numpy as np

satellite = np.array(["A", "B", "C", "D"])
azimuth_deg = np.array([36.9, 323.1, 0.0, 53.1])
dx_km = np.array([3.0, -3.0, 0.0, 8.0])
dy_km = np.array([4.0, 4.0, 6.0, 6.0])

# This supplied step gives the row indices in angle order.
order = np.argsort(azimuth_deg)
satellite = satellite[order]
azimuth_deg = azimuth_deg[order]
dx_km = dx_km[order]
dy_km = dy_km[order]

# TODO: calculate ranges_km with np.sqrt(dx_km ** 2 + dy_km ** 2).
# Print the sorted names and angles, ranges and mean range (two decimals).

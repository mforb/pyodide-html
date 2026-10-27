# Optional Task 9: which of three receiver positions fits measured ranges?
# Idealised 2D beacons, exact ranges, synchronised clocks; no carrier phase.
import numpy as np

sat_x_km = np.array([0.0, 8.0, 0.0])
sat_y_km = np.array([0.0, 0.0, 8.0])
measured_km = np.array([5.0, np.sqrt(41.0), 5.0])


def range_error(x_km, y_km):
    dx_km = sat_x_km - x_km
    dy_km = sat_y_km - y_km
    # TODO: predict the three ranges using np.sqrt().
    # Return np.sum(np.abs(predicted_km - measured_km)).
    pass


for x, y in [(2.0, 4.0), (3.0, 4.0), (4.0, 4.0)]:
    print(f"({x:.0f}, {y:.0f}) km: error {range_error(x, y):.3f} km")

# Identify the best candidate. This compares guesses; it is not a full solver.

# Optional Task 10: orbital speed versus speed of the point directly below.
# Circular equatorial orbit, spherical NON-ROTATING Earth, no atmosphere.
import numpy as np

MU = 398600.0  # Earth's gravitational parameter, km^3/s^2


def ground_speed(height_km, earth_radius_km=6371.0):
    radius_km = earth_radius_km + height_km
    orbital_km_s = np.sqrt(MU / radius_km)
    # TODO: return orbital_km_s * earth_radius_km / radius_km.
    pass


for height in [400.0, 20200.0, 35786.0]:
    print(f"{height:.0f} km altitude: {ground_speed(height):.3f} km/s")

# Why is this smaller than orbital speed? Why does it fall with altitude?
# The 35786 km case is NOT stationary above this non-rotating model Earth.

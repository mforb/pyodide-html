# Optional Task 12: a small velocity update in a 2D orbital cross-section.
# At a 400 km circular-orbit radius; all velocities below are in km/s.
# This is an instantaneous impulse approximation at a fixed position.
import numpy as np

radius_km = 6371.0 + 400.0
circular_km_s = np.sqrt(398600.0 / radius_km)
velocity = np.array([0.0, 7.4])       # +x outward, +y tangential here
target = np.array([0.0, circular_km_s])
burn_s = 10.0


def velocity_after(velocity, acceleration, seconds):
    # TODO: return velocity + acceleration * seconds.
    pass


# Acceleration is in km/s^2. Use a provided target rather than an orbit solver.
acceleration = (target - velocity) / burn_s
updated = velocity_after(velocity, acceleration, burn_s)
print(f"Before: {velocity[1]:.3f} km/s tangential")
print(f"Target: {circular_km_s:.3f} km/s tangential")
print(f"After: {updated[1]:.3f} km/s tangential")

# Explore an outward (+x) acceleration: does it reach the tangential target?
# A real transfer also updates position and gravity, and may need more burns.

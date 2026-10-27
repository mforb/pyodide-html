# Task 3: distance = speed * one-way travel time.
# Use a rounded light speed of 300 km/ms by default.

def signal_range(travel_ms, speed_km_ms=300.0):
    # Return distance in kilometres.
    pass


print(f"Default speed: {signal_range(70.0):.1f} km")
print(f"Changed speed: {signal_range(70.0, speed_km_ms=299.8):.1f} km")

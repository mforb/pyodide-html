# Task 3: use parameters and defaults in a cable-length function.

def total_cable_length(route_m, cable_count=6, sag_fraction=0.02):
    # Return the total cable length in metres.
    pass


print(f"Default case: {total_cable_length(80.0):.1f} m")
print(f"Changed cables: {total_cable_length(80.0, cable_count=4):.1f} m")

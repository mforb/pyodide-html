# Task 6: visit each site record and check its own tolerance.
sites = {
    "Camp A": {"error_mm": 0.2, "tolerance_mm": 0.5},
    "Camp B": {"error_mm": -0.8, "tolerance_mm": 0.5},
    "Camp C": {"error_mm": 0.5, "tolerance_mm": 0.5},
}

# Plan and trace the check for Camp B and Camp C.
# Use for name, record in sites.items():
# abs(record["error_mm"]) <= record["tolerance_mm"] means OK.
# Otherwise the site needs CHECK. Print one labelled line per site.

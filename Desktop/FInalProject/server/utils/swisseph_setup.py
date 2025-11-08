import swisseph as swe
import os

# Set the ephemeris path
def setup_ephemeris():
    ephe_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "swisseph_data"))
    if not os.path.exists(ephe_path):
        raise FileNotFoundError(f"Ephemeris folder not found: {ephe_path}")
    swe.set_ephe_path(ephe_path)
    print(f"[OK] Swiss Ephemeris path set to: {ephe_path}")

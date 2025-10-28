import os
from dotenv import load_dotenv

load_dotenv()

# Data Sources
ISS_POSITION_URL = "https://api.wheretheiss.at/v1/satellites/25544"
METEOR_SHOWER_DATA = "https://data.imo.net/files/imo_calendar.json"
AURORA_FORECAST_URL = "https://services.swpc.noaa.gov/products/ovation_aurora_latest.json"
ROCKET_LAUNCH_API = "https://lldev.thespacedevs.com/2.2.0/launch/upcoming/"

# Notification Settings
CHECK_INTERVAL = int(os.getenv('CHECK_INTERVAL', 300))  # 5 minutes
ALERT_WINDOW = int(os.getenv('ALERT_WINDOW', 60))  # minutes

# Import global locations
try:
    from src.global_locations import GLOBAL_LOCATIONS, DEFAULT_LOCATIONS
except ImportError:
    DEFAULT_LOCATIONS = {
        'bangalore': {'lat': 12.9716, 'lon': 77.5946, 'name': 'Bangalore, India'},
        'delhi': {'lat': 28.7041, 'lon': 77.1025, 'name': 'Delhi, India'}
    }
    GLOBAL_LOCATIONS = DEFAULT_LOCATIONS
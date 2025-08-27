from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
from datetime import datetime
import pytz

def geocode_city(city_query: str):
    """
    Devuelve (lat, lon, display_name).
    """
    geolocator = Nominatim(user_agent="carta_natal_app")
    loc = geolocator.geocode(city_query)
    if not loc:
        raise ValueError(f"No pude geocodificar: {city_query}")
    return (loc.latitude, loc.longitude, loc.address)

def local_to_utc(date_str: str, time_str: str, lat: float, lon: float):
    """
    date_str: 'YYYY-MM-DD'
    time_str: 'HH:MM' o None si desconocida (usamos 12:00)
    Retorna datetime UTC y tzname.
    """
    if not time_str or time_str.strip() == "":
        time_str = "12:00"  # Hora media si no se sabe
    h, m = map(int, time_str.split(":"))
    y, mm, d = map(int, date_str.split("-"))

    tf = TimezoneFinder()
    tz_name = tf.timezone_at(lng=lon, lat=lat)
    if tz_name is None:
        # fallback simple
        tz_name = "UTC"

    tz = pytz.timezone(tz_name)
    local_dt = tz.localize(datetime(y, mm, d, h, m), is_dst=None)  # respeta DST correcto
    utc_dt = local_dt.astimezone(pytz.utc)
    return utc_dt, tz_name
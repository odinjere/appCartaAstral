from geo_time import geocode_city, local_to_utc
from astro_core import build_chart, planet_positions, major_aspects, houses_info

def main():
    print("=== Carta Natal (MVP) ===")
    name = input("Nombre (opcional): ").strip()
    date_str = input("Fecha de nacimiento (YYYY-MM-DD): ").strip()
    time_str = input("Hora de nacimiento (HH:MM) o dejar vacío si desconocida: ").strip()
    city = input("Ciudad y país (ej: 'San Fernando del Valle de Catamarca, Argentina'): ").strip()

    lat, lon, display = geocode_city(city)
    utc_dt, tz_name = local_to_utc(date_str, time_str, lat, lon)

    c = build_chart(utc_dt, lon, lat)

    print("\n--- Datos normalizados ---")
    print(f"Lugar: {display}")
    print(f"Lat/Lon: {lat:.5f}, {lon:.5f}")
    print(f"Zona horaria: {tz_name}")
    print(f"Fecha/Hora local → UTC: {utc_dt.strftime('%Y-%m-%d %H:%M')}")

    print("\n--- Planetas y puntos ---")
    for row in planet_positions(c):
        casa_txt = f" | Casa {row['house']}" if row['house'] else ""
        print(f"{row['name']:<9} {row['sign']:<3} {row['lon']:>8}°{casa_txt}")

    print("\n--- Casas ---")
    for h in houses_info(c):
        print(f"Casa {h['house']:>2}: {h['sign']} {h['lon']}°")

    print("\n--- Aspectos mayores ---")
    for a in major_aspects(c, orb=6):
        print(f"{a['p1']} - {a['p2']}: {a['type']} (orb {a['orb']}°)")

    print("\nListo. (Este es el MVP textual).")

if __name__ == "__main__":
    main()
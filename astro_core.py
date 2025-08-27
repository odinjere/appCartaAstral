from flatlib import const, chart, aspects

# Elegí tu sistema de casas: PLACIDUS o WHOLESIGN
HOUSE_SYSTEM = const.HOUSES_PLACIDUS

PLANETS = [
    const.SUN, const.MOON, const.MERCURY, const.VENUS, const.MARS,
    const.JUPITER, const.SATURN, const.URANUS, const.NEPTUNE, const.PLUTO
]
POINTS = [const.ASC]  # Podés agregar MC, Node, etc.: const.MC, const.NORTH_NODE

def build_chart(utc_dt, lon, lat):
    """
    Construye la carta con fecha/hora UTC en formato requerido por flatlib.
    """
    # flatlib espera strings: date 'YYYY/MM/DD' y time 'HH:MM'
    date_str = utc_dt.strftime("%Y/%m/%d")
    time_str = utc_dt.strftime("%H:%M")

    c = chart.Chart(date_str, time_str, lon, lat, hsys=HOUSE_SYSTEM)
    return c

def planet_positions(c):
    data = []
    for p in PLANETS + POINTS:
        obj = c.get(p)
        data.append({
            "id": p,
            "name": obj.name,
            "sign": obj.sign,     # ej. 'Ari', 'Tau'
            "lon": round(obj.lon, 4),   # longitud eclíptica
            "lat": round(obj.lat, 4),
            "house": getattr(obj, "house", None)
        })
    return data

def major_aspects(c, orb=6):
    objs = [c.get(p) for p in PLANETS]
    asp_list = aspects.getAspects(objs, aspects.MAJOR_ASPECTS, orb=orb)
    # Formateo simple
    out = []
    for a in asp_list:
        out.append({
            "p1": a.p1.name,
            "p2": a.p2.name,
            "type": a.type,     # CONJUNCTION, OPPOSITION, etc.
            "orb": round(a.orb, 2)
        })
    return out

def houses_info(c):
    # Casas 1..12 (asc es cúspide de casa 1)
    info = []
    for i in range(1, 13):
        h = c.houses[i]
        info.append({
            "house": i,
            "sign": h.sign,
            "lon": round(h.lon, 4)
        })
    return info
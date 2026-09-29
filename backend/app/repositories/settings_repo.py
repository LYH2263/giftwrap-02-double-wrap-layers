from app.config import DEFAULT_OVERLAP, DEFAULT_LINING_COEFFICIENT
from app.db import connect

_DEFAULTS = {
    "overlap": str(DEFAULT_OVERLAP),
    "lining_coefficient": str(DEFAULT_LINING_COEFFICIENT),
}

def get_all():
    c = connect()
    try:
        d = {r["key"]: r["value"] for r in c.execute("SELECT key,value FROM settings").fetchall()}
        for k, v in _DEFAULTS.items():
            d.setdefault(k, v)
        return d
    finally:
        c.close()

def get_overlap():
    return float(get_all()["overlap"])

def get_lining_coefficient():
    return float(get_all()["lining_coefficient"])

def set_setting(key: str, value: str):
    if key not in _DEFAULTS:
        raise KeyError(key)
    c = connect()
    try:
        c.execute(
            "INSERT INTO settings(key,value) VALUES (?,?) "
            "ON CONFLICT(key) DO UPDATE SET value=excluded.value",
            (key, str(value)),
        )
        c.commit()
    finally:
        c.close()

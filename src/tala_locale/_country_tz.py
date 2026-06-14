"""
Country → primary IANA timezone and all IANA timezones.

Computed at import time by inverting TIMEZONE_COUNTRY_MAP from _timezone_data.py.
Zero runtime dependencies. No external calls. O(1) lookup after import.

Design
------
For single-timezone countries the primary IS the only zone (e.g. Nigeria → Africa/Lagos).
For multi-timezone countries the primary is the capital/most-populated zone
(e.g. USA → America/New_York, Russia → Europe/Moscow, Brazil → America/Sao_Paulo).

Primary zone overrides are listed explicitly in _PRIMARY_OVERRIDES for the ~25
multi-timezone countries. All other countries have exactly one IANA zone so
there is no ambiguity.

Usage
-----
    from tala_locale._country_tz import COUNTRY_PRIMARY_TZ, COUNTRY_ALL_TZ

    COUNTRY_PRIMARY_TZ["NG"]   # "Africa/Lagos"
    COUNTRY_PRIMARY_TZ["US"]   # "America/New_York"
    COUNTRY_ALL_TZ["US"]       # ("America/Adak", "America/Anchorage", ...) — all ~30 US zones
    COUNTRY_ALL_TZ["ID"]       # ("Asia/Jakarta", "Asia/Jayapura", "Asia/Makassar", ...)
"""

from __future__ import annotations

from collections import defaultdict

from tala_locale._timezone_data import TIMEZONE_COUNTRY_MAP

# Explicit primary timezone for multi-timezone countries.
# Single-timezone countries are automatic (one zone → that zone is primary).
_PRIMARY_OVERRIDES: dict[str, str] = {
    # Americas
    "AR": "America/Argentina/Buenos_Aires",
    "BR": "America/Sao_Paulo",
    "CA": "America/Toronto",
    "CL": "America/Santiago",
    "EC": "America/Guayaquil",
    "GL": "America/Nuuk",
    "MX": "America/Mexico_City",
    "UM": "Pacific/Wake",
    "US": "America/New_York",
    # Europe
    "ES": "Europe/Madrid",
    "FI": "Europe/Helsinki",
    "GB": "Europe/London",  # beats Europe/Belfast alphabetically
    "MD": "Europe/Chisinau",
    "PT": "Europe/Lisbon",
    "RU": "Europe/Moscow",
    "UA": "Europe/Kyiv",
    # Africa
    "CD": "Africa/Kinshasa",
    # Asia
    "CN": "Asia/Shanghai",
    "CY": "Asia/Nicosia",
    "ID": "Asia/Jakarta",
    "IN": "Asia/Kolkata",  # beats Asia/Calcutta (legacy alias) alphabetically
    "KZ": "Asia/Almaty",
    "MN": "Asia/Ulaanbaatar",
    "MY": "Asia/Kuala_Lumpur",
    "PS": "Asia/Gaza",
    # Pacific
    "FM": "Pacific/Pohnpei",
    "KI": "Pacific/Tarawa",
    "NZ": "Pacific/Auckland",
    "PF": "Pacific/Tahiti",
    # Australia — Sydney beats ACT/Broken_Hill etc. alphabetically
    "AU": "Australia/Sydney",
}

# Build inverted map: country → sorted list of all IANA zones
_country_to_zones: dict[str, list[str]] = defaultdict(list)
for _tz, _cc in TIMEZONE_COUNTRY_MAP.items():
    _country_to_zones[_cc].append(_tz)

for _cc in _country_to_zones:
    _country_to_zones[_cc].sort()

# Public lookup tables — both are O(1) dict access after module load

COUNTRY_ALL_TZ: dict[str, tuple[str, ...]] = {
    cc: tuple(zones) for cc, zones in _country_to_zones.items()
}
"""All IANA timezone strings for a country, sorted alphabetically.

Single-timezone countries have a one-element tuple.
Multi-timezone countries have every IANA zone.

Examples::

    COUNTRY_ALL_TZ["NG"]   # ("Africa/Lagos",)
    COUNTRY_ALL_TZ["US"]   # ~30 zones from America/Adak to Pacific/Midway
    COUNTRY_ALL_TZ["ID"]   # ("Asia/Jakarta", "Asia/Jayapura", "Asia/Makassar", ...)
    COUNTRY_ALL_TZ["RU"]   # 11 zones across 11 time zones
"""

COUNTRY_PRIMARY_TZ: dict[str, str] = {
    cc: (_PRIMARY_OVERRIDES[cc] if cc in _PRIMARY_OVERRIDES else zones[0])
    for cc, zones in _country_to_zones.items()
}
"""Primary IANA timezone for a country — the capital or most-populated zone.

For single-timezone countries this is the only zone.
For multi-timezone countries this is the most-populated or capital zone.

Examples::

    COUNTRY_PRIMARY_TZ["NG"]   # "Africa/Lagos"
    COUNTRY_PRIMARY_TZ["US"]   # "America/New_York"
    COUNTRY_PRIMARY_TZ["CA"]   # "America/Toronto"
    COUNTRY_PRIMARY_TZ["RU"]   # "Europe/Moscow"
    COUNTRY_PRIMARY_TZ["BR"]   # "America/Sao_Paulo"
    COUNTRY_PRIMARY_TZ["ID"]   # "Asia/Jakarta"
    COUNTRY_PRIMARY_TZ["IN"]   # "Asia/Kolkata"  (single zone — IST is uniform)
    COUNTRY_PRIMARY_TZ["CN"]   # "Asia/Shanghai" (legally uniform despite geography)
"""

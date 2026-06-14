#!/usr/bin/env python3
"""
generate_area_data.py — Build-time generator for _area_data.py

Extracts area-code → (city, state, timezone_list) mappings from the
Google libphonenumber dataset (Apache 2.0) via the `phonenumbers` PyPI package.

Run at release time to regenerate _area_data.py:
    pip install phonenumbers
    python scripts/generate_area_data.py

Output: src/tala_locale/_area_data.py — committed to the repo.
Zero runtime dependencies — the generated file is a plain Python dict.

Priority countries (in order of business relevance):
    +1  USA & Canada  — ~330 NPA codes, critical for +1 disambiguation
    +7  Russia        — key +7 disambiguation (vs Kazakhstan)
    +55 Brazil        — 94 DDD codes
    +62 Indonesia     — 90 codes
    +91 India         — 400+ STD codes
    +52 Mexico        — 300+ LADA codes
    +27 South Africa  — 30+ codes
    +234 Nigeria      — 50+ codes
    +86 China         — 100+ codes
    +61 Australia     — ~50 codes
    +44 UK            — ~100 codes
    +49 Germany       — ~50 codes
    +33 France        — ~30 codes
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
OUTPUT_PATH = REPO_ROOT / "src" / "tala_locale" / "_area_data.py"

# Calling code → ISO country code(s) and priority
# Multiple country codes for shared prefixes (e.g. +1 = US + CA)
PRIORITY_CALLING_CODES: list[tuple[int, list[str], str]] = [
    (1, ["US", "CA"], "North America (+1) — critical for CA/US disambiguation"),
    (7, ["RU", "KZ"], "Russia/Kazakhstan (+7)"),
    (27, ["ZA"], "South Africa"),
    (44, ["GB"], "United Kingdom"),
    (49, ["DE"], "Germany"),
    (33, ["FR"], "France"),
    (52, ["MX"], "Mexico"),
    (55, ["BR"], "Brazil"),
    (61, ["AU"], "Australia"),
    (62, ["ID"], "Indonesia"),
    (86, ["CN"], "China"),
    (91, ["IN"], "India"),
    (92, ["PK"], "Pakistan"),
    (234, ["NG"], "Nigeria"),
    (254, ["KE"], "Kenya"),
    (255, ["TZ"], "Tanzania"),
    (256, ["UG"], "Uganda"),
    (233, ["GH"], "Ghana"),
    (20, ["EG"], "Egypt"),
    (212, ["MA"], "Morocco"),
    (81, ["JP"], "Japan"),
    (82, ["KR"], "South Korea"),
    (65, ["SG"], "Singapore"),
    (60, ["MY"], "Malaysia"),
    (66, ["TH"], "Thailand"),
    (971, ["AE"], "United Arab Emirates"),
    (966, ["SA"], "Saudi Arabia"),
]


def get_timezones_for_number(phone_number_obj) -> list[str]:
    """Get IANA timezones for a phonenumbers phone number object."""
    try:
        from phonenumbers import timezone as pn_tz

        zones = pn_tz.time_zones_for_number(phone_number_obj)
        return list(zones)
    except Exception:
        return []


def extract_area_data() -> dict[str, dict]:
    """
    Extract area code data for priority countries.

    Returns a dict keyed by calling_code (as string) → dict of:
        area_code (str) → {
            "city": str | None,
            "state": str | None,
            "timezones": list[str],
            "country": str,
        }
    """
    try:
        import phonenumbers
        from phonenumbers import geocoder
        from phonenumbers import timezone as pn_tz
    except ImportError:
        print("ERROR: phonenumbers not installed. Run: pip install phonenumbers")
        sys.exit(1)

    result: dict[str, dict] = {}

    for calling_code, countries, description in PRIORITY_CALLING_CODES:
        print(f"Processing +{calling_code} ({description})...")
        code_data: dict[str, dict] = {}

        if calling_code == 1:
            # North America: iterate NPA codes 200-999
            _extract_npa_codes(code_data, phonenumbers, geocoder, pn_tz)
        elif calling_code == 7:
            # Russia/Kazakhstan: iterate area codes
            _extract_ru_kz_codes(code_data, phonenumbers, geocoder, pn_tz)
        elif calling_code == 55:
            # Brazil: DDD codes 11-99
            _extract_brazil_codes(code_data, phonenumbers, geocoder, pn_tz)
        elif calling_code == 91:
            # India: STD codes
            _extract_india_codes(code_data, phonenumbers, geocoder, pn_tz)
        elif calling_code == 62:
            # Indonesia
            _extract_indonesia_codes(code_data, phonenumbers, geocoder, pn_tz)
        elif calling_code == 52:
            # Mexico: LADA codes
            _extract_mexico_codes(code_data, phonenumbers, geocoder, pn_tz)
        else:
            # Generic extraction for other countries
            _extract_generic(
                code_data, calling_code, countries, phonenumbers, geocoder, pn_tz
            )

        if code_data:
            result[str(calling_code)] = code_data
            print(f"  -> {len(code_data)} area codes extracted")
        else:
            print("  -> No area codes found (will use country-level fallback)")

    return result


def _try_parse(phonenumbers, number_str: str) -> object | None:
    """Parse a phone number string, return None on failure."""
    try:
        return phonenumbers.parse(number_str, None)
    except Exception:
        return None


def _get_city_state(
    geocoder, pn_obj, lang: str = "en"
) -> tuple[str | None, str | None]:
    """Extract city and state from a geocoded description."""
    try:
        desc = geocoder.description_for_number(pn_obj, lang)
        if not desc:
            return None, None
        # Format is typically "City, State" or "City, Country"
        parts = [p.strip() for p in desc.split(",")]
        if len(parts) >= 2:
            return parts[0] or None, parts[1] or None
        elif len(parts) == 1:
            return parts[0] or None, None
        return None, None
    except Exception:
        return None, None


def _extract_npa_codes(result: dict, phonenumbers, geocoder, pn_tz) -> None:
    """Extract North American +1 NPA (area) codes."""
    seen_npas: set[str] = set()

    for npa in range(200, 1000):
        npa_str = str(npa)
        # Try a sample number in this NPA
        sample = f"+1{npa_str}5550100"
        pn_obj = _try_parse(phonenumbers, sample)
        if pn_obj is None:
            continue
        if not phonenumbers.is_valid_number(pn_obj):
            continue
        if npa_str in seen_npas:
            continue

        city, state = _get_city_state(geocoder, pn_obj)
        zones = list(pn_tz.time_zones_for_number(pn_obj))

        # Determine country from timezone
        country = _country_from_npa_zones(zones, npa_str)

        if city or state or zones:
            seen_npas.add(npa_str)
            result[npa_str] = {
                "city": city,
                "state": state,
                "timezones": zones,
                "country": country,
            }


def _country_from_npa_zones(zones: list[str], npa: str) -> str:
    """Determine whether an NPA is US or CA based on its timezones."""
    # Canadian NPAs typically have America/Toronto, America/Vancouver,
    # America/Halifax, America/Winnipeg, America/Edmonton, etc.
    # but so do US NPAs bordering Canada.
    # Use a hardcoded known-Canadian NPA prefix list for accuracy.
    # NPA codes assigned to Canada (NANP):
    _CA_NPAS = {
        "204",
        "226",
        "236",
        "249",
        "250",
        "289",
        "306",
        "343",
        "365",
        "367",
        "382",
        "403",
        "416",
        "418",
        "431",
        "437",
        "438",
        "450",
        "506",
        "514",
        "519",
        "548",
        "579",
        "581",
        "587",
        "604",
        "613",
        "639",
        "647",
        "672",
        "705",
        "709",
        "742",
        "778",
        "780",
        "782",
        "807",
        "819",
        "825",
        "867",
        "873",
        "902",
        "905",
    }
    if npa in _CA_NPAS:
        return "CA"
    # Check zones for Canadian zone names
    ca_zones = {
        "America/Toronto",
        "America/Vancouver",
        "America/Halifax",
        "America/Winnipeg",
        "America/Edmonton",
        "America/St_Johns",
        "America/Regina",
        "America/Moncton",
        "America/Glace_Bay",
        "America/Goose_Bay",
        "America/Blanc-Sablon",
        "America/Dawson",
        "America/Whitehorse",
        "America/Iqaluit",
        "America/Rankin_Inlet",
        "America/Resolute",
        "America/Cambridge_Bay",
        "America/Inuvik",
        "America/Creston",
        "America/Dawson_Creek",
        "America/Fort_Nelson",
        "America/Nipigon",
        "America/Rainy_River",
        "America/Swift_Current",
        "America/Thunder_Bay",
        "America/Pangnirtung",
    }
    if zones and all(z in ca_zones for z in zones):
        return "CA"
    return "US"


def _extract_ru_kz_codes(result: dict, phonenumbers, geocoder, pn_tz) -> None:
    """Extract Russian and Kazakhstani area codes."""
    # Russia uses 3-digit area codes after +7
    # Kazakhstan uses 7 followed by 2-3 digit codes
    # Sample area codes for key Russian cities
    ru_sample_codes = [
        "495",
        "499",  # Moscow
        "812",  # Saint Petersburg
        "343",  # Yekaterinburg
        "383",  # Novosibirsk
        "846",  # Samara
        "861",  # Krasnodar
        "863",  # Rostov-on-Don
        "831",  # Nizhny Novgorod
        "422",  # Vladivostok
        "423",  # Vladivostok (mobile)
        "4212",  # Khabarovsk
        "3952",  # Irkutsk
        "3822",  # Tomsk
        "3812",  # Omsk
        "8442",  # Volgograd
        "347",  # Ufa
        "3532",  # Orenburg
        "4812",  # Smolensk
        "4822",  # Tver
        "4872",  # Tula
    ]
    # Kazakhstan area codes
    kz_sample_codes = [
        "727",  # Almaty
        "717",  # Astana (Nur-Sultan)
        "7172",  # Astana
        "721",  # Shymkent
        "725",  # Aktobe
        "722",  # Taraz
        "726",  # Pavlodar
        "7232",  # Oskemen
    ]

    for code in ru_sample_codes:
        sample = f"+7{code}5550100"
        pn_obj = _try_parse(phonenumbers, sample)
        if pn_obj is None or not phonenumbers.is_valid_number(pn_obj):
            continue
        city, state = _get_city_state(geocoder, pn_obj)
        zones = list(pn_tz.time_zones_for_number(pn_obj))
        if city or zones:
            result[code] = {
                "city": city,
                "state": state,
                "timezones": zones,
                "country": "RU",
            }

    for code in kz_sample_codes:
        sample = f"+7{code}5550100"
        pn_obj = _try_parse(phonenumbers, sample)
        if pn_obj is None or not phonenumbers.is_valid_number(pn_obj):
            continue
        city, state = _get_city_state(geocoder, pn_obj)
        zones = list(pn_tz.time_zones_for_number(pn_obj))
        if city or zones:
            result[code] = {
                "city": city,
                "state": state,
                "timezones": zones,
                "country": "KZ",
            }


def _extract_brazil_codes(result: dict, phonenumbers, geocoder, pn_tz) -> None:
    """Extract Brazilian DDD area codes (2-digit, 11-99)."""
    for ddd in range(11, 100):
        ddd_str = str(ddd)
        sample = f"+55{ddd_str}912345678"
        pn_obj = _try_parse(phonenumbers, sample)
        if pn_obj is None or not phonenumbers.is_valid_number(pn_obj):
            continue
        city, state = _get_city_state(geocoder, pn_obj)
        zones = list(pn_tz.time_zones_for_number(pn_obj))
        if city or zones:
            result[ddd_str] = {
                "city": city,
                "state": state,
                "timezones": zones,
                "country": "BR",
            }


def _extract_india_codes(result: dict, phonenumbers, geocoder, pn_tz) -> None:
    """Extract Indian STD codes."""
    # India has 2-4 digit STD codes. Sample key cities.
    india_codes = [
        "11",  # Delhi
        "22",  # Mumbai
        "33",  # Kolkata
        "44",  # Chennai
        "80",  # Bangalore
        "40",  # Hyderabad
        "20",  # Pune
        "79",  # Ahmedabad
        "141",  # Jaipur
        "522",  # Lucknow
        "612",  # Patna
        "674",  # Bhubaneswar
        "651",  # Ranchi
        "172",  # Chandigarh
        "821",  # Mysore
        "413",  # Pondicherry
        "471",  # Thiruvananthapuram
        "484",  # Kochi
        "495",  # Kozhikode
        "452",  # Madurai
        "422",  # Coimbatore
        "240",  # Aurangabad
        "712",  # Nagpur
        "361",  # Guwahati
        "191",  # Jammu
    ]
    for code in india_codes:
        sample = f"+91{code}23456789"
        pn_obj = _try_parse(phonenumbers, sample)
        if pn_obj is None or not phonenumbers.is_valid_number(pn_obj):
            continue
        city, state = _get_city_state(geocoder, pn_obj)
        zones = list(pn_tz.time_zones_for_number(pn_obj))
        if city or zones:
            result[code] = {
                "city": city,
                "state": state,
                "timezones": zones,
                "country": "IN",
            }


def _extract_indonesia_codes(result: dict, phonenumbers, geocoder, pn_tz) -> None:
    """Extract Indonesian area codes."""
    indonesia_codes = [
        "21",  # Jakarta
        "22",  # Bandung
        "24",  # Semarang
        "31",  # Surabaya
        "361",  # Bali/Denpasar — WITA (UTC+8)
        "370",  # Lombok — WITA
        "371",  # Sumbawa — WITA
        "380",  # Ende — WITA
        "385",  # Maumere — WITA
        "411",  # Makassar — WITA
        "430",  # Palu — WITA
        "451",  # Manado — WITA
        "901",  # Papua/Jayapura — WIT (UTC+9)
        "962",  # Merauke — WIT
        "511",  # Banjarmasin
        "541",  # Samarinda
        "542",  # Balikpapan
        "623",  # Pontianak
        "561",  # Pontianak (alternate)
        "711",  # Palembang
        "751",  # Padang
        "61",  # Medan
    ]
    for code in indonesia_codes:
        sample = f"+62{code}12345678"
        pn_obj = _try_parse(phonenumbers, sample)
        if pn_obj is None or not phonenumbers.is_valid_number(pn_obj):
            continue
        city, state = _get_city_state(geocoder, pn_obj)
        zones = list(pn_tz.time_zones_for_number(pn_obj))
        if city or zones:
            result[code] = {
                "city": city,
                "state": state,
                "timezones": zones,
                "country": "ID",
            }


def _extract_mexico_codes(result: dict, phonenumbers, geocoder, pn_tz) -> None:
    """Extract Mexican LADA codes."""
    mexico_codes = [
        "55",  # Mexico City
        "33",  # Guadalajara
        "81",  # Monterrey
        "222",  # Puebla
        "777",  # Cuernavaca
        "442",  # Querétaro
        "477",  # León
        "461",  # Celaya
        "444",  # San Luis Potosí
        "867",  # Reynosa
        "844",  # Saltillo
        "614",  # Chihuahua
        "656",  # Ciudad Juárez
        "686",  # Mexicali
        "664",  # Tijuana
        "662",  # Hermosillo
        "668",  # Los Mochis
        "667",  # Culiacán
        "871",  # Torreón
        "921",  # Coatzacoalcos
        "229",  # Veracruz
        "951",  # Oaxaca
        "999",  # Mérida
        "998",  # Cancún
        "993",  # Villahermosa
        "961",  # Tuxtla Gutiérrez
        "312",  # Colima
        "311",  # Tepic
        "329",  # Puerto Vallarta
        "322",  # Puerto Vallarta
        "744",  # Acapulco
        "755",  # Zihuatanejo
        "388",  # Autlán
    ]
    for code in mexico_codes:
        sample = f"+52{code}12345678"
        pn_obj = _try_parse(phonenumbers, sample)
        if pn_obj is None or not phonenumbers.is_valid_number(pn_obj):
            continue
        city, state = _get_city_state(geocoder, pn_obj)
        zones = list(pn_tz.time_zones_for_number(pn_obj))
        if city or zones:
            result[code] = {
                "city": city,
                "state": state,
                "timezones": zones,
                "country": "MX",
            }


def _extract_generic(
    result: dict, calling_code: int, countries: list[str], phonenumbers, geocoder, pn_tz
) -> None:
    """Generic extractor: try 2-4 digit area codes."""
    country_code = countries[0]
    # Try common 2-3 digit patterns
    for length in (2, 3):
        for code_int in range(10 ** (length - 1), 10**length):
            code_str = str(code_int)
            # Sample subscriber number
            sample = f"+{calling_code}{code_str}12345678"
            pn_obj = _try_parse(phonenumbers, sample)
            if pn_obj is None or not phonenumbers.is_valid_number(pn_obj):
                continue
            city, state = _get_city_state(geocoder, pn_obj)
            zones = list(pn_tz.time_zones_for_number(pn_obj))
            if (city or state) and code_str not in result:
                result[code_str] = {
                    "city": city,
                    "state": state,
                    "timezones": zones,
                    "country": country_code,
                }


def write_output(data: dict[str, dict]) -> None:
    """Write the extracted data to _area_data.py."""
    lines = [
        '"""',
        "Area code data for tala-locale.",
        "",
        "AUTO-GENERATED — do not edit by hand.",
        "Regenerate with: python scripts/generate_area_data.py",
        "",
        "Data source: Google libphonenumber (Apache 2.0)",
        "via the `phonenumbers` PyPI package (build-time only).",
        "",
        "Structure:",
        "    AREA_CODE_MAP[calling_code_str][area_code_str] = {",
        '        "city": str | None,',
        '        "state": str | None,',
        '        "timezones": list[str],',
        '        "country": str,  # ISO 3166-1 alpha-2',
        "    }",
        '"""',
        "",
        "from __future__ import annotations",
        "",
        "AREA_CODE_MAP: dict[str, dict[str, dict]] = {",
    ]

    total_codes = 0
    for calling_code_str, code_data in sorted(data.items(), key=lambda x: int(x[0])):
        lines.append(f"    # +{calling_code_str}")
        lines.append(f"    {calling_code_str!r}: {{")
        for area_code, info in sorted(code_data.items()):
            city = info.get("city")
            state = info.get("state")
            timezones = info.get("timezones", [])
            country = info.get("country", "")
            city_repr = repr(city) if city else "None"
            state_repr = repr(state) if state else "None"
            tz_repr = repr(timezones)
            lines.append(
                f"        {area_code!r}: "
                f'{{"city": {city_repr}, "state": {state_repr}, '
                f'"timezones": {tz_repr}, "country": {country!r}}},'
            )
            total_codes += 1
        lines.append("    },")

    lines += [
        "}",
        "",
        f"# {total_codes} area codes across {len(data)} calling code groups",
    ]

    output = "\n".join(lines) + "\n"
    OUTPUT_PATH.write_text(output, encoding="utf-8")
    print(f"\nWrote {total_codes} area codes to {OUTPUT_PATH}")


def main() -> None:
    print("tala-locale area code generator")
    print("=" * 50)
    data = extract_area_data()
    write_output(data)
    print("\nDone. Commit src/tala_locale/_area_data.py to the repo.")


if __name__ == "__main__":
    main()

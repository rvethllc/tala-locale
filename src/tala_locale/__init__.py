"""
tala-locale — Phone number, timezone, and country locale inference.

Given any phone number, infer the ISO country code, currency, language,
timezone, UTC offset, and full formatting metadata — in one call, zero
network requests, zero runtime dependencies.

Quick start::

    from tala_locale import infer_full_locale, infer_locale, get_extended, format_amount

    # v3.0.0 — full inference, flat fields on result
    r = infer_full_locale("+2348012345678")
    print(r.country)          # "NG"
    print(r.timezone)         # "Africa/Lagos"
    print(r.utc_offset_hours) # 1.0
    print(r.confidence)       # 1.0
    # Flat access — no more .extended.xxx
    print(r.currency_symbol)  # "₦"
    print(r.vat_rate)         # 0.075
    print(r.date_format)      # "%d/%m/%Y"
    print(r.language)         # "en-NG"  (BCP 47, not bare "en")

    # +1 disambiguation — area code resolution (no browser timezone needed)
    r = infer_full_locale("+14165551234")   # 416 = Toronto
    print(r.country)    # "CA"
    print(r.timezone)   # "America/Toronto"
    print(r.confidence) # 0.95

    # Convert UTC to local time
    from datetime import datetime, timezone
    from tala_locale import get_local_datetime, format_local_datetime

    utc = datetime(2025, 6, 14, 11, 30, tzinfo=timezone.utc)
    local = get_local_datetime(utc, "NG")
    print(local.hour)   # 12  (WAT = UTC+1)

    print(format_local_datetime(utc, "NG"))  # "14/06/2025 12:30"
    print(format_local_datetime(utc, "US"))  # "06/14/2025 07:30"
    print(format_local_datetime(utc, "DE"))  # "14.06.2025 13:30"

    # Timezone utilities
    from tala_locale import infer_timezone, infer_timezones, get_utc_offset

    print(infer_timezone("US"))        # "America/New_York"
    print(infer_timezone("CA"))        # "America/Toronto"
    print(infer_timezone("ID"))        # "Asia/Jakarta"
    print(len(infer_timezones("US")))  # 30  (all US IANA zones)
    print(get_utc_offset("NG"))        # 1.0
    print(get_utc_offset("IN"))        # 5.5  (IST = UTC+5:30)
    print(get_utc_offset("NP"))        # 5.75 (NPT = UTC+5:45)

    # v0.2.0 functions still available
    result = infer_locale("+2348012345678")
    print(result.country)   # "NG"
    print(result.currency)  # "NGN"

    ext = get_extended("NG")
    print(ext.currency_symbol)  # "₦"
    print(ext.date_format)      # "%d/%m/%Y"
    print(ext.rtl)              # False

    print(format_amount(1234.5, "NG"))  # "₦1,234.50"
    print(format_amount(1234.5, "DE"))  # "1.234,50 €"
"""

from tala_locale._core import (
    ExtendedLocale,
    FullLocaleResult,
    LocaleResult,
    format_amount,
    format_local_datetime,
    get_extended,
    get_local_datetime,
    get_utc_offset,
    infer_country,
    infer_country_from_timezone,
    infer_currency,
    infer_full_locale,
    infer_language,
    infer_locale,
    infer_timezone,
    infer_timezones,
    is_supported,
    supported_countries,
)

__all__ = [
    # Types
    "LocaleResult",
    "FullLocaleResult",
    "ExtendedLocale",
    # Primary entry points
    "infer_locale",
    "infer_full_locale",
    # Shortcuts — phone
    "infer_country",
    "infer_currency",
    "infer_language",
    # Shortcuts — timezone
    "infer_country_from_timezone",
    "infer_timezone",
    "infer_timezones",
    # UTC offset + datetime conversion
    "get_utc_offset",
    "get_local_datetime",
    "format_local_datetime",
    # Extended data
    "get_extended",
    "format_amount",
    # Utility
    "is_supported",
    "supported_countries",
]

__version__ = "3.0.0"

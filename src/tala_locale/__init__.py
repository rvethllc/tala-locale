"""
tala-locale — Phone number, timezone, and country locale inference.

Given any phone number, infer the ISO country code, currency, and language.
Given an IANA timezone, infer the country.
Given a country code, get extended locale data for document formatting.
Zero dependencies. Works with any phone format.

Quick start::

    from tala_locale import infer_locale, get_extended, format_amount

    result = infer_locale("+2348012345678")
    print(result.country)   # "NG"
    print(result.currency)  # "NGN"
    print(result.language)  # "en"

    ext = get_extended("NG")
    print(ext.currency_symbol)  # "₦"
    print(ext.vat_rate)         # 0.075
    print(ext.date_format)      # "%d/%m/%Y"

    print(format_amount(1234.5, "NG"))  # "₦1,234.50"
    print(format_amount(1234.5, "DE"))  # "1.234,50 €"
"""

from tala_locale._core import (
    ExtendedLocale,
    LocaleResult,
    format_amount,
    get_extended,
    infer_country,
    infer_country_from_timezone,
    infer_currency,
    infer_language,
    infer_locale,
    is_supported,
    supported_countries,
)

__all__ = [
    "LocaleResult",
    "ExtendedLocale",
    "infer_locale",
    "infer_country",
    "infer_currency",
    "infer_language",
    "infer_country_from_timezone",
    "is_supported",
    "supported_countries",
    "get_extended",
    "format_amount",
]

__version__ = "0.2.0"

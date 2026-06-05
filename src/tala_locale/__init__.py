"""
tala-locale — Phone number to locale inference.

Given any phone number, infer the ISO country code, currency, and language.
Zero dependencies. Works with any phone format.

Quick start::

    from tala_locale import infer_locale

    result = infer_locale("+2348012345678")
    print(result.country)   # "NG"
    print(result.currency)  # "NGN"
    print(result.language)  # "en"

    # Or unpack like a tuple:
    country, currency, language = infer_locale("+14155552671")
"""

from tala_locale._core import (
    LocaleResult,
    infer_country,
    infer_currency,
    infer_language,
    infer_locale,
    is_supported,
    supported_countries,
)

__all__ = [
    "LocaleResult",
    "infer_locale",
    "infer_country",
    "infer_currency",
    "infer_language",
    "is_supported",
    "supported_countries",
]

__version__ = "0.1.0"

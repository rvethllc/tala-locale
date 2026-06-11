"""
Core inference logic for tala-locale.

All public symbols are re-exported from tala_locale.__init__.
"""

from __future__ import annotations

from typing import NamedTuple

from tala_locale._data import PHONE_PREFIX_MAP
from tala_locale._extended_data import EXTENDED_LOCALE_MAP, ExtendedLocale
from tala_locale._timezone_data import TIMEZONE_COUNTRY_MAP

# Pre-sort prefixes longest-first once at import time — O(1) per lookup
_SORTED_PREFIXES: list[str] = sorted(PHONE_PREFIX_MAP, key=len, reverse=True)


class LocaleResult(NamedTuple):
    """Result of a locale inference call.

    Behaves like a plain tuple so it unpacks naturally::

        country, currency, language = infer_locale("+2348012345678")

    But also has named fields and a helper method::

        result = infer_locale("+2348012345678")
        if result.is_known():
            print(result.currency)   # "NGN"
    """

    country: str | None
    """ISO 3166-1 alpha-2 country code, e.g. "NG", "US", "DE". None if unknown."""

    currency: str | None
    """ISO 4217 currency code, e.g. "NGN", "USD", "EUR". None if unknown."""

    language: str | None
    """ISO 639-1 language code, e.g. "en", "fr", "ar". None if unknown."""

    def is_known(self) -> bool:
        """Return True if the phone prefix was recognised."""
        return self.country is not None


_UNKNOWN = LocaleResult(None, None, None)


def _canonicalize(phone: str) -> str:
    """Strip all non-digit characters and the 'whatsapp:' prefix."""
    if phone and phone.startswith("whatsapp:"):
        phone = phone[len("whatsapp:") :]
    return "".join(c for c in (phone or "") if c.isdigit())


def infer_locale(phone_number: str) -> LocaleResult:
    """Infer country, currency, and language from a phone number.

    Uses longest-prefix-match against E.164 country calling codes.

    Parameters
    ----------
    phone_number:
        A phone number in any common format.  The following are all
        equivalent::

            "+234 801 234 5678"
            "2348012345678"
            "+2348012345678"
            "whatsapp:+2348012345678"
            "(234) 801-234-5678"

    Returns
    -------
    LocaleResult
        A named tuple ``(country, currency, language)``.  All three fields
        are ``None`` when the prefix is not recognised — the caller should
        ask the user explicitly rather than assuming a default.

    Examples
    --------
    >>> infer_locale("+2348012345678")
    LocaleResult(country='NG', currency='NGN', language='en')
    >>> infer_locale("+14155552671")
    LocaleResult(country='US', currency='USD', language='en')
    >>> infer_locale("+33612345678")
    LocaleResult(country='FR', currency='EUR', language='fr')
    >>> infer_locale("+882123456789")
    LocaleResult(country=None, currency=None, language=None)
    """
    digits = _canonicalize(phone_number)
    if not digits:
        return _UNKNOWN
    for prefix in _SORTED_PREFIXES:
        if digits.startswith(prefix):
            return LocaleResult(*PHONE_PREFIX_MAP[prefix])
    return _UNKNOWN


def infer_country(phone_number: str) -> str | None:
    """Return only the ISO 3166-1 alpha-2 country code, or None."""
    return infer_locale(phone_number).country


def infer_currency(phone_number: str) -> str | None:
    """Return only the ISO 4217 currency code, or None."""
    return infer_locale(phone_number).currency


def infer_language(phone_number: str) -> str | None:
    """Return only the ISO 639-1 language code, or None."""
    return infer_locale(phone_number).language


def is_supported(phone_number: str) -> bool:
    """Return True if the phone number prefix is recognised.

    Shortcut for ``infer_locale(phone_number).is_known()``.

    Examples
    --------
    >>> is_supported("+2348012345678")
    True
    >>> is_supported("+8821234567")
    False
    """
    return infer_locale(phone_number).is_known()


def infer_country_from_timezone(timezone: str) -> str | None:
    """Infer ISO 3166-1 alpha-2 country code from an IANA timezone string.

    Parameters
    ----------
    timezone:
        An IANA timezone string, e.g. ``"Africa/Lagos"``, ``"America/Toronto"``,
        ``"Asia/Jakarta"``.  Typically obtained from
        ``Intl.DateTimeFormat().resolvedOptions().timeZone`` in the browser.

    Returns
    -------
    str | None
        ISO country code, e.g. ``"NG"``, ``"CA"``, ``"ID"``.
        ``None`` if the timezone is unrecognised.

    Notes
    -----
    Multi-timezone countries are handled correctly:

    - Indonesia has three zones (Jakarta/Makassar/Jayapura) — all return ``"ID"``
    - Canada and USA share the +1 calling code, but their timezones are distinct
      (``"America/Toronto"`` → ``"CA"``, ``"America/New_York"`` → ``"US"``)
    - Russia's 11 zones all return ``"RU"``

    Examples
    --------
    >>> infer_country_from_timezone("Africa/Lagos")
    'NG'
    >>> infer_country_from_timezone("America/Toronto")
    'CA'
    >>> infer_country_from_timezone("America/New_York")
    'US'
    >>> infer_country_from_timezone("Asia/Jakarta")
    'ID'
    >>> infer_country_from_timezone("Asia/Makassar")
    'ID'
    >>> infer_country_from_timezone("Unknown/Zone")
    """
    if not timezone:
        return None
    return TIMEZONE_COUNTRY_MAP.get(timezone)


def supported_countries() -> list[dict[str, str]]:
    """Return a list of all supported countries with their metadata.

    Each entry is a dict with keys ``prefix``, ``country``, ``currency``,
    ``language``.  Sorted by prefix length then lexicographically.

    Useful for building country-selector dropdowns, documentation, or
    validation lists.

    Examples
    --------
    >>> entries = supported_countries()
    >>> len(entries)
    191
    >>> entries[0]
    {'prefix': '1', 'country': 'US', 'currency': 'USD', 'language': 'en'}
    """
    return [
        {
            "prefix": prefix,
            "country": country,
            "currency": currency,
            "language": language,
        }
        for prefix, (country, currency, language) in sorted(
            PHONE_PREFIX_MAP.items(), key=lambda kv: (len(kv[0]), kv[0])
        )
    ]


def get_extended(country_code: str) -> ExtendedLocale | None:
    """Return extended locale metadata for a country code, or None if unknown.

    Parameters
    ----------
    country_code:
        ISO 3166-1 alpha-2 country code, e.g. ``"NG"``, ``"DE"``, ``"US"``.
        Case-insensitive.

    Returns
    -------
    ExtendedLocale | None
        Named tuple with currency symbol, number formatting, VAT rate, date
        format, RTL flag, week start, and BCP 47 tag.  ``None`` when the
        country code is not in the extended dataset.

    Examples
    --------
    >>> ext = get_extended("NG")
    >>> ext.currency_symbol
    '₦'
    >>> ext.vat_rate
    0.075
    >>> ext.rtl
    False
    >>> get_extended("XX") is None
    True
    """
    if not country_code:
        return None
    return EXTENDED_LOCALE_MAP.get(country_code.upper())


def format_amount(value: float | int, country_code: str) -> str:
    """Format a monetary amount using the country's locale conventions.

    Places the currency symbol before or after the amount per local convention,
    uses the correct decimal and thousands separators.

    Parameters
    ----------
    value:
        The numeric amount to format, e.g. ``1234.5``.
    country_code:
        ISO 3166-1 alpha-2 country code.  Falls back to plain two-decimal
        formatting with no symbol when the country is not in the extended
        dataset.

    Returns
    -------
    str
        Formatted string, e.g. ``"₦1,234.50"``, ``"1.234,50 €"``,
        ``"R 1 234.50"``.

    Examples
    --------
    >>> format_amount(1234.5, "NG")
    '₦1,234.50'
    >>> format_amount(1234.5, "DE")
    '1.234,50 €'
    >>> format_amount(1234.5, "FR")
    '1 234,50 €'
    >>> format_amount(1234.5, "US")
    '$1,234.50'
    >>> format_amount(1234.5, "ZA")
    'R 1 234.50'
    """
    ext = get_extended(country_code)
    if ext is None:
        return f"{value:.2f}"

    # Build the numeric part with correct separators
    int_part, dec_part = f"{abs(value):.2f}".split(".")

    # Insert thousands separators
    groups: list[str] = []
    while len(int_part) > 3:
        groups.append(int_part[-3:])
        int_part = int_part[:-3]
    groups.append(int_part)
    int_formatted = ext.thousands_sep.join(reversed(groups))

    numeric = f"{int_formatted}{ext.decimal_sep}{dec_part}"
    sign = "-" if value < 0 else ""

    if ext.currency_before:
        return f"{sign}{ext.currency_symbol}{numeric}"
    else:
        return f"{sign}{numeric} {ext.currency_symbol}"


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

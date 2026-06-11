"""
Extended locale data for tala-locale v0.2.0.

Maps ISO 3166-1 alpha-2 country codes to formatting and regulatory metadata
needed for enterprise document generation (invoices, receipts, reports).

Data sources: ISO 4217 (currency symbols), CLDR (number formatting),
government VAT legislation (rates as of 2025), Unicode CLDR (BCP 47 tags).

All values are STATIC — they do not call any external service.
VAT rates reflect standard rates and should be verified before tax filing.
"""

from __future__ import annotations

from typing import NamedTuple


class ExtendedLocale(NamedTuple):
    """Extended locale data for a country.

    Fields
    ------
    currency_symbol : str
        Printable currency symbol, e.g. ``"₦"``, ``"$"``, ``"€"``.
    currency_before : bool
        True if the symbol precedes the amount (``$1,234.56``),
        False if it follows (``1.234,56 €``).
    decimal_sep : str
        Decimal separator character — ``"."`` or ``","``
    thousands_sep : str
        Thousands separator character — ``","`` or ``"."`` or ``" "`` (space).
    vat_rate : float
        Standard VAT/GST/sales-tax rate as a decimal fraction, e.g. ``0.075``
        for 7.5 %.  ``0.0`` when no national VAT applies.
    vat_name : str
        Local name for the consumption tax, e.g. ``"VAT"``, ``"GST"``, ``"TVA"``.
        Empty string when ``vat_rate == 0.0``.
    date_format : str
        strftime-compatible date format string, e.g. ``"%d/%m/%Y"``.
    rtl : bool
        True when the primary script is right-to-left (Arabic, Hebrew, etc.).
    week_start : int
        ISO weekday of the first day of the week: 0=Monday … 6=Sunday.
    bcp47 : str
        BCP 47 language tag for the primary locale, e.g. ``"en-NG"``.
    """

    currency_symbol: str
    currency_before: bool
    decimal_sep: str
    thousands_sep: str
    vat_rate: float
    vat_name: str
    date_format: str
    rtl: bool
    week_start: int
    bcp47: str


# ---------------------------------------------------------------------------
# EXTENDED_LOCALE_MAP
# ---------------------------------------------------------------------------
# Key: ISO 3166-1 alpha-2 country code (uppercase, 2 chars)
# Value: ExtendedLocale
#
# Coverage: All of Africa + key MENA, European, Asian, and Americas markets.
# ---------------------------------------------------------------------------

EXTENDED_LOCALE_MAP: dict[str, ExtendedLocale] = {
    # ── Africa ──────────────────────────────────────────────────────────────
    # Nigeria — primary TALA market
    "NG": ExtendedLocale(
        currency_symbol="₦",
        currency_before=True,
        decimal_sep=".",
        thousands_sep=",",
        vat_rate=0.075,
        vat_name="VAT",
        date_format="%d/%m/%Y",
        rtl=False,
        week_start=0,
        bcp47="en-NG",
    ),
    # Kenya
    "KE": ExtendedLocale(
        currency_symbol="KSh",
        currency_before=True,
        decimal_sep=".",
        thousands_sep=",",
        vat_rate=0.16,
        vat_name="VAT",
        date_format="%d/%m/%Y",
        rtl=False,
        week_start=0,
        bcp47="sw-KE",
    ),
    # South Africa
    "ZA": ExtendedLocale(
        currency_symbol="R",
        currency_before=True,
        decimal_sep=".",
        thousands_sep=" ",
        vat_rate=0.15,
        vat_name="VAT",
        date_format="%Y/%m/%d",
        rtl=False,
        week_start=0,
        bcp47="en-ZA",
    ),
    # Ghana
    "GH": ExtendedLocale(
        currency_symbol="₵",
        currency_before=True,
        decimal_sep=".",
        thousands_sep=",",
        vat_rate=0.15,
        vat_name="VAT",
        date_format="%d/%m/%Y",
        rtl=False,
        week_start=0,
        bcp47="en-GH",
    ),
    # Egypt
    "EG": ExtendedLocale(
        currency_symbol="E£",
        currency_before=True,
        decimal_sep=".",
        thousands_sep=",",
        vat_rate=0.14,
        vat_name="VAT",
        date_format="%d/%m/%Y",
        rtl=True,
        week_start=6,
        bcp47="ar-EG",
    ),
    # Tanzania
    "TZ": ExtendedLocale(
        currency_symbol="TSh",
        currency_before=True,
        decimal_sep=".",
        thousands_sep=",",
        vat_rate=0.18,
        vat_name="VAT",
        date_format="%d/%m/%Y",
        rtl=False,
        week_start=0,
        bcp47="sw-TZ",
    ),
    # Uganda
    "UG": ExtendedLocale(
        currency_symbol="USh",
        currency_before=True,
        decimal_sep=".",
        thousands_sep=",",
        vat_rate=0.18,
        vat_name="VAT",
        date_format="%d/%m/%Y",
        rtl=False,
        week_start=0,
        bcp47="en-UG",
    ),
    # Ethiopia
    "ET": ExtendedLocale(
        currency_symbol="Br",
        currency_before=True,
        decimal_sep=".",
        thousands_sep=",",
        vat_rate=0.15,
        vat_name="VAT",
        date_format="%d/%m/%Y",
        rtl=False,
        week_start=0,
        bcp47="am-ET",
    ),
    # Rwanda
    "RW": ExtendedLocale(
        currency_symbol="RF",
        currency_before=True,
        decimal_sep=".",
        thousands_sep=",",
        vat_rate=0.18,
        vat_name="VAT",
        date_format="%d/%m/%Y",
        rtl=False,
        week_start=0,
        bcp47="rw-RW",
    ),
    # Senegal
    "SN": ExtendedLocale(
        currency_symbol="CFA",
        currency_before=False,
        decimal_sep=",",
        thousands_sep=" ",
        vat_rate=0.18,
        vat_name="TVA",
        date_format="%d/%m/%Y",
        rtl=False,
        week_start=0,
        bcp47="fr-SN",
    ),
    # Ivory Coast
    "CI": ExtendedLocale(
        currency_symbol="CFA",
        currency_before=False,
        decimal_sep=",",
        thousands_sep=" ",
        vat_rate=0.18,
        vat_name="TVA",
        date_format="%d/%m/%Y",
        rtl=False,
        week_start=0,
        bcp47="fr-CI",
    ),
    # Cameroon
    "CM": ExtendedLocale(
        currency_symbol="CFA",
        currency_before=False,
        decimal_sep=",",
        thousands_sep=" ",
        vat_rate=0.1925,
        vat_name="TVA",
        date_format="%d/%m/%Y",
        rtl=False,
        week_start=0,
        bcp47="fr-CM",
    ),
    # Zambia
    "ZM": ExtendedLocale(
        currency_symbol="K",
        currency_before=True,
        decimal_sep=".",
        thousands_sep=",",
        vat_rate=0.16,
        vat_name="VAT",
        date_format="%d/%m/%Y",
        rtl=False,
        week_start=0,
        bcp47="en-ZM",
    ),
    # Zimbabwe
    "ZW": ExtendedLocale(
        currency_symbol="ZiG",
        currency_before=True,
        decimal_sep=".",
        thousands_sep=",",
        vat_rate=0.15,
        vat_name="VAT",
        date_format="%d/%m/%Y",
        rtl=False,
        week_start=0,
        bcp47="en-ZW",
    ),
    # Mozambique
    "MZ": ExtendedLocale(
        currency_symbol="MT",
        currency_before=False,
        decimal_sep=",",
        thousands_sep=".",
        vat_rate=0.17,
        vat_name="IVA",
        date_format="%d/%m/%Y",
        rtl=False,
        week_start=0,
        bcp47="pt-MZ",
    ),
    # Angola
    "AO": ExtendedLocale(
        currency_symbol="Kz",
        currency_before=False,
        decimal_sep=",",
        thousands_sep=".",
        vat_rate=0.14,
        vat_name="IVA",
        date_format="%d/%m/%Y",
        rtl=False,
        week_start=0,
        bcp47="pt-AO",
    ),
    # Morocco
    "MA": ExtendedLocale(
        currency_symbol="MAD",
        currency_before=False,
        decimal_sep=",",
        thousands_sep=".",
        vat_rate=0.20,
        vat_name="TVA",
        date_format="%d/%m/%Y",
        rtl=True,
        week_start=0,
        bcp47="ar-MA",
    ),
    # Tunisia
    "TN": ExtendedLocale(
        currency_symbol="DT",
        currency_before=False,
        decimal_sep=",",
        thousands_sep=".",
        vat_rate=0.19,
        vat_name="TVA",
        date_format="%d/%m/%Y",
        rtl=True,
        week_start=0,
        bcp47="ar-TN",
    ),
    # Algeria
    "DZ": ExtendedLocale(
        currency_symbol="DA",
        currency_before=False,
        decimal_sep=",",
        thousands_sep=".",
        vat_rate=0.19,
        vat_name="TVA",
        date_format="%d/%m/%Y",
        rtl=True,
        week_start=6,
        bcp47="ar-DZ",
    ),
    # Botswana
    "BW": ExtendedLocale(
        currency_symbol="P",
        currency_before=True,
        decimal_sep=".",
        thousands_sep=",",
        vat_rate=0.12,
        vat_name="VAT",
        date_format="%d/%m/%Y",
        rtl=False,
        week_start=0,
        bcp47="en-BW",
    ),
    # Namibia
    "NA": ExtendedLocale(
        currency_symbol="N$",
        currency_before=True,
        decimal_sep=".",
        thousands_sep=" ",
        vat_rate=0.15,
        vat_name="VAT",
        date_format="%Y/%m/%d",
        rtl=False,
        week_start=0,
        bcp47="en-NA",
    ),
    # Malawi
    "MW": ExtendedLocale(
        currency_symbol="MK",
        currency_before=True,
        decimal_sep=".",
        thousands_sep=",",
        vat_rate=0.165,
        vat_name="VAT",
        date_format="%d/%m/%Y",
        rtl=False,
        week_start=0,
        bcp47="en-MW",
    ),
    # Madagascar
    "MG": ExtendedLocale(
        currency_symbol="Ar",
        currency_before=False,
        decimal_sep=",",
        thousands_sep=" ",
        vat_rate=0.20,
        vat_name="TVA",
        date_format="%d/%m/%Y",
        rtl=False,
        week_start=0,
        bcp47="mg-MG",
    ),
    # Democratic Republic of Congo
    "CD": ExtendedLocale(
        currency_symbol="FC",
        currency_before=True,
        decimal_sep=",",
        thousands_sep=".",
        vat_rate=0.16,
        vat_name="TVA",
        date_format="%d/%m/%Y",
        rtl=False,
        week_start=0,
        bcp47="fr-CD",
    ),
    # Sudan
    "SD": ExtendedLocale(
        currency_symbol="SDG",
        currency_before=True,
        decimal_sep=".",
        thousands_sep=",",
        vat_rate=0.17,
        vat_name="VAT",
        date_format="%d/%m/%Y",
        rtl=True,
        week_start=6,
        bcp47="ar-SD",
    ),
    # Libya
    "LY": ExtendedLocale(
        currency_symbol="LD",
        currency_before=True,
        decimal_sep=".",
        thousands_sep=",",
        vat_rate=0.0,
        vat_name="",
        date_format="%d/%m/%Y",
        rtl=True,
        week_start=6,
        bcp47="ar-LY",
    ),
    # ── Middle East ─────────────────────────────────────────────────────────
    # Saudi Arabia
    "SA": ExtendedLocale(
        currency_symbol="SR",
        currency_before=True,
        decimal_sep=".",
        thousands_sep=",",
        vat_rate=0.15,
        vat_name="VAT",
        date_format="%d/%m/%Y",
        rtl=True,
        week_start=0,
        bcp47="ar-SA",
    ),
    # United Arab Emirates
    "AE": ExtendedLocale(
        currency_symbol="AED",
        currency_before=True,
        decimal_sep=".",
        thousands_sep=",",
        vat_rate=0.05,
        vat_name="VAT",
        date_format="%d/%m/%Y",
        rtl=True,
        week_start=0,
        bcp47="ar-AE",
    ),
    # Qatar
    "QA": ExtendedLocale(
        currency_symbol="QR",
        currency_before=True,
        decimal_sep=".",
        thousands_sep=",",
        vat_rate=0.0,
        vat_name="",
        date_format="%d/%m/%Y",
        rtl=True,
        week_start=0,
        bcp47="ar-QA",
    ),
    # Kuwait
    "KW": ExtendedLocale(
        currency_symbol="KD",
        currency_before=True,
        decimal_sep=".",
        thousands_sep=",",
        vat_rate=0.0,
        vat_name="",
        date_format="%d/%m/%Y",
        rtl=True,
        week_start=0,
        bcp47="ar-KW",
    ),
    # Israel
    "IL": ExtendedLocale(
        currency_symbol="₪",
        currency_before=True,
        decimal_sep=".",
        thousands_sep=",",
        vat_rate=0.17,
        vat_name="מע״מ",
        date_format="%d/%m/%Y",
        rtl=True,
        week_start=0,
        bcp47="he-IL",
    ),
    # Turkey
    "TR": ExtendedLocale(
        currency_symbol="₺",
        currency_before=True,
        decimal_sep=",",
        thousands_sep=".",
        vat_rate=0.20,
        vat_name="KDV",
        date_format="%d.%m.%Y",
        rtl=False,
        week_start=0,
        bcp47="tr-TR",
    ),
    # ── Europe ──────────────────────────────────────────────────────────────
    # United Kingdom
    "GB": ExtendedLocale(
        currency_symbol="£",
        currency_before=True,
        decimal_sep=".",
        thousands_sep=",",
        vat_rate=0.20,
        vat_name="VAT",
        date_format="%d/%m/%Y",
        rtl=False,
        week_start=0,
        bcp47="en-GB",
    ),
    # Germany
    "DE": ExtendedLocale(
        currency_symbol="€",
        currency_before=False,
        decimal_sep=",",
        thousands_sep=".",
        vat_rate=0.19,
        vat_name="MwSt.",
        date_format="%d.%m.%Y",
        rtl=False,
        week_start=0,
        bcp47="de-DE",
    ),
    # France
    "FR": ExtendedLocale(
        currency_symbol="€",
        currency_before=False,
        decimal_sep=",",
        thousands_sep=" ",
        vat_rate=0.20,
        vat_name="TVA",
        date_format="%d/%m/%Y",
        rtl=False,
        week_start=0,
        bcp47="fr-FR",
    ),
    # Netherlands
    "NL": ExtendedLocale(
        currency_symbol="€",
        currency_before=True,
        decimal_sep=",",
        thousands_sep=".",
        vat_rate=0.21,
        vat_name="BTW",
        date_format="%d-%m-%Y",
        rtl=False,
        week_start=0,
        bcp47="nl-NL",
    ),
    # Sweden
    "SE": ExtendedLocale(
        currency_symbol="kr",
        currency_before=False,
        decimal_sep=",",
        thousands_sep=" ",
        vat_rate=0.25,
        vat_name="Moms",
        date_format="%Y-%m-%d",
        rtl=False,
        week_start=0,
        bcp47="sv-SE",
    ),
    # Spain
    "ES": ExtendedLocale(
        currency_symbol="€",
        currency_before=False,
        decimal_sep=",",
        thousands_sep=".",
        vat_rate=0.21,
        vat_name="IVA",
        date_format="%d/%m/%Y",
        rtl=False,
        week_start=0,
        bcp47="es-ES",
    ),
    # Portugal
    "PT": ExtendedLocale(
        currency_symbol="€",
        currency_before=False,
        decimal_sep=",",
        thousands_sep=".",
        vat_rate=0.23,
        vat_name="IVA",
        date_format="%d/%m/%Y",
        rtl=False,
        week_start=0,
        bcp47="pt-PT",
    ),
    # Poland
    "PL": ExtendedLocale(
        currency_symbol="zł",
        currency_before=False,
        decimal_sep=",",
        thousands_sep=" ",
        vat_rate=0.23,
        vat_name="VAT",
        date_format="%d.%m.%Y",
        rtl=False,
        week_start=0,
        bcp47="pl-PL",
    ),
    # ── Americas ─────────────────────────────────────────────────────────────
    # United States
    "US": ExtendedLocale(
        currency_symbol="$",
        currency_before=True,
        decimal_sep=".",
        thousands_sep=",",
        vat_rate=0.0,
        vat_name="",
        date_format="%m/%d/%Y",
        rtl=False,
        week_start=6,
        bcp47="en-US",
    ),
    # Canada
    "CA": ExtendedLocale(
        currency_symbol="CA$",
        currency_before=True,
        decimal_sep=".",
        thousands_sep=",",
        vat_rate=0.05,
        vat_name="GST",
        date_format="%Y-%m-%d",
        rtl=False,
        week_start=0,
        bcp47="en-CA",
    ),
    # Brazil
    "BR": ExtendedLocale(
        currency_symbol="R$",
        currency_before=True,
        decimal_sep=",",
        thousands_sep=".",
        vat_rate=0.0,
        vat_name="",
        date_format="%d/%m/%Y",
        rtl=False,
        week_start=0,
        bcp47="pt-BR",
    ),
    # Mexico
    "MX": ExtendedLocale(
        currency_symbol="MX$",
        currency_before=True,
        decimal_sep=".",
        thousands_sep=",",
        vat_rate=0.16,
        vat_name="IVA",
        date_format="%d/%m/%Y",
        rtl=False,
        week_start=0,
        bcp47="es-MX",
    ),
    # ── Asia-Pacific ─────────────────────────────────────────────────────────
    # India
    "IN": ExtendedLocale(
        currency_symbol="₹",
        currency_before=True,
        decimal_sep=".",
        thousands_sep=",",
        vat_rate=0.18,
        vat_name="GST",
        date_format="%d/%m/%Y",
        rtl=False,
        week_start=0,
        bcp47="en-IN",
    ),
    # China
    "CN": ExtendedLocale(
        currency_symbol="¥",
        currency_before=True,
        decimal_sep=".",
        thousands_sep=",",
        vat_rate=0.13,
        vat_name="增值税",
        date_format="%Y/%m/%d",
        rtl=False,
        week_start=0,
        bcp47="zh-CN",
    ),
    # Japan
    "JP": ExtendedLocale(
        currency_symbol="¥",
        currency_before=True,
        decimal_sep=".",
        thousands_sep=",",
        vat_rate=0.10,
        vat_name="消費税",
        date_format="%Y/%m/%d",
        rtl=False,
        week_start=0,
        bcp47="ja-JP",
    ),
    # Singapore
    "SG": ExtendedLocale(
        currency_symbol="S$",
        currency_before=True,
        decimal_sep=".",
        thousands_sep=",",
        vat_rate=0.09,
        vat_name="GST",
        date_format="%d/%m/%Y",
        rtl=False,
        week_start=0,
        bcp47="en-SG",
    ),
    # Indonesia
    "ID": ExtendedLocale(
        currency_symbol="Rp",
        currency_before=True,
        decimal_sep=",",
        thousands_sep=".",
        vat_rate=0.11,
        vat_name="PPN",
        date_format="%d/%m/%Y",
        rtl=False,
        week_start=0,
        bcp47="id-ID",
    ),
    # Australia
    "AU": ExtendedLocale(
        currency_symbol="A$",
        currency_before=True,
        decimal_sep=".",
        thousands_sep=",",
        vat_rate=0.10,
        vat_name="GST",
        date_format="%d/%m/%Y",
        rtl=False,
        week_start=0,
        bcp47="en-AU",
    ),
    # Pakistan
    "PK": ExtendedLocale(
        currency_symbol="₨",
        currency_before=True,
        decimal_sep=".",
        thousands_sep=",",
        vat_rate=0.17,
        vat_name="GST",
        date_format="%d/%m/%Y",
        rtl=True,
        week_start=0,
        bcp47="ur-PK",
    ),
    # Bangladesh
    "BD": ExtendedLocale(
        currency_symbol="৳",
        currency_before=True,
        decimal_sep=".",
        thousands_sep=",",
        vat_rate=0.15,
        vat_name="VAT",
        date_format="%d/%m/%Y",
        rtl=False,
        week_start=0,
        bcp47="bn-BD",
    ),
}

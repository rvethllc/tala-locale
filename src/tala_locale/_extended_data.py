"""
Extended locale data for tala-locale v3.0.0.

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
    languages : tuple[str, ...]
        All significant languages spoken in this country, as BCP 47 tags.
        Primary language is always first.  Includes minority, regional, and
        co-official languages that are relevant for business communications.
        e.g. Nigeria → ``("en-NG", "ha-NG", "yo-NG", "ig-NG", "pcm-NG")``,
        Morocco → ``("ar-MA", "fr-MA", "tzm-MA")``,
        South Africa → ``("en-ZA", "zu-ZA", "xh-ZA", "af-ZA", ...)``.
        Use this to detect which language a user is writing in, or to decide
        which language variants to offer in a UI.
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
    languages: tuple


# ---------------------------------------------------------------------------
# EXTENDED_LOCALE_MAP
# ---------------------------------------------------------------------------
# Key: ISO 3166-1 alpha-2 country code (uppercase, 2 chars)
# Value: ExtendedLocale
#
# Coverage: All 191 countries from _data.py
# ---------------------------------------------------------------------------

EXTENDED_LOCALE_MAP: dict[str, ExtendedLocale] = {
    # fmt: off
    # ── West Africa ──────────────────────────────────────────────────────────
    # Nigeria: English (official/business) + Hausa + Yoruba + Igbo + Nigerian Pidgin
    "NG": ExtendedLocale("₦", True, ".", ",", 0.075, "VAT", "%d/%m/%Y", False, 0, "en-NG",
        ("en-NG", "ha-NG", "yo-NG", "ig-NG", "pcm-NG")),
    # Ghana: English + Twi (Akan) + Ewe + Ga + Dagbani
    "GH": ExtendedLocale("₵", True, ".", ",", 0.15, "VAT", "%d/%m/%Y", False, 0, "en-GH",
        ("en-GH", "ak-GH", "ee-GH", "gaa-GH")),
    # Senegal: French (official) + Wolof (lingua franca) + Pulaar + Serer
    "SN": ExtendedLocale("CFA", False, ",", " ", 0.18, "TVA", "%d/%m/%Y", False, 0, "fr-SN",
        ("fr-SN", "wo-SN", "ff-SN")),
    # Côte d'Ivoire: French + Dioula (trade lingua franca)
    "CI": ExtendedLocale("CFA", False, ",", " ", 0.18, "TVA", "%d/%m/%Y", False, 0, "fr-CI",
        ("fr-CI", "dyu-CI")),
    # Burkina Faso: French + Mooré + Dioula
    "BF": ExtendedLocale("CFA", False, ",", " ", 0.18, "TVA", "%d/%m/%Y", False, 0, "fr-BF",
        ("fr-BF", "mos-BF", "dyu-BF")),
    # Niger: French + Hausa + Zarma
    "NE": ExtendedLocale("CFA", False, ",", " ", 0.19, "TVA", "%d/%m/%Y", False, 0, "fr-NE",
        ("fr-NE", "ha-NE", "dje-NE")),
    # Togo: French + Ewe + Kabiyé
    "TG": ExtendedLocale("CFA", False, ",", " ", 0.18, "TVA", "%d/%m/%Y", False, 0, "fr-TG",
        ("fr-TG", "ee-TG", "kbp-TG")),
    # Benin: French + Fon + Yoruba
    "BJ": ExtendedLocale("CFA", False, ",", " ", 0.18, "TVA", "%d/%m/%Y", False, 0, "fr-BJ",
        ("fr-BJ", "fon-BJ", "yo-BJ")),
    # Liberia: English only primary
    "LR": ExtendedLocale("L$", True, ".", ",", 0.10, "GST", "%d/%m/%Y", False, 0, "en-LR",
        ("en-LR",)),
    # Sierra Leone: English + Krio (Creole lingua franca)
    "SL": ExtendedLocale("Le", True, ".", ",", 0.15, "GST", "%d/%m/%Y", False, 0, "en-SL",
        ("en-SL", "kri-SL")),
    # Gambia: English only primary
    "GM": ExtendedLocale("D", True, ".", ",", 0.15, "VAT", "%d/%m/%Y", False, 0, "en-GM",
        ("en-GM", "wo-GM")),
    # Mali: French + Bambara (lingua franca)
    "ML": ExtendedLocale("CFA", False, ",", " ", 0.18, "TVA", "%d/%m/%Y", False, 0, "fr-ML",
        ("fr-ML", "bm-ML")),
    # Guinea: French + Pulaar + Mandinka + Susu
    "GN": ExtendedLocale("FG", True, ",", " ", 0.18, "TVA", "%d/%m/%Y", False, 0, "fr-GN",
        ("fr-GN", "ff-GN", "man-GN", "sus-GN")),
    # Guinea-Bissau: Portuguese + Creole (Crioulo)
    "GW": ExtendedLocale("CFA", False, ",", " ", 0.17, "TVA", "%d/%m/%Y", False, 0, "pt-GW",
        ("pt-GW", "pov-GW")),
    # Cape Verde: Portuguese + Cape Verdean Creole
    "CV": ExtendedLocale("$", True, ",", ".", 0.15, "IVA", "%d/%m/%Y", False, 0, "pt-CV",
        ("pt-CV", "kea-CV")),
    # Mauritania: Arabic + French + Pulaar
    "MR": ExtendedLocale("UM", True, ",", " ", 0.16, "TVA", "%d/%m/%Y", True, 0, "ar-MR",
        ("ar-MR", "fr-MR", "ff-MR")),
    # ── East Africa ──────────────────────────────────────────────────────────
    # Kenya: Swahili (national) + English (official/business) + Kikuyu + Luo
    "KE": ExtendedLocale("KSh", True, ".", ",", 0.16, "VAT", "%d/%m/%Y", False, 0, "sw-KE",
        ("sw-KE", "en-KE", "ki-KE", "luo-KE")),
    # Tanzania: Swahili (dominant) + English
    "TZ": ExtendedLocale("TSh", True, ".", ",", 0.18, "VAT", "%d/%m/%Y", False, 0, "sw-TZ",
        ("sw-TZ", "en-TZ")),
    # Uganda: English + Luganda + Swahili
    "UG": ExtendedLocale("USh", True, ".", ",", 0.18, "VAT", "%d/%m/%Y", False, 0, "en-UG",
        ("en-UG", "lg-UG", "sw-UG")),
    # Rwanda: Kinyarwanda + French + English
    "RW": ExtendedLocale("RF", True, ".", ",", 0.18, "VAT", "%d/%m/%Y", False, 0, "rw-RW",
        ("rw-RW", "en-RW", "fr-RW")),
    # Burundi: French + Kirundi + English
    "BI": ExtendedLocale("Fr", True, ",", ".", 0.18, "TVA", "%d/%m/%Y", False, 0, "fr-BI",
        ("fr-BI", "rn-BI", "en-BI")),
    # Ethiopia: Amharic (official) + Oromo + Somali + Tigrinya
    "ET": ExtendedLocale("Br", True, ".", ",", 0.15, "VAT", "%d/%m/%Y", False, 0, "am-ET",
        ("am-ET", "om-ET", "so-ET", "ti-ET")),
    # Somalia: Somali + Arabic
    "SO": ExtendedLocale("Sh.So.", True, ".", ",", 0.0, "", "%d/%m/%Y", False, 0, "so-SO",
        ("so-SO", "ar-SO")),
    # Djibouti: French + Arabic + Somali + Afar
    "DJ": ExtendedLocale("Fr", True, ",", " ", 0.10, "TVA", "%d/%m/%Y", False, 0, "fr-DJ",
        ("fr-DJ", "ar-DJ", "so-DJ", "aa-DJ")),
    # Eritrea: Tigrinya + Arabic + English
    "ER": ExtendedLocale("Nfk", True, ".", ",", 0.0, "", "%d/%m/%Y", False, 0, "ti-ER",
        ("ti-ER", "ar-ER", "en-ER")),
    # South Sudan: English + Dinka + Nuer + Arabic
    "SS": ExtendedLocale("SSP", True, ".", ",", 0.18, "VAT", "%d/%m/%Y", False, 0, "en-SS",
        ("en-SS", "din-SS", "nus-SS", "ar-SS")),
    # ── North Africa ─────────────────────────────────────────────────────────
    # Egypt: Arabic (Egyptian dialect, ar-EG — distinct from Gulf MSA)
    "EG": ExtendedLocale("E£", True, ".", ",", 0.14, "VAT", "%d/%m/%Y", True, 6, "ar-EG",
        ("ar-EG", "en-EG")),
    # Morocco: Moroccan Arabic/Darija (ar-MA) + French (heavily used in business) + Tamazight/Berber
    "MA": ExtendedLocale("MAD", False, ",", ".", 0.20, "TVA", "%d/%m/%Y", True, 0, "ar-MA",
        ("ar-MA", "fr-MA", "tzm-MA", "zgh-MA")),
    # Algeria: Algerian Arabic/Darja + French + Kabyle Berber
    "DZ": ExtendedLocale("DA", False, ",", ".", 0.19, "TVA", "%d/%m/%Y", True, 6, "ar-DZ",
        ("ar-DZ", "fr-DZ", "kab-DZ")),
    # Tunisia: Tunisian Arabic + French
    "TN": ExtendedLocale("DT", False, ",", ".", 0.19, "TVA", "%d/%m/%Y", True, 0, "ar-TN",
        ("ar-TN", "fr-TN")),
    # Libya: Libyan Arabic (distinct dialect, ar-LY) — minimal French unlike Maghreb
    "LY": ExtendedLocale("LD", True, ".", ",", 0.0, "", "%d/%m/%Y", True, 6, "ar-LY",
        ("ar-LY",)),
    # Sudan: Sudanese Arabic + Nile Nubian + Beja
    "SD": ExtendedLocale("SDG", True, ".", ",", 0.17, "VAT", "%d/%m/%Y", True, 6, "ar-SD",
        ("ar-SD", "en-SD")),
    # ── Southern Africa ──────────────────────────────────────────────────────
    # South Africa: 11 official languages — English + Zulu + Xhosa + Afrikaans + more
    "ZA": ExtendedLocale("R", True, ".", " ", 0.15, "VAT", "%Y/%m/%d", False, 0, "en-ZA",
        ("en-ZA", "zu-ZA", "xh-ZA", "af-ZA", "nso-ZA", "tn-ZA", "st-ZA", "ts-ZA", "ss-ZA", "ve-ZA", "nr-ZA")),
    # Zambia: English + Bemba + Nyanja + Tonga
    "ZM": ExtendedLocale("K", True, ".", ",", 0.16, "VAT", "%d/%m/%Y", False, 0, "en-ZM",
        ("en-ZM", "bem-ZM", "ny-ZM", "toi-ZM")),
    # Zimbabwe: English + Shona + Ndebele
    "ZW": ExtendedLocale("ZiG", True, ".", ",", 0.15, "VAT", "%d/%m/%Y", False, 0, "en-ZW",
        ("en-ZW", "sn-ZW", "nd-ZW")),
    # Botswana: English + Tswana
    "BW": ExtendedLocale("P", True, ".", ",", 0.12, "VAT", "%d/%m/%Y", False, 0, "en-BW",
        ("en-BW", "tn-BW")),
    # Lesotho: Sotho + English
    "LS": ExtendedLocale("M", True, ".", ",", 0.15, "VAT", "%d/%m/%Y", False, 0, "en-LS",
        ("en-LS", "st-LS")),
    # Eswatini: Swati + English
    "SZ": ExtendedLocale("E", True, ".", ",", 0.15, "VAT", "%d/%m/%Y", False, 0, "en-SZ",
        ("en-SZ", "ss-SZ")),
    # Namibia: English + Afrikaans + Oshiwambo + German
    "NA": ExtendedLocale("N$", True, ".", " ", 0.15, "VAT", "%Y/%m/%d", False, 0, "en-NA",
        ("en-NA", "af-NA", "kj-NA", "de-NA")),
    # Malawi: English + Chichewa
    "MW": ExtendedLocale("MK", True, ".", ",", 0.165, "VAT", "%d/%m/%Y", False, 0, "en-MW",
        ("en-MW", "ny-MW")),
    # Mozambique: Portuguese + Makhuwa + Tsonga + Sena
    "MZ": ExtendedLocale("MT", False, ",", ".", 0.17, "IVA", "%d/%m/%Y", False, 0, "pt-MZ",
        ("pt-MZ", "vmw-MZ", "ts-MZ", "seh-MZ")),
    # ── Central Africa ───────────────────────────────────────────────────────
    # Cameroon: French + English (official bilingual) + Fulfulde + Ewondo + Camfranglais
    "CM": ExtendedLocale("CFA", False, ",", " ", 0.1925, "TVA", "%d/%m/%Y", False, 0, "fr-CM",
        ("fr-CM", "en-CM", "ff-CM")),
    # Central African Republic: French + Sango (national lingua franca)
    "CF": ExtendedLocale("CFA", False, ",", " ", 0.19, "TVA", "%d/%m/%Y", False, 0, "fr-CF",
        ("fr-CF", "sg-CF")),
    # Chad: French + Arabic + Sara
    "TD": ExtendedLocale("CFA", False, ",", " ", 0.18, "TVA", "%d/%m/%Y", False, 0, "fr-TD",
        ("fr-TD", "ar-TD")),
    # Gabon: French only dominant
    "GA": ExtendedLocale("CFA", False, ",", " ", 0.18, "TVA", "%d/%m/%Y", False, 0, "fr-GA",
        ("fr-GA",)),
    # Republic of Congo: French + Lingala + Kituba
    "CG": ExtendedLocale("CFA", False, ",", " ", 0.18, "TVA", "%d/%m/%Y", False, 0, "fr-CG",
        ("fr-CG", "ln-CG")),
    # DRC: French + Lingala + Swahili + Kikongo + Tshiluba
    "CD": ExtendedLocale("FC", True, ",", ".", 0.16, "TVA", "%d/%m/%Y", False, 0, "fr-CD",
        ("fr-CD", "ln-CD", "sw-CD", "kg-CD", "lua-CD")),
    # Angola: Portuguese + Umbundu + Kimbundu + Kikongo
    "AO": ExtendedLocale("Kz", False, ",", ".", 0.14, "IVA", "%d/%m/%Y", False, 0, "pt-AO",
        ("pt-AO", "umb-AO", "kmb-AO", "kg-AO")),
    # Equatorial Guinea: Spanish + French + Portuguese
    "GQ": ExtendedLocale("CFA", False, ",", " ", 0.15, "IVA", "%d/%m/%Y", False, 0, "es-GQ",
        ("es-GQ", "fr-GQ", "pt-GQ")),
    # São Tomé: Portuguese only
    "ST": ExtendedLocale("Db", True, ",", ".", 0.0, "", "%d/%m/%Y", False, 0, "pt-ST",
        ("pt-ST",)),
    # ── Indian Ocean ─────────────────────────────────────────────────────────
    # Madagascar: Malagasy + French
    "MG": ExtendedLocale("Ar", False, ",", " ", 0.20, "TVA", "%d/%m/%Y", False, 0, "mg-MG",
        ("mg-MG", "fr-MG")),
    # Mauritius: English (official/business) + Mauritian Creole + French
    "MU": ExtendedLocale("₨", True, ".", ",", 0.15, "VAT", "%d/%m/%Y", False, 0, "en-MU",
        ("en-MU", "mfe-MU", "fr-MU")),
    # Seychelles: English + French + Seychellois Creole
    "SC": ExtendedLocale("SR", True, ".", ",", 0.15, "VAT", "%d/%m/%Y", False, 0, "en-SC",
        ("en-SC", "fr-SC", "crs-SC")),
    # Comoros: Arabic + Comorian + French
    "KM": ExtendedLocale("CF", True, ",", " ", 0.10, "TVA", "%d/%m/%Y", True, 0, "ar-KM",
        ("ar-KM", "wni-KM", "fr-KM")),
    # ── Western Europe ───────────────────────────────────────────────────────
    # UK: English — but en-GB is meaningfully different from en-US/en-AU/en-CA
    "GB": ExtendedLocale("£", True, ".", ",", 0.20, "VAT", "%d/%m/%Y", False, 0, "en-GB",
        ("en-GB", "cy-GB", "gd-GB")),
    # France: French — fr-FR is different from fr-CA, fr-BE, fr-CH
    "FR": ExtendedLocale("€", False, ",", " ", 0.20, "TVA", "%d/%m/%Y", False, 0, "fr-FR",
        ("fr-FR",)),
    # Germany: German
    "DE": ExtendedLocale("€", False, ",", ".", 0.19, "MwSt.", "%d.%m.%Y", False, 0, "de-DE",
        ("de-DE",)),
    # Netherlands: Dutch + Frisian
    "NL": ExtendedLocale("€", True, ",", ".", 0.21, "BTW", "%d-%m-%Y", False, 0, "nl-NL",
        ("nl-NL", "fy-NL")),
    # Spain: Spanish + Catalan + Basque + Galician
    "ES": ExtendedLocale("€", False, ",", ".", 0.21, "IVA", "%d/%m/%Y", False, 0, "es-ES",
        ("es-ES", "ca-ES", "eu-ES", "gl-ES")),
    # Italy: Italian
    "IT": ExtendedLocale("€", False, ",", ".", 0.22, "IVA", "%d/%m/%Y", False, 0, "it-IT",
        ("it-IT",)),
    # Switzerland: German + French + Italian + Romansh (four official)
    "CH": ExtendedLocale("CHF", True, ".", "'", 0.081, "MWST", "%d.%m.%Y", False, 0, "de-CH",
        ("de-CH", "fr-CH", "it-CH", "rm-CH")),
    # Austria: German
    "AT": ExtendedLocale("€", False, ",", ".", 0.20, "MwSt.", "%d.%m.%Y", False, 0, "de-AT",
        ("de-AT",)),
    # Belgium: French + Dutch/Flemish + German (three official)
    "BE": ExtendedLocale("€", False, ",", ".", 0.21, "TVA/BTW", "%d/%m/%Y", False, 0, "fr-BE",
        ("fr-BE", "nl-BE", "de-BE")),
    # Portugal
    "PT": ExtendedLocale("€", False, ",", ".", 0.23, "IVA", "%d/%m/%Y", False, 0, "pt-PT",
        ("pt-PT",)),
    # Ireland: English + Irish (Gaelic)
    "IE": ExtendedLocale("€", True, ".", ",", 0.23, "VAT", "%d/%m/%Y", False, 0, "en-IE",
        ("en-IE", "ga-IE")),
    # Luxembourg: French + German + Luxembourgish
    "LU": ExtendedLocale("€", False, ",", ".", 0.17, "TVA", "%d/%m/%Y", False, 0, "fr-LU",
        ("fr-LU", "de-LU", "lb-LU")),
    # Andorra: Catalan + Spanish + French
    "AD": ExtendedLocale("€", True, ",", ".", 0.045, "IGI", "%d/%m/%Y", False, 0, "ca-AD",
        ("ca-AD", "es-AD", "fr-AD")),
    # Monaco: French
    "MC": ExtendedLocale("€", False, ",", " ", 0.20, "TVA", "%d/%m/%Y", False, 0, "fr-MC",
        ("fr-MC",)),
    # San Marino: Italian
    "SM": ExtendedLocale("€", False, ",", ".", 0.0, "", "%d/%m/%Y", False, 0, "it-SM",
        ("it-SM",)),
    # Vatican: Italian + Latin
    "VA": ExtendedLocale("€", False, ",", ".", 0.0, "", "%d/%m/%Y", False, 0, "it-VA",
        ("it-VA", "la-VA")),
    # Liechtenstein: German
    "LI": ExtendedLocale("CHF", True, ".", "'", 0.081, "MWST", "%d.%m.%Y", False, 0, "de-LI",
        ("de-LI",)),
    # ── Northern Europe ──────────────────────────────────────────────────────
    "SE": ExtendedLocale("kr", False, ",", " ", 0.25, "Moms", "%Y-%m-%d", False, 0, "sv-SE",
        ("sv-SE",)),
    # Norway: Norwegian Bokmål + Nynorsk + Northern Sami
    "NO": ExtendedLocale("kr", True, ",", " ", 0.25, "MVA", "%d.%m.%Y", False, 0, "nb-NO",
        ("nb-NO", "nn-NO", "se-NO")),
    # Denmark: Danish + Greenlandic + German (South Jutland)
    "DK": ExtendedLocale("kr", True, ",", ".", 0.25, "Moms", "%d/%m/%Y", False, 0, "da-DK",
        ("da-DK",)),
    # Finland: Finnish + Swedish (both official)
    "FI": ExtendedLocale("€", False, ",", " ", 0.255, "ALV", "%d.%m.%Y", False, 0, "fi-FI",
        ("fi-FI", "sv-FI")),
    # Iceland
    "IS": ExtendedLocale("kr", False, ",", ".", 0.24, "VSK", "%d/%m/%Y", False, 0, "is-IS",
        ("is-IS",)),
    # Faroe Islands: Faroese + Danish
    "FO": ExtendedLocale("kr", True, ",", ".", 0.25, "MVG", "%d/%m/%Y", False, 0, "fo-FO",
        ("fo-FO", "da-FO")),
    # Greenland: Greenlandic/Kalaallisut + Danish
    "GL": ExtendedLocale("kr", True, ",", ".", 0.0, "", "%d/%m/%Y", False, 0, "kl-GL",
        ("kl-GL", "da-GL")),
    # ── Southern Europe ──────────────────────────────────────────────────────
    # Greece: Greek
    "GR": ExtendedLocale("€", False, ",", ".", 0.24, "ΦΠΑ", "%d/%m/%Y", False, 0, "el-GR",
        ("el-GR",)),
    # Cyprus: Greek + Turkish (both official)
    "CY": ExtendedLocale("€", True, ".", ",", 0.19, "ΦΠΑ", "%d/%m/%Y", False, 0, "el-CY",
        ("el-CY", "tr-CY")),
    # Malta: Maltese + English
    "MT": ExtendedLocale("€", True, ".", ",", 0.18, "VAT", "%d/%m/%Y", False, 0, "mt-MT",
        ("mt-MT", "en-MT")),
    # ── Eastern Europe ───────────────────────────────────────────────────────
    "RU": ExtendedLocale("₽", False, ",", " ", 0.20, "НДС", "%d.%m.%Y", False, 0, "ru-RU",
        ("ru-RU",)),
    # Ukraine: Ukrainian + Russian
    "UA": ExtendedLocale("₴", False, ",", " ", 0.20, "ПДВ", "%d.%m.%Y", False, 0, "uk-UA",
        ("uk-UA", "ru-UA")),
    "PL": ExtendedLocale("zł", False, ",", " ", 0.23, "VAT", "%d.%m.%Y", False, 0, "pl-PL",
        ("pl-PL",)),
    "HU": ExtendedLocale("Ft", False, ",", " ", 0.27, "ÁFA", "%Y.%m.%d", False, 0, "hu-HU",
        ("hu-HU",)),
    "CZ": ExtendedLocale("Kč", False, ",", " ", 0.21, "DPH", "%d.%m.%Y", False, 0, "cs-CZ",
        ("cs-CZ", "sk-CZ")),
    "SK": ExtendedLocale("€", False, ",", " ", 0.23, "DPH", "%d.%m.%Y", False, 0, "sk-SK",
        ("sk-SK", "cs-SK", "hu-SK")),
    "RO": ExtendedLocale("lei", False, ",", ".", 0.19, "TVA", "%d.%m.%Y", False, 0, "ro-RO",
        ("ro-RO", "hu-RO")),
    "BG": ExtendedLocale("лв", False, ",", " ", 0.20, "ДДС", "%d.%m.%Y", False, 0, "bg-BG",
        ("bg-BG",)),
    "LT": ExtendedLocale("€", False, ",", " ", 0.21, "PVM", "%Y-%m-%d", False, 0, "lt-LT",
        ("lt-LT",)),
    "LV": ExtendedLocale("€", False, ",", " ", 0.21, "PVN", "%d.%m.%Y", False, 0, "lv-LV",
        ("lv-LV", "ru-LV")),
    "EE": ExtendedLocale("€", False, ",", " ", 0.22, "KM", "%d.%m.%Y", False, 0, "et-EE",
        ("et-EE", "ru-EE")),
    # Belarus: Belarusian + Russian (both official)
    "BY": ExtendedLocale("Br", False, ",", " ", 0.20, "НДС", "%d.%m.%Y", False, 0, "be-BY",
        ("be-BY", "ru-BY")),
    # Moldova: Romanian + Russian
    "MD": ExtendedLocale("L", False, ",", ".", 0.20, "TVA", "%d.%m.%Y", False, 0, "ro-MD",
        ("ro-MD", "ru-MD")),
    "SI": ExtendedLocale("€", False, ",", ".", 0.22, "DDV", "%d.%m.%Y", False, 0, "sl-SI",
        ("sl-SI",)),
    "HR": ExtendedLocale("€", False, ",", ".", 0.25, "PDV", "%d.%m.%Y", False, 0, "hr-HR",
        ("hr-HR",)),
    # Bosnia: Bosnian + Serbian + Croatian (all three official, mutually intelligible)
    "BA": ExtendedLocale("KM", False, ",", ".", 0.17, "PDV", "%d.%m.%Y", False, 0, "bs-BA",
        ("bs-BA", "sr-BA", "hr-BA")),
    # Serbia: Serbian + Hungarian (Vojvodina)
    "RS": ExtendedLocale("RSD", False, ",", ".", 0.20, "PDV", "%d.%m.%Y", False, 0, "sr-RS",
        ("sr-RS", "hu-RS")),
    "ME": ExtendedLocale("€", False, ",", ".", 0.21, "PDV", "%d.%m.%Y", False, 0, "sr-ME",
        ("sr-ME", "sq-ME")),
    # Kosovo: Albanian + Serbian (both official)
    "XK": ExtendedLocale("€", True, ",", ".", 0.18, "TVSH", "%d.%m.%Y", False, 0, "sq-XK",
        ("sq-XK", "sr-XK")),
    # North Macedonia: Macedonian + Albanian
    "MK": ExtendedLocale("den", False, ",", ".", 0.18, "ДДВ", "%d.%m.%Y", False, 0, "mk-MK",
        ("mk-MK", "sq-MK")),
    "AL": ExtendedLocale("L", False, ",", ".", 0.20, "TVSH", "%d.%m.%Y", False, 0, "sq-AL",
        ("sq-AL",)),
    # ── Middle East ──────────────────────────────────────────────────────────
    # UAE: Gulf Arabic (ar-AE) + English widely used in business
    "AE": ExtendedLocale("AED", True, ".", ",", 0.05, "VAT", "%d/%m/%Y", True, 0, "ar-AE",
        ("ar-AE", "en-AE")),
    # Saudi Arabia: Gulf Arabic (ar-SA) — formal MSA in business + colloquial Najdi/Hejazi
    "SA": ExtendedLocale("SR", True, ".", ",", 0.15, "VAT", "%d/%m/%Y", True, 0, "ar-SA",
        ("ar-SA", "en-SA")),
    # Oman: Omani Arabic
    "OM": ExtendedLocale("﷼", True, ".", ",", 0.05, "VAT", "%d/%m/%Y", True, 0, "ar-OM",
        ("ar-OM", "en-OM")),
    # Qatar: Qatari Arabic
    "QA": ExtendedLocale("QR", True, ".", ",", 0.0, "", "%d/%m/%Y", True, 0, "ar-QA",
        ("ar-QA", "en-QA")),
    # Bahrain
    "BH": ExtendedLocale("BD", True, ".", ",", 0.10, "VAT", "%d/%m/%Y", True, 0, "ar-BH",
        ("ar-BH", "en-BH")),
    # Yemen: Yemeni Arabic
    "YE": ExtendedLocale("﷼", True, ".", ",", 0.0, "", "%d/%m/%Y", True, 6, "ar-YE",
        ("ar-YE",)),
    # Kuwait
    "KW": ExtendedLocale("KD", True, ".", ",", 0.0, "", "%d/%m/%Y", True, 0, "ar-KW",
        ("ar-KW", "en-KW")),
    # Jordan: Levantine Arabic (ar-JO) — distinct from Gulf Arabic
    "JO": ExtendedLocale("JD", True, ".", ",", 0.16, "GST", "%d/%m/%Y", True, 0, "ar-JO",
        ("ar-JO", "en-JO")),
    # Lebanon: Lebanese Arabic + French + English — genuinely trilingual in business
    "LB": ExtendedLocale("LL", True, ",", ".", 0.11, "TVA", "%d/%m/%Y", True, 0, "ar-LB",
        ("ar-LB", "fr-LB", "en-LB")),
    # Syria: Levantine Arabic
    "SY": ExtendedLocale("£S", True, ",", ".", 0.0, "", "%d/%m/%Y", True, 6, "ar-SY",
        ("ar-SY",)),
    # Israel: Hebrew + Arabic (both official) + Russian (large community)
    "IL": ExtendedLocale("₪", True, ".", ",", 0.17, "מע״מ", "%d/%m/%Y", True, 0, "he-IL",
        ("he-IL", "ar-IL", "ru-IL", "en-IL")),
    # Iraq: Iraqi Arabic (ar-IQ) + Kurdish
    "IQ": ExtendedLocale("ID", True, ",", ".", 0.0, "", "%d/%m/%Y", True, 6, "ar-IQ",
        ("ar-IQ", "ku-IQ")),
    # Iran: Persian/Farsi — not Arabic at all, different script and language family
    "IR": ExtendedLocale("﷼", True, ",", ".", 0.09, "ارزش افزوده", "%Y/%m/%d", True, 6, "fa-IR",
        ("fa-IR", "az-IR", "ku-IR")),
    # Turkey: Turkish — not Arabic, not Indo-European
    "TR": ExtendedLocale("₺", True, ",", ".", 0.20, "KDV", "%d.%m.%Y", False, 0, "tr-TR",
        ("tr-TR", "ku-TR")),
    # ── South Asia ───────────────────────────────────────────────────────────
    # India: English (official/business) + Hindi + Bengali + Telugu + Marathi + Tamil + more
    "IN": ExtendedLocale("₹", True, ".", ",", 0.18, "GST", "%d/%m/%Y", False, 0, "en-IN",
        ("en-IN", "hi-IN", "bn-IN", "te-IN", "mr-IN", "ta-IN", "ur-IN", "gu-IN", "kn-IN", "ml-IN", "pa-IN")),
    # Pakistan: Urdu (national) + English + Punjabi + Sindhi + Pashto
    "PK": ExtendedLocale("₨", True, ".", ",", 0.17, "GST", "%d/%m/%Y", True, 0, "ur-PK",
        ("ur-PK", "en-PK", "pa-PK", "sd-PK", "ps-PK")),
    # Bangladesh: Bengali
    "BD": ExtendedLocale("৳", True, ".", ",", 0.15, "VAT", "%d/%m/%Y", False, 0, "bn-BD",
        ("bn-BD", "en-BD")),
    # Sri Lanka: Sinhala + Tamil + English
    "LK": ExtendedLocale("Rs", True, ".", ",", 0.18, "VAT", "%d/%m/%Y", False, 0, "si-LK",
        ("si-LK", "ta-LK", "en-LK")),
    # Nepal: Nepali + Maithili + Bhojpuri
    "NP": ExtendedLocale("₨", True, ".", ",", 0.13, "VAT", "%d/%m/%Y", False, 0, "ne-NP",
        ("ne-NP", "mai-NP")),
    # Afghanistan: Pashto + Dari/Afghan Persian
    "AF": ExtendedLocale("Af", True, ",", ".", 0.0, "", "%d/%m/%Y", True, 6, "ps-AF",
        ("ps-AF", "fa-AF")),
    # ── East Asia ────────────────────────────────────────────────────────────
    # China: Mandarin Chinese — zh-CN is Simplified Chinese (mainland)
    "CN": ExtendedLocale("¥", True, ".", ",", 0.13, "增值税", "%Y/%m/%d", False, 0, "zh-CN",
        ("zh-CN",)),
    # Japan
    "JP": ExtendedLocale("¥", True, ".", ",", 0.10, "消費税", "%Y/%m/%d", False, 0, "ja-JP",
        ("ja-JP",)),
    # South Korea
    "KR": ExtendedLocale("₩", True, ".", ",", 0.10, "부가가치세", "%Y.%m.%d", False, 0, "ko-KR",
        ("ko-KR",)),
    # Hong Kong: Traditional Chinese (zh-HK) + English — genuinely bilingual in business
    "HK": ExtendedLocale("HK$", True, ".", ",", 0.0, "", "%d/%m/%Y", False, 0, "zh-HK",
        ("zh-HK", "en-HK")),
    # Macao: Traditional Chinese + Portuguese + Cantonese
    "MO": ExtendedLocale("P", True, ".", ",", 0.0, "", "%d/%m/%Y", False, 0, "zh-MO",
        ("zh-MO", "pt-MO")),
    # Taiwan: Traditional Chinese (zh-TW) — different from zh-CN
    "TW": ExtendedLocale("NT$", True, ".", ",", 0.05, "營業稅", "%Y/%m/%d", False, 0, "zh-TW",
        ("zh-TW",)),
    "MN": ExtendedLocale("₮", True, ",", " ", 0.10, "VAT", "%Y-%m-%d", False, 0, "mn-MN",
        ("mn-MN", "ru-MN")),
    "KP": ExtendedLocale("₩", True, ".", ",", 0.0, "", "%Y-%m-%d", False, 0, "ko-KP",
        ("ko-KP",)),
    # ── Southeast Asia ───────────────────────────────────────────────────────
    # Singapore: English (official/business) + Mandarin + Malay + Tamil — 4 official
    "SG": ExtendedLocale("S$", True, ".", ",", 0.09, "GST", "%d/%m/%Y", False, 0, "en-SG",
        ("en-SG", "zh-SG", "ms-SG", "ta-SG")),
    # Malaysia: Malay + English + Chinese (Mandarin/Cantonese) + Tamil
    "MY": ExtendedLocale("RM", True, ".", ",", 0.08, "SST", "%d/%m/%Y", False, 0, "ms-MY",
        ("ms-MY", "en-MY", "zh-MY", "ta-MY")),
    "TH": ExtendedLocale("฿", True, ".", ",", 0.07, "VAT", "%d/%m/%Y", False, 0, "th-TH",
        ("th-TH", "en-TH")),
    # Indonesia: Indonesian (official) + Javanese + Sundanese
    "ID": ExtendedLocale("Rp", True, ",", ".", 0.11, "PPN", "%d/%m/%Y", False, 0, "id-ID",
        ("id-ID", "jv-ID", "su-ID")),
    # Philippines: Filipino/Tagalog + English (both official) + Cebuano + Ilocano
    "PH": ExtendedLocale("₱", True, ".", ",", 0.12, "VAT", "%m/%d/%Y", False, 6, "en-PH",
        ("en-PH", "fil-PH", "ceb-PH")),
    "VN": ExtendedLocale("₫", False, ",", ".", 0.10, "VAT", "%d/%m/%Y", False, 0, "vi-VN",
        ("vi-VN",)),
    # Myanmar: Burmese + English
    "MM": ExtendedLocale("K", True, ".", ",", 0.05, "CT", "%d/%m/%Y", False, 0, "my-MM",
        ("my-MM", "en-MM")),
    "KH": ExtendedLocale("៛", False, ",", ".", 0.10, "VAT", "%d/%m/%Y", False, 0, "km-KH",
        ("km-KH", "en-KH")),
    "LA": ExtendedLocale("₭", True, ",", ".", 0.10, "VAT", "%d/%m/%Y", False, 0, "lo-LA",
        ("lo-LA",)),
    # ── Central Asia ─────────────────────────────────────────────────────────
    # Kazakhstan: Kazakh + Russian (both official)
    "KZ": ExtendedLocale("₸", False, ",", " ", 0.12, "ҚҚС", "%d.%m.%Y", False, 0, "kk-KZ",
        ("kk-KZ", "ru-KZ")),
    "TM": ExtendedLocale("T", True, ",", " ", 0.15, "VAT", "%d.%m.%Y", False, 0, "tk-TM",
        ("tk-TM", "ru-TM")),
    "TJ": ExtendedLocale("SM", True, ",", " ", 0.18, "VAT", "%d.%m.%Y", False, 0, "tg-TJ",
        ("tg-TJ", "ru-TJ")),
    # Kyrgyzstan: Kyrgyz + Russian (both official)
    "KG": ExtendedLocale("с", False, ",", " ", 0.12, "НДС", "%d.%m.%Y", False, 0, "ky-KG",
        ("ky-KG", "ru-KG")),
    # Uzbekistan: Uzbek + Russian
    "UZ": ExtendedLocale("сўм", False, ",", " ", 0.12, "QQS", "%d.%m.%Y", False, 0, "uz-UZ",
        ("uz-UZ", "ru-UZ")),
    # Azerbaijan: Azerbaijani + Russian
    "AZ": ExtendedLocale("₼", True, ",", ".", 0.18, "ƏDV", "%d.%m.%Y", False, 0, "az-AZ",
        ("az-AZ", "ru-AZ")),
    "AM": ExtendedLocale("֏", False, ",", " ", 0.20, "ԱԱՀ", "%d.%m.%Y", False, 0, "hy-AM",
        ("hy-AM", "ru-AM")),
    # Georgia: Georgian + Russian + Armenian
    "GE": ExtendedLocale("₾", False, ",", " ", 0.18, "VAT", "%d.%m.%Y", False, 0, "ka-GE",
        ("ka-GE", "ru-GE", "hy-GE")),
    # ── North America ────────────────────────────────────────────────────────
    # USA: English — en-US is distinct (spelling, date format, idioms)
    "US": ExtendedLocale("$", True, ".", ",", 0.0, "", "%m/%d/%Y", False, 6, "en-US",
        ("en-US", "es-US")),
    # Canada: English + French (both official) — en-CA and fr-CA are both real
    "CA": ExtendedLocale("CA$", True, ".", ",", 0.05, "GST", "%Y-%m-%d", False, 0, "en-CA",
        ("en-CA", "fr-CA")),
    # Mexico: Spanish + indigenous (Nahuatl, Mayan, etc.)
    "MX": ExtendedLocale("MX$", True, ".", ",", 0.16, "IVA", "%d/%m/%Y", False, 0, "es-MX",
        ("es-MX",)),
    # ── Caribbean ────────────────────────────────────────────────────────────
    # T&T: English + Trinidadian Creole
    "TT": ExtendedLocale("TT$", True, ".", ",", 0.125, "VAT", "%d/%m/%Y", False, 0, "en-TT",
        ("en-TT",)),
    "JM": ExtendedLocale("J$", True, ".", ",", 0.15, "GCT", "%d/%m/%Y", False, 0, "en-JM",
        ("en-JM",)),
    "BB": ExtendedLocale("Bds$", True, ".", ",", 0.175, "VAT", "%d/%m/%Y", False, 0, "en-BB",
        ("en-BB",)),
    "VC": ExtendedLocale("EC$", True, ".", ",", 0.15, "VAT", "%d/%m/%Y", False, 0, "en-VC",
        ("en-VC",)),
    "LC": ExtendedLocale("EC$", True, ".", ",", 0.15, "VAT", "%d/%m/%Y", False, 0, "en-LC",
        ("en-LC",)),
    "GD": ExtendedLocale("EC$", True, ".", ",", 0.15, "VAT", "%d/%m/%Y", False, 0, "en-GD",
        ("en-GD",)),
    "DM": ExtendedLocale("EC$", True, ".", ",", 0.15, "VAT", "%d/%m/%Y", False, 0, "en-DM",
        ("en-DM", "fr-DM")),
    "AG": ExtendedLocale("EC$", True, ".", ",", 0.15, "VAT", "%d/%m/%Y", False, 0, "en-AG",
        ("en-AG",)),
    "KN": ExtendedLocale("EC$", True, ".", ",", 0.17, "VAT", "%d/%m/%Y", False, 0, "en-KN",
        ("en-KN",)),
    # Dominican Republic: Spanish only
    "DO": ExtendedLocale("RD$", True, ".", ",", 0.18, "ITBIS", "%d/%m/%Y", False, 0, "es-DO",
        ("es-DO",)),
    # Haiti: French + Haitian Creole (both official — Creole is dominant in daily life)
    "HT": ExtendedLocale("G", True, ",", ".", 0.10, "TVA", "%d/%m/%Y", False, 0, "fr-HT",
        ("fr-HT", "ht-HT")),
    "CU": ExtendedLocale("₱", True, ".", ",", 0.0, "", "%d/%m/%Y", False, 0, "es-CU",
        ("es-CU",)),
    # ── Central America ──────────────────────────────────────────────────────
    "NI": ExtendedLocale("C$", True, ".", ",", 0.15, "IVA", "%d/%m/%Y", False, 0, "es-NI",
        ("es-NI",)),
    "SV": ExtendedLocale("$", True, ".", ",", 0.13, "IVA", "%d/%m/%Y", False, 0, "es-SV",
        ("es-SV",)),
    "GT": ExtendedLocale("Q", True, ".", ",", 0.12, "IVA", "%d/%m/%Y", False, 0, "es-GT",
        ("es-GT",)),
    "HN": ExtendedLocale("L", True, ".", ",", 0.15, "ISV", "%d/%m/%Y", False, 0, "es-HN",
        ("es-HN",)),
    "CR": ExtendedLocale("₡", True, ",", ".", 0.13, "IVA", "%d/%m/%Y", False, 0, "es-CR",
        ("es-CR",)),
    "PA": ExtendedLocale("B/.", True, ".", ",", 0.07, "ITBMS", "%d/%m/%Y", False, 0, "es-PA",
        ("es-PA", "en-PA")),
    # ── South America ────────────────────────────────────────────────────────
    # Brazil: Portuguese — pt-BR is meaningfully different from pt-PT
    "BR": ExtendedLocale("R$", True, ",", ".", 0.0, "", "%d/%m/%Y", False, 0, "pt-BR",
        ("pt-BR",)),
    "AR": ExtendedLocale("$", True, ",", ".", 0.21, "IVA", "%d/%m/%Y", False, 0, "es-AR",
        ("es-AR",)),
    "CL": ExtendedLocale("$", True, ",", ".", 0.19, "IVA", "%d/%m/%Y", False, 0, "es-CL",
        ("es-CL",)),
    "CO": ExtendedLocale("$", True, ",", ".", 0.19, "IVA", "%d/%m/%Y", False, 0, "es-CO",
        ("es-CO",)),
    "PE": ExtendedLocale("S/", True, ".", ",", 0.18, "IGV", "%d/%m/%Y", False, 0, "es-PE",
        ("es-PE", "qu-PE", "ay-PE")),
    "VE": ExtendedLocale("Bs.D", True, ",", ".", 0.16, "IVA", "%d/%m/%Y", False, 0, "es-VE",
        ("es-VE",)),
    "EC": ExtendedLocale("$", True, ".", ",", 0.12, "IVA", "%d/%m/%Y", False, 0, "es-EC",
        ("es-EC", "qu-EC")),
    # Bolivia: Spanish + Quechua + Aymara (all three official)
    "BO": ExtendedLocale("Bs.", True, ".", ",", 0.13, "IVA", "%d/%m/%Y", False, 0, "es-BO",
        ("es-BO", "qu-BO", "ay-BO")),
    # Paraguay: Spanish + Guaraní (both official — one of few truly bilingual nations)
    "PY": ExtendedLocale("₲", True, ",", ".", 0.10, "IVA", "%d/%m/%Y", False, 0, "es-PY",
        ("es-PY", "gn-PY")),
    "UY": ExtendedLocale("$", True, ",", ".", 0.22, "IVA", "%d/%m/%Y", False, 0, "es-UY",
        ("es-UY",)),
    # ── Oceania ──────────────────────────────────────────────────────────────
    # Australia: English — en-AU is distinct (spelling, idioms, local tax terms)
    "AU": ExtendedLocale("A$", True, ".", ",", 0.10, "GST", "%d/%m/%Y", False, 0, "en-AU",
        ("en-AU",)),
    "NZ": ExtendedLocale("NZ$", True, ".", ",", 0.15, "GST", "%d/%m/%Y", False, 0, "en-NZ",
        ("en-NZ", "mi-NZ")),
    # PNG: English + Tok Pisin (Creole lingua franca) + Hiri Motu
    "PG": ExtendedLocale("K", True, ".", ",", 0.10, "VAT", "%d/%m/%Y", False, 0, "en-PG",
        ("en-PG", "tpi-PG", "ho-PG")),
    # Fiji: English + Fijian + Fiji Hindi
    "FJ": ExtendedLocale("FJ$", True, ".", ",", 0.09, "VAT", "%d/%m/%Y", False, 0, "en-FJ",
        ("en-FJ", "fj-FJ", "hif-FJ")),
    "TO": ExtendedLocale("T$", True, ".", ",", 0.15, "VAT", "%d/%m/%Y", False, 0, "en-TO",
        ("en-TO", "to-TO")),
    "WS": ExtendedLocale("T", True, ".", ",", 0.15, "VAT", "%d/%m/%Y", False, 0, "sm-WS",
        ("sm-WS", "en-WS")),
    "KI": ExtendedLocale("A$", True, ".", ",", 0.0, "", "%d/%m/%Y", False, 0, "en-KI",
        ("en-KI", "gil-KI")),
    "MH": ExtendedLocale("$", True, ".", ",", 0.0, "", "%m/%d/%Y", False, 6, "en-MH",
        ("en-MH", "mh-MH")),
    "FM": ExtendedLocale("$", True, ".", ",", 0.0, "", "%m/%d/%Y", False, 6, "en-FM",
        ("en-FM",)),
    "PW": ExtendedLocale("$", True, ".", ",", 0.0, "", "%m/%d/%Y", False, 6, "en-PW",
        ("en-PW",)),
    "SB": ExtendedLocale("SI$", True, ".", ",", 0.15, "PPIP", "%d/%m/%Y", False, 0, "en-SB",
        ("en-SB",)),
    # Vanuatu: Bislama (Creole) + English + French (three official)
    "VU": ExtendedLocale("VT", True, ".", ",", 0.15, "VAT", "%d/%m/%Y", False, 0, "en-VU",
        ("bi-VU", "en-VU", "fr-VU")),
    "NR": ExtendedLocale("A$", True, ".", ",", 0.0, "", "%d/%m/%Y", False, 0, "en-NR",
        ("en-NR", "na-NR")),
    "TV": ExtendedLocale("A$", True, ".", ",", 0.0, "", "%d/%m/%Y", False, 0, "en-TV",
        ("en-TV", "tvl-TV")),
    "TK": ExtendedLocale("NZ$", True, ".", ",", 0.0, "", "%d/%m/%Y", False, 0, "en-TK",
        ("en-TK", "tkl-TK")),
    # fmt: on
}

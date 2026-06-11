"""Tests for tala-locale v0.2.0 extended locale data."""

from tala_locale import ExtendedLocale, format_amount, get_extended

# ---------------------------------------------------------------------------
# get_extended — basic coverage
# ---------------------------------------------------------------------------


class TestGetExtended:
    def test_returns_extended_locale_instance(self):
        ext = get_extended("NG")
        assert isinstance(ext, ExtendedLocale)

    def test_unknown_returns_none(self):
        assert get_extended("XX") is None

    def test_empty_returns_none(self):
        assert get_extended("") is None

    def test_case_insensitive(self):
        assert get_extended("ng") == get_extended("NG")
        assert get_extended("de") == get_extended("DE")

    def test_none_input_returns_none(self):
        # None is not a valid str so mypy would catch it, but guard anyway
        assert get_extended(None) is None  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# Africa — primary TALA markets
# ---------------------------------------------------------------------------


class TestAfricanExtended:
    def test_nigeria(self):
        ext = get_extended("NG")
        assert ext.currency_symbol == "₦"
        assert ext.currency_before is True
        assert ext.decimal_sep == "."
        assert ext.thousands_sep == ","
        assert ext.vat_rate == 0.075
        assert ext.vat_name == "VAT"
        assert ext.date_format == "%d/%m/%Y"
        assert ext.rtl is False
        assert ext.bcp47 == "en-NG"

    def test_kenya(self):
        ext = get_extended("KE")
        assert ext.currency_symbol == "KSh"
        assert ext.vat_rate == 0.16
        assert ext.rtl is False

    def test_south_africa(self):
        ext = get_extended("ZA")
        assert ext.currency_symbol == "R"
        assert ext.thousands_sep == " "
        assert ext.vat_rate == 0.15
        assert ext.date_format == "%Y/%m/%d"

    def test_ghana(self):
        ext = get_extended("GH")
        assert ext.currency_symbol == "₵"
        assert ext.vat_rate == 0.15

    def test_egypt_rtl(self):
        ext = get_extended("EG")
        assert ext.rtl is True
        assert ext.week_start == 6  # Saturday in Egypt

    def test_tanzania(self):
        ext = get_extended("TZ")
        assert ext.currency_symbol == "TSh"
        assert ext.vat_rate == 0.18

    def test_senegal_french_cfa(self):
        ext = get_extended("SN")
        assert ext.currency_before is False
        assert ext.decimal_sep == ","
        assert ext.vat_name == "TVA"

    def test_ivory_coast(self):
        ext = get_extended("CI")
        assert ext.currency_symbol == "CFA"
        assert ext.vat_rate == 0.18

    def test_morocco_rtl(self):
        ext = get_extended("MA")
        assert ext.rtl is True
        assert ext.vat_rate == 0.20

    def test_zambia(self):
        ext = get_extended("ZM")
        assert ext.currency_symbol == "K"
        assert ext.vat_rate == 0.16

    def test_angola_portuguese(self):
        ext = get_extended("AO")
        assert ext.decimal_sep == ","
        assert ext.vat_name == "IVA"
        assert ext.bcp47 == "pt-AO"


# ---------------------------------------------------------------------------
# Middle East — RTL markets
# ---------------------------------------------------------------------------


class TestMiddleEastExtended:
    def test_saudi_arabia_rtl(self):
        ext = get_extended("SA")
        assert ext.rtl is True
        assert ext.currency_symbol == "SR"
        assert ext.vat_rate == 0.15

    def test_uae_low_vat(self):
        ext = get_extended("AE")
        assert ext.vat_rate == 0.05
        assert ext.rtl is True

    def test_qatar_no_vat(self):
        ext = get_extended("QA")
        assert ext.vat_rate == 0.0
        assert ext.vat_name == ""

    def test_kuwait_no_vat(self):
        ext = get_extended("KW")
        assert ext.vat_rate == 0.0

    def test_israel_rtl(self):
        ext = get_extended("IL")
        assert ext.rtl is True
        assert ext.currency_symbol == "₪"

    def test_turkey_comma_decimal(self):
        ext = get_extended("TR")
        assert ext.decimal_sep == ","
        assert ext.thousands_sep == "."


# ---------------------------------------------------------------------------
# Europe — symbol-after and comma-decimal
# ---------------------------------------------------------------------------


class TestEuropeanExtended:
    def test_uk_symbol_before(self):
        ext = get_extended("GB")
        assert ext.currency_symbol == "£"
        assert ext.currency_before is True

    def test_germany_symbol_after(self):
        ext = get_extended("DE")
        assert ext.currency_symbol == "€"
        assert ext.currency_before is False
        assert ext.decimal_sep == ","
        assert ext.thousands_sep == "."

    def test_france_symbol_after_space_thousand(self):
        ext = get_extended("FR")
        assert ext.currency_before is False
        assert ext.thousands_sep == " "

    def test_netherlands(self):
        ext = get_extended("NL")
        assert ext.currency_before is True
        assert ext.vat_name == "BTW"

    def test_sweden_iso_date(self):
        ext = get_extended("SE")
        assert ext.date_format == "%Y-%m-%d"
        assert ext.thousands_sep == " "


# ---------------------------------------------------------------------------
# Americas
# ---------------------------------------------------------------------------


class TestAmericasExtended:
    def test_us_no_vat_week_start_sunday(self):
        ext = get_extended("US")
        assert ext.vat_rate == 0.0
        assert ext.vat_name == ""
        assert ext.week_start == 6  # Sunday

    def test_us_vs_canada_distinct(self):
        us = get_extended("US")
        ca = get_extended("CA")
        assert us.currency_symbol != ca.currency_symbol  # $ vs CA$
        assert ca.vat_rate == 0.05  # federal GST only

    def test_brazil_comma_decimal(self):
        ext = get_extended("BR")
        assert ext.decimal_sep == ","
        assert ext.thousands_sep == "."
        assert ext.bcp47 == "pt-BR"

    def test_mexico_symbol_before(self):
        ext = get_extended("MX")
        assert ext.currency_before is True
        assert ext.vat_rate == 0.16


# ---------------------------------------------------------------------------
# Asia-Pacific
# ---------------------------------------------------------------------------


class TestAsiaPacificExtended:
    def test_india(self):
        ext = get_extended("IN")
        assert ext.currency_symbol == "₹"
        assert ext.vat_rate == 0.18

    def test_china(self):
        ext = get_extended("CN")
        assert ext.currency_symbol == "¥"
        assert ext.date_format == "%Y/%m/%d"

    def test_singapore(self):
        ext = get_extended("SG")
        assert ext.currency_symbol == "S$"
        assert ext.vat_name == "GST"

    def test_indonesia_comma_decimal(self):
        ext = get_extended("ID")
        assert ext.decimal_sep == ","
        assert ext.thousands_sep == "."

    def test_pakistan_rtl(self):
        ext = get_extended("PK")
        assert ext.rtl is True
        assert ext.bcp47 == "ur-PK"

    def test_australia(self):
        ext = get_extended("AU")
        assert ext.currency_symbol == "A$"
        assert ext.vat_rate == 0.10


# ---------------------------------------------------------------------------
# format_amount
# ---------------------------------------------------------------------------


class TestFormatAmount:
    # Symbol-before countries
    def test_nigeria_symbol_before(self):
        assert format_amount(1234.5, "NG") == "₦1,234.50"

    def test_us_symbol_before(self):
        assert format_amount(1234.5, "US") == "$1,234.50"

    def test_uk_symbol_before(self):
        assert format_amount(1234.5, "GB") == "£1,234.50"

    def test_india_symbol_before(self):
        assert format_amount(1234.5, "IN") == "₹1,234.50"

    # Symbol-after countries
    def test_germany_symbol_after_comma_decimal(self):
        assert format_amount(1234.5, "DE") == "1.234,50 €"

    def test_france_symbol_after_space_thousand(self):
        assert format_amount(1234.5, "FR") == "1 234,50 €"

    def test_south_africa_space_thousand(self):
        assert format_amount(1234.5, "ZA") == "R1 234.50"

    def test_senegal_cfa_after(self):
        assert format_amount(1234.5, "SN") == "1 234,50 CFA"

    def test_brazil_comma_decimal(self):
        assert format_amount(1234.5, "BR") == "R$1.234,50"

    # Edge cases
    def test_zero_value(self):
        assert format_amount(0, "NG") == "₦0.00"

    def test_large_number(self):
        result = format_amount(1234567.89, "NG")
        assert result == "₦1,234,567.89"

    def test_negative_value(self):
        result = format_amount(-1234.5, "NG")
        assert result == "-₦1,234.50"

    def test_negative_symbol_after(self):
        result = format_amount(-1234.5, "DE")
        assert result == "-1.234,50 €"

    def test_unknown_country_fallback(self):
        result = format_amount(1234.5, "XX")
        assert result == "1234.50"

    def test_integer_value(self):
        result = format_amount(1000, "NG")
        assert result == "₦1,000.00"

    def test_three_digit_no_separator(self):
        result = format_amount(999.0, "NG")
        assert result == "₦999.00"

    def test_exactly_one_thousand(self):
        result = format_amount(1000.0, "DE")
        assert result == "1.000,00 €"

    def test_millions_germany(self):
        result = format_amount(1234567.89, "DE")
        assert result == "1.234.567,89 €"

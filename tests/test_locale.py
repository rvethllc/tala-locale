from tala_locale import (
    LocaleResult,
    infer_country,
    infer_country_from_timezone,
    infer_currency,
    infer_language,
    infer_locale,
    is_supported,
    supported_countries,
)

# ---------------------------------------------------------------------------
# African numbers
# ---------------------------------------------------------------------------


class TestAfrican:
    def test_nigeria(self):
        r = infer_locale("2348012345678")
        assert r == LocaleResult("NG", "NGN", "en")

    def test_kenya(self):
        r = infer_locale("254712345678")
        assert r == LocaleResult("KE", "KES", "en")

    def test_ghana(self):
        r = infer_locale("233201234567")
        assert r == LocaleResult("GH", "GHS", "en")

    def test_south_africa_short_prefix(self):
        # +27 is a 2-digit prefix — must not be shadowed by a 1-digit match
        r = infer_locale("27821234567")
        assert r == LocaleResult("ZA", "ZAR", "en")

    def test_tanzania_swahili(self):
        r = infer_locale("255712345678")
        assert r == LocaleResult("TZ", "TZS", "sw")

    def test_egypt_arabic(self):
        r = infer_locale("201012345678")
        assert r == LocaleResult("EG", "EGP", "ar")

    def test_senegal_french(self):
        r = infer_locale("221771234567")
        assert r == LocaleResult("SN", "XOF", "fr")

    def test_ethiopia_amharic(self):
        r = infer_locale("251911234567")
        assert r == LocaleResult("ET", "ETB", "am")

    def test_drc(self):
        r = infer_locale("243812345678")
        assert r == LocaleResult("CD", "CDF", "fr")

    def test_rwanda(self):
        r = infer_locale("250781234567")
        assert r == LocaleResult("RW", "RWF", "en")


# ---------------------------------------------------------------------------
# Global / diaspora numbers
# ---------------------------------------------------------------------------


class TestGlobal:
    def test_uk(self):
        r = infer_locale("447911123456")
        assert r == LocaleResult("GB", "GBP", "en")

    def test_usa(self):
        r = infer_locale("14155552671")
        assert r == LocaleResult("US", "USD", "en")

    def test_france(self):
        r = infer_locale("33612345678")
        assert r == LocaleResult("FR", "EUR", "fr")

    def test_germany(self):
        r = infer_locale("4915112345678")
        assert r == LocaleResult("DE", "EUR", "de")

    def test_india(self):
        r = infer_locale("919812345678")
        assert r == LocaleResult("IN", "INR", "en")

    def test_brazil(self):
        r = infer_locale("5511912345678")
        assert r == LocaleResult("BR", "BRL", "pt")

    def test_uae(self):
        r = infer_locale("971501234567")
        assert r == LocaleResult("AE", "AED", "ar")

    def test_china(self):
        r = infer_locale("8613812345678")
        assert r == LocaleResult("CN", "CNY", "zh")

    def test_japan(self):
        r = infer_locale("819012345678")
        assert r == LocaleResult("JP", "JPY", "ja")

    def test_australia(self):
        r = infer_locale("61412345678")
        assert r == LocaleResult("AU", "AUD", "en")

    def test_turkey(self):
        r = infer_locale("905321234567")
        assert r == LocaleResult("TR", "TRY", "tr")

    def test_singapore(self):
        r = infer_locale("6591234567")
        assert r == LocaleResult("SG", "SGD", "en")

    def test_saudi_arabia(self):
        r = infer_locale("966512345678")
        assert r == LocaleResult("SA", "SAR", "ar")

    def test_nigeria_with_plus(self):
        r = infer_locale("+2348012345678")
        assert r == LocaleResult("NG", "NGN", "en")


# ---------------------------------------------------------------------------
# Longest-prefix-match correctness
# ---------------------------------------------------------------------------


class TestPrefixMatching:
    def test_trinidad_beats_usa(self):
        # +1868 (Trinidad) must win over +1 (USA)
        r = infer_locale("18681234567")
        assert r == LocaleResult("TT", "TTD", "en")

    def test_jamaica_beats_usa(self):
        r = infer_locale("18761234567")
        assert r == LocaleResult("JM", "JMD", "en")

    def test_barbados_beats_usa(self):
        r = infer_locale("12461234567")
        assert r == LocaleResult("BB", "BBD", "en")

    def test_hong_kong_beats_china(self):
        # +852 must win over +86 — different first digits so this tests ordering
        r = infer_locale("85291234567")
        assert r == LocaleResult("HK", "HKD", "zh")

    def test_bangladesh_beats_india_prefix_clash(self):
        # +880 starts with '8' — must not be confused with +86 (China)
        r = infer_locale("8801712345678")
        assert r == LocaleResult("BD", "BDT", "bn")

    def test_finland_beats_short_prefix(self):
        # +358 must not clash with +35x shorter candidates
        r = infer_locale("358401234567")
        assert r == LocaleResult("FI", "EUR", "fi")


# ---------------------------------------------------------------------------
# Phone format tolerance
# ---------------------------------------------------------------------------


class TestFormats:
    def test_plus_prefix(self):
        assert infer_locale("+2348012345678").country == "NG"

    def test_bare_digits(self):
        assert infer_locale("2348012345678").country == "NG"

    def test_spaces(self):
        assert infer_locale("+234 801 234 5678").country == "NG"

    def test_dashes(self):
        assert infer_locale("+234-801-234-5678").country == "NG"

    def test_parentheses(self):
        assert infer_locale("(234) 801 234 5678").country == "NG"

    def test_whatsapp_prefix(self):
        assert infer_locale("whatsapp:+2348012345678").country == "NG"

    def test_whatsapp_no_plus(self):
        assert infer_locale("whatsapp:2348012345678").country == "NG"

    def test_mixed_formatting(self):
        assert infer_locale("+1 (415) 555-2671").country == "US"


# ---------------------------------------------------------------------------
# Unknown / edge cases
# ---------------------------------------------------------------------------


class TestEdgeCases:
    def test_unknown_prefix_returns_none_triple(self):
        r = infer_locale("+882123456789")
        assert r == LocaleResult(None, None, None)
        assert r.country is None
        assert r.currency is None
        assert r.language is None

    def test_empty_string(self):
        assert infer_locale("") == LocaleResult(None, None, None)

    def test_none_input(self):  # type: ignore[arg-type]
        assert infer_locale(None) == LocaleResult(None, None, None)  # type: ignore[arg-type]

    def test_whitespace_only(self):
        assert infer_locale("   ") == LocaleResult(None, None, None)

    def test_letters_only(self):
        assert infer_locale("abcdef") == LocaleResult(None, None, None)


# ---------------------------------------------------------------------------
# LocaleResult helpers
# ---------------------------------------------------------------------------


class TestLocaleResult:
    def test_is_known_true(self):
        assert infer_locale("+2348012345678").is_known() is True

    def test_is_known_false(self):
        assert infer_locale("+882123456789").is_known() is False

    def test_unpacks_as_tuple(self):
        country, currency, language = infer_locale("+2348012345678")
        assert country == "NG"
        assert currency == "NGN"
        assert language == "en"

    def test_named_field_access(self):
        r = infer_locale("+14155552671")
        assert r.country == "US"
        assert r.currency == "USD"
        assert r.language == "en"


# ---------------------------------------------------------------------------
# Shortcut functions
# ---------------------------------------------------------------------------


class TestShortcuts:
    def test_infer_country(self):
        assert infer_country("+2348012345678") == "NG"
        assert infer_country("+882123456789") is None

    def test_infer_currency(self):
        assert infer_currency("+2348012345678") == "NGN"
        assert infer_currency("+882123456789") is None

    def test_infer_language(self):
        assert infer_language("+2348012345678") == "en"
        assert infer_language("+882123456789") is None


# ---------------------------------------------------------------------------
# is_supported
# ---------------------------------------------------------------------------


class TestIsSupported:
    def test_known_number(self):
        assert is_supported("+2348012345678") is True

    def test_unknown_number(self):
        assert is_supported("+882123456789") is False

    def test_empty(self):
        assert is_supported("") is False


# ---------------------------------------------------------------------------
# supported_countries
# ---------------------------------------------------------------------------


class TestSupportedCountries:
    def test_returns_list_of_dicts(self):
        entries = supported_countries()
        assert isinstance(entries, list)
        assert len(entries) > 180

    def test_entry_shape(self):
        entry = supported_countries()[0]
        assert set(entry.keys()) == {"prefix", "country", "currency", "language"}

    def test_all_entries_non_empty(self):
        for entry in supported_countries():
            assert entry["prefix"]
            assert entry["country"]
            assert entry["currency"]
            assert entry["language"]

    def test_nigeria_present(self):
        countries = {e["country"] for e in supported_countries()}
        assert "NG" in countries

    def test_us_present(self):
        countries = {e["country"] for e in supported_countries()}
        assert "US" in countries


# ---------------------------------------------------------------------------
# infer_country_from_timezone — single-timezone countries
# ---------------------------------------------------------------------------


class TestTimezoneInference:
    def test_nigeria(self):
        assert infer_country_from_timezone("Africa/Lagos") == "NG"

    def test_kenya(self):
        assert infer_country_from_timezone("Africa/Nairobi") == "KE"

    def test_ghana(self):
        assert infer_country_from_timezone("Africa/Accra") == "GH"

    def test_south_africa(self):
        assert infer_country_from_timezone("Africa/Johannesburg") == "ZA"

    def test_egypt(self):
        assert infer_country_from_timezone("Africa/Cairo") == "EG"

    def test_uk(self):
        assert infer_country_from_timezone("Europe/London") == "GB"

    def test_ireland(self):
        assert infer_country_from_timezone("Europe/Dublin") == "IE"

    def test_france(self):
        assert infer_country_from_timezone("Europe/Paris") == "FR"

    def test_germany(self):
        assert infer_country_from_timezone("Europe/Berlin") == "DE"

    def test_uae(self):
        assert infer_country_from_timezone("Asia/Dubai") == "AE"

    def test_india(self):
        assert infer_country_from_timezone("Asia/Kolkata") == "IN"

    def test_india_legacy(self):
        # Calcutta is a legacy alias for Kolkata
        assert infer_country_from_timezone("Asia/Calcutta") == "IN"

    def test_japan(self):
        assert infer_country_from_timezone("Asia/Tokyo") == "JP"

    def test_singapore(self):
        assert infer_country_from_timezone("Asia/Singapore") == "SG"

    def test_australia_sydney(self):
        assert infer_country_from_timezone("Australia/Sydney") == "AU"


# ---------------------------------------------------------------------------
# Multi-timezone country disambiguation — the whole point of this feature
# ---------------------------------------------------------------------------


class TestTimezoneMultiZoneCountries:
    # USA — 7 zones, all must return "US"
    def test_us_eastern(self):
        assert infer_country_from_timezone("America/New_York") == "US"

    def test_us_central(self):
        assert infer_country_from_timezone("America/Chicago") == "US"

    def test_us_mountain(self):
        assert infer_country_from_timezone("America/Denver") == "US"

    def test_us_pacific(self):
        assert infer_country_from_timezone("America/Los_Angeles") == "US"

    def test_us_alaska(self):
        assert infer_country_from_timezone("America/Anchorage") == "US"

    def test_us_hawaii(self):
        assert infer_country_from_timezone("Pacific/Honolulu") == "US"

    def test_us_arizona(self):
        assert infer_country_from_timezone("America/Phoenix") == "US"

    # Canada — distinguished from USA despite sharing +1 calling code
    def test_canada_toronto(self):
        assert infer_country_from_timezone("America/Toronto") == "CA"

    def test_canada_vancouver(self):
        assert infer_country_from_timezone("America/Vancouver") == "CA"

    def test_canada_halifax(self):
        assert infer_country_from_timezone("America/Halifax") == "CA"

    def test_canada_winnipeg(self):
        assert infer_country_from_timezone("America/Winnipeg") == "CA"

    def test_canada_st_johns(self):
        assert infer_country_from_timezone("America/St_Johns") == "CA"

    # Indonesia — 3 zones, all return "ID"
    def test_indonesia_jakarta(self):
        assert infer_country_from_timezone("Asia/Jakarta") == "ID"

    def test_indonesia_makassar(self):
        assert infer_country_from_timezone("Asia/Makassar") == "ID"

    def test_indonesia_jayapura(self):
        assert infer_country_from_timezone("Asia/Jayapura") == "ID"

    # Brazil — 4 zones, all return "BR"
    def test_brazil_sao_paulo(self):
        assert infer_country_from_timezone("America/Sao_Paulo") == "BR"

    def test_brazil_manaus(self):
        assert infer_country_from_timezone("America/Manaus") == "BR"

    def test_brazil_fortaleza(self):
        assert infer_country_from_timezone("America/Fortaleza") == "BR"

    def test_brazil_recife(self):
        assert infer_country_from_timezone("America/Recife") == "BR"

    # Russia — 11 zones, spot-check 3
    def test_russia_moscow(self):
        assert infer_country_from_timezone("Europe/Moscow") == "RU"

    def test_russia_yekaterinburg(self):
        assert infer_country_from_timezone("Asia/Yekaterinburg") == "RU"

    def test_russia_vladivostok(self):
        assert infer_country_from_timezone("Asia/Vladivostok") == "RU"

    # Australia — 7 zones, spot-check 3
    def test_australia_perth(self):
        assert infer_country_from_timezone("Australia/Perth") == "AU"

    def test_australia_darwin(self):
        assert infer_country_from_timezone("Australia/Darwin") == "AU"

    def test_australia_brisbane(self):
        assert infer_country_from_timezone("Australia/Brisbane") == "AU"

    # China — 2 zones (legacy Chongqing alias), both return "CN"
    def test_china_shanghai(self):
        assert infer_country_from_timezone("Asia/Shanghai") == "CN"

    def test_china_urumqi(self):
        assert infer_country_from_timezone("Asia/Urumqi") == "CN"

    # Mongolia — 3 zones
    def test_mongolia_ulaanbaatar(self):
        assert infer_country_from_timezone("Asia/Ulaanbaatar") == "MN"

    def test_mongolia_hovd(self):
        assert infer_country_from_timezone("Asia/Hovd") == "MN"

    # New Zealand — 2 zones
    def test_nz_auckland(self):
        assert infer_country_from_timezone("Pacific/Auckland") == "NZ"

    def test_nz_chatham(self):
        assert infer_country_from_timezone("Pacific/Chatham") == "NZ"


# ---------------------------------------------------------------------------
# Unknown / edge cases for timezone
# ---------------------------------------------------------------------------


class TestTimezoneEdgeCases:
    def test_unknown_returns_none(self):
        assert infer_country_from_timezone("Unknown/Zone") is None

    def test_empty_string_returns_none(self):
        assert infer_country_from_timezone("") is None

    def test_none_input_returns_none(self):  # type: ignore[arg-type]
        assert infer_country_from_timezone(None) is None  # type: ignore[arg-type]

    def test_utc_returns_none(self):
        # UTC is not a country — callers must not assume a country from UTC
        assert infer_country_from_timezone("UTC") is None

    def test_gmt_returns_none(self):
        assert infer_country_from_timezone("GMT") is None

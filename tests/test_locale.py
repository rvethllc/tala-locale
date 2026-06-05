from tala_locale import (
    LocaleResult,
    infer_country,
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

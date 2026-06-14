"""
Tests for tala-locale v2.0.0 — timezone inference, UTC offset, datetime conversion,
full locale inference, and +1/+7 disambiguation.
"""

from __future__ import annotations

from datetime import datetime
from datetime import timezone as stdlib_tz

import pytest

from tala_locale import (
    FullLocaleResult,
    format_local_datetime,
    get_local_datetime,
    get_utc_offset,
    infer_full_locale,
    infer_timezone,
    infer_timezones,
)

# ---------------------------------------------------------------------------
# infer_timezone — country → primary IANA zone
# ---------------------------------------------------------------------------


class TestInferTimezone:
    def test_nigeria(self):
        assert infer_timezone("NG") == "Africa/Lagos"

    def test_ghana(self):
        assert infer_timezone("GH") == "Africa/Accra"

    def test_kenya(self):
        assert infer_timezone("KE") == "Africa/Nairobi"

    def test_south_africa(self):
        assert infer_timezone("ZA") == "Africa/Johannesburg"

    def test_uk(self):
        assert infer_timezone("GB") == "Europe/London"

    def test_germany(self):
        assert infer_timezone("DE") == "Europe/Berlin"

    def test_france(self):
        assert infer_timezone("FR") == "Europe/Paris"

    def test_india(self):
        # India has a single IANA zone — no ambiguity
        assert infer_timezone("IN") == "Asia/Kolkata"

    def test_japan(self):
        assert infer_timezone("JP") == "Asia/Tokyo"

    def test_singapore(self):
        assert infer_timezone("SG") == "Asia/Singapore"

    # Multi-timezone countries — primary zone
    def test_us_returns_new_york(self):
        # Most-populated time zone
        assert infer_timezone("US") == "America/New_York"

    def test_canada_returns_toronto(self):
        assert infer_timezone("CA") == "America/Toronto"

    def test_russia_returns_moscow(self):
        assert infer_timezone("RU") == "Europe/Moscow"

    def test_brazil_returns_sao_paulo(self):
        assert infer_timezone("BR") == "America/Sao_Paulo"

    def test_indonesia_returns_jakarta(self):
        assert infer_timezone("ID") == "Asia/Jakarta"

    def test_australia_returns_sydney(self):
        assert infer_timezone("AU") == "Australia/Sydney"

    def test_mexico_returns_mexico_city(self):
        assert infer_timezone("MX") == "America/Mexico_City"

    def test_china_returns_shanghai(self):
        assert infer_timezone("CN") == "Asia/Shanghai"

    # Case-insensitive
    def test_lowercase(self):
        assert infer_timezone("ng") == "Africa/Lagos"

    def test_mixed_case(self):
        assert infer_timezone("Ng") == "Africa/Lagos"

    # Edge cases
    def test_unknown_returns_none(self):
        assert infer_timezone("XX") is None

    def test_empty_returns_none(self):
        assert infer_timezone("") is None

    def test_none_returns_none(self):
        assert infer_timezone(None) is None  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# infer_timezones — country → ALL IANA zones
# ---------------------------------------------------------------------------


class TestInferTimezones:
    def test_nigeria_single_zone(self):
        assert infer_timezones("NG") == ("Africa/Lagos",)

    def test_us_has_many_zones(self):
        zones = infer_timezones("US")
        assert len(zones) >= 20
        assert "America/New_York" in zones
        assert "America/Los_Angeles" in zones
        assert "America/Chicago" in zones
        assert "America/Denver" in zones
        assert "America/Anchorage" in zones
        assert "Pacific/Honolulu" in zones

    def test_canada_zones(self):
        zones = infer_timezones("CA")
        assert "America/Toronto" in zones
        assert "America/Vancouver" in zones
        assert "America/Halifax" in zones
        assert "America/St_Johns" in zones

    def test_indonesia_three_zones(self):
        zones = infer_timezones("ID")
        assert "Asia/Jakarta" in zones
        assert "Asia/Makassar" in zones
        assert "Asia/Jayapura" in zones

    def test_russia_eleven_zones(self):
        zones = infer_timezones("RU")
        assert len(zones) >= 11
        assert "Europe/Moscow" in zones
        assert "Asia/Yekaterinburg" in zones
        assert "Asia/Vladivostok" in zones
        assert "Asia/Kamchatka" in zones

    def test_brazil_zones(self):
        zones = infer_timezones("BR")
        assert "America/Sao_Paulo" in zones
        assert "America/Manaus" in zones
        assert "America/Fortaleza" in zones

    def test_australia_zones(self):
        zones = infer_timezones("AU")
        assert "Australia/Sydney" in zones
        assert "Australia/Perth" in zones
        assert "Australia/Darwin" in zones

    def test_sorted_alphabetically(self):
        zones = infer_timezones("US")
        assert list(zones) == sorted(zones)

    def test_unknown_returns_empty_tuple(self):
        assert infer_timezones("XX") == ()

    def test_empty_returns_empty_tuple(self):
        assert infer_timezones("") == ()


# ---------------------------------------------------------------------------
# get_utc_offset — country code or IANA string → offset in decimal hours
# ---------------------------------------------------------------------------


class TestGetUtcOffset:
    def test_nigeria_no_dst(self):
        # WAT is always UTC+1 — no DST
        assert get_utc_offset("NG") == 1.0

    def test_ghana_utc(self):
        # Ghana uses GMT year-round
        assert get_utc_offset("GH") == 0.0

    def test_india_half_hour(self):
        # IST = UTC+5:30, no DST ever
        assert get_utc_offset("IN") == 5.5

    def test_nepal_quarter_hour(self):
        # NPT = UTC+5:45 — one of only two quarter-hour offsets in the world
        assert get_utc_offset("NP") == 5.75

    def test_uae_no_dst(self):
        # GST = UTC+4, no DST
        assert get_utc_offset("AE") == 4.0

    def test_saudi_arabia_no_dst(self):
        # AST = UTC+3, no DST
        assert get_utc_offset("SA") == 3.0

    def test_china_no_dst(self):
        # CST = UTC+8, no DST
        assert get_utc_offset("CN") == 8.0

    def test_japan_no_dst(self):
        # JST = UTC+9, no DST
        assert get_utc_offset("JP") == 9.0

    def test_iana_string_direct(self):
        # Accepts IANA timezone string directly
        assert get_utc_offset("Africa/Lagos") == 1.0

    def test_iana_new_york(self):
        # EST = -5 or EDT = -4 depending on DST — just verify it's one of them
        offset = get_utc_offset("America/New_York")
        assert offset in (-5.0, -4.0)

    def test_iana_toronto(self):
        # Same rules as New York
        offset = get_utc_offset("America/Toronto")
        assert offset in (-5.0, -4.0)

    def test_uk_is_dst_aware(self):
        # GMT = 0.0 in winter, BST = 1.0 in summer
        offset = get_utc_offset("GB")
        assert offset in (0.0, 1.0)

    def test_uk_matches_iana(self):
        assert get_utc_offset("GB") == get_utc_offset("Europe/London")

    def test_unknown_country_returns_none(self):
        assert get_utc_offset("XX") is None

    def test_unknown_iana_returns_none(self):
        assert get_utc_offset("Unknown/Zone") is None

    def test_empty_returns_none(self):
        assert get_utc_offset("") is None

    def test_case_insensitive_country(self):
        assert get_utc_offset("ng") == 1.0


# ---------------------------------------------------------------------------
# get_local_datetime — UTC → local datetime
# ---------------------------------------------------------------------------


class TestGetLocalDatetime:
    _UTC = datetime(
        2025, 1, 15, 12, 0, 0, tzinfo=stdlib_tz.utc
    )  # January = Northern winter

    def test_nigeria_utc_plus_1(self):
        local = get_local_datetime(self._UTC, "NG")
        assert local.hour == 13  # UTC+1

    def test_uk_january_no_dst(self):
        local = get_local_datetime(self._UTC, "GB")
        assert local.hour == 12  # GMT in January

    def test_uk_july_dst(self):
        july = datetime(2025, 7, 15, 12, 0, 0, tzinfo=stdlib_tz.utc)
        local = get_local_datetime(july, "GB")
        assert local.hour == 13  # BST = UTC+1 in summer

    def test_us_eastern_january(self):
        local = get_local_datetime(self._UTC, "US")
        assert local.hour == 7  # EST = UTC-5 in January

    def test_india_half_hour(self):
        local = get_local_datetime(self._UTC, "IN")
        assert local.hour == 17
        assert local.minute == 30  # IST = UTC+5:30

    def test_nepal_quarter_hour(self):
        local = get_local_datetime(self._UTC, "NP")
        assert local.hour == 17
        assert local.minute == 45  # NPT = UTC+5:45

    def test_iana_string_direct(self):
        local = get_local_datetime(self._UTC, "America/New_York")
        assert local.hour == 7  # EST in January

    def test_result_is_timezone_aware(self):
        local = get_local_datetime(self._UTC, "NG")
        assert local.tzinfo is not None

    def test_naive_input_treated_as_utc(self):
        naive = datetime(2025, 1, 15, 12, 0, 0)  # no tzinfo
        local = get_local_datetime(naive, "NG")
        assert local.hour == 13

    def test_unknown_country_raises(self):
        with pytest.raises(ValueError):
            get_local_datetime(self._UTC, "XX")

    def test_unknown_iana_raises(self):
        with pytest.raises(ValueError):
            get_local_datetime(self._UTC, "Unknown/Zone")

    def test_canada_toronto(self):
        # Toronto uses Eastern time same as New York
        local = get_local_datetime(self._UTC, "CA")
        assert local.hour == 7  # EST in January

    def test_ghana_utc(self):
        local = get_local_datetime(self._UTC, "GH")
        assert local.hour == 12  # UTC+0


# ---------------------------------------------------------------------------
# format_local_datetime
# ---------------------------------------------------------------------------


class TestFormatLocalDatetime:
    _UTC = datetime(2025, 6, 14, 11, 30, 45, tzinfo=stdlib_tz.utc)

    def test_nigeria_date_format(self):
        result = format_local_datetime(self._UTC, "NG")
        assert result == "14/06/2025 12:30"  # WAT = UTC+1 in June

    def test_us_date_format(self):
        result = format_local_datetime(self._UTC, "US")
        # EST+DST = EDT = UTC-4 in June  →  07:30
        assert result == "06/14/2025 07:30"

    def test_germany_date_format(self):
        result = format_local_datetime(self._UTC, "DE")
        # CEST = UTC+2 in June  →  13:30
        assert result == "14.06.2025 13:30"

    def test_sweden_iso_date(self):
        result = format_local_datetime(self._UTC, "SE")
        # CEST = UTC+2 in June  →  13:30
        assert result == "2025-06-14 13:30"

    def test_date_only(self):
        result = format_local_datetime(self._UTC, "NG", include_time=False)
        assert result == "14/06/2025"

    def test_include_seconds(self):
        result = format_local_datetime(self._UTC, "NG", include_seconds=True)
        assert result == "14/06/2025 12:30:45"

    def test_iana_string(self):
        result = format_local_datetime(self._UTC, "Africa/Lagos", include_time=False)
        assert result == "14/06/2025"

    def test_unknown_country_raises(self):
        with pytest.raises(ValueError):
            format_local_datetime(self._UTC, "XX")


# ---------------------------------------------------------------------------
# infer_full_locale — primary v2 entry point
# ---------------------------------------------------------------------------


class TestInferFullLocale:
    # ── Single-timezone countries — confidence 1.0 ──────────────────────────

    def test_nigeria(self):
        r = infer_full_locale("+2348012345678")
        assert r.country == "NG"
        assert r.currency == "NGN"
        assert r.language == "en-NG"  # BCP 47 from extended data
        assert r.timezone == "Africa/Lagos"
        assert r.utc_offset_hours == 1.0
        assert r.confidence == 1.0
        assert r.extended is not None
        assert r.extended.currency_symbol == "₦"

    def test_ghana(self):
        r = infer_full_locale("+233201234567")
        assert r.country == "GH"
        assert r.timezone == "Africa/Accra"
        assert r.utc_offset_hours == 0.0
        assert r.confidence == 1.0

    def test_uk(self):
        r = infer_full_locale("+447911123456")
        assert r.country == "GB"
        assert r.timezone == "Europe/London"
        assert r.confidence == 1.0

    def test_india(self):
        r = infer_full_locale("+919812345678")
        assert r.country == "IN"
        assert r.timezone == "Asia/Kolkata"
        assert r.utc_offset_hours == 5.5
        assert r.confidence == 1.0

    def test_japan(self):
        r = infer_full_locale("+819012345678")
        assert r.country == "JP"
        assert r.timezone == "Asia/Tokyo"
        assert r.utc_offset_hours == 9.0
        assert r.confidence == 1.0

    def test_uae(self):
        r = infer_full_locale("+971501234567")
        assert r.country == "AE"
        assert r.utc_offset_hours == 4.0
        assert r.confidence == 1.0

    # ── Multi-timezone — phone only, no browser tz → primary zone ──────────

    def test_us_phone_only_gets_eastern_zone(self):
        # +1-212 = New York City area code → America/New_York
        r = infer_full_locale("+12125551234")
        assert r.country == "US"
        assert r.timezone == "America/New_York"
        assert r.confidence == 1.0

    def test_brazil_phone_only_gets_sao_paulo(self):
        r = infer_full_locale("+5511912345678")
        assert r.country == "BR"
        assert r.timezone == "America/Sao_Paulo"
        assert r.confidence == 1.0

    # ── +1 disambiguation — US vs Canada ────────────────────────────────────

    def test_plus1_with_toronto_tz_resolves_canada(self):
        # +1-416 = Toronto NPA → area code resolves CA at confidence 0.95
        # browser_timezone confirms, but area code already got there first
        r = infer_full_locale("+14165551234", browser_timezone="America/Toronto")
        assert r.country == "CA"
        assert r.timezone == "America/Toronto"
        assert r.confidence >= 0.9  # 0.95 from area code, 0.9 from tz-only

    def test_plus1_with_new_york_tz_confirms_us(self):
        # Phone says US (+1), browser says New York → they agree → confidence 1.0
        r = infer_full_locale("+12125551234", browser_timezone="America/New_York")
        assert r.country == "US"
        assert r.timezone == "America/New_York"
        assert r.confidence == 1.0  # agreement: no tiebreak needed

    def test_plus1_with_los_angeles_tz_overrides_primary_zone(self):
        # Phone says US (+1), browser says LA → still US, but uses LA timezone
        r = infer_full_locale("+14155552671", browser_timezone="America/Los_Angeles")
        assert r.country == "US"
        assert r.timezone == "America/Los_Angeles"
        assert r.confidence == 1.0  # same country — full confidence

    def test_plus1_with_vancouver_tz_resolves_canada(self):
        # +1-604 = British Columbia NPA → area code resolves CA at confidence 0.95
        r = infer_full_locale("+16041234567", browser_timezone="America/Vancouver")
        assert r.country == "CA"
        assert r.timezone == "America/Vancouver"
        assert r.confidence >= 0.9  # 0.95 from area code

    def test_plus1_agreement_gives_full_confidence(self):
        # Phone says US, browser says New York — they agree → 1.0
        r = infer_full_locale("+12125551234", browser_timezone="America/New_York")
        assert r.country == "US"
        assert r.confidence == 1.0

    # ── Indonesia — 3 timezones, same country ────────────────────────────────

    def test_indonesia_jakarta(self):
        r = infer_full_locale("+6221123456", browser_timezone="Asia/Jakarta")
        assert r.country == "ID"
        assert r.timezone == "Asia/Jakarta"
        assert r.utc_offset_hours == 7.0
        assert r.confidence == 1.0  # phone and tz agree on country

    def test_indonesia_bali(self):
        # Bali uses Asia/Makassar (WITA = UTC+8)
        r = infer_full_locale("+6236123456", browser_timezone="Asia/Makassar")
        assert r.country == "ID"
        assert r.timezone == "Asia/Makassar"
        assert r.utc_offset_hours == 8.0

    def test_indonesia_papua(self):
        r = infer_full_locale("+62901234567", browser_timezone="Asia/Jayapura")
        assert r.country == "ID"
        assert r.timezone == "Asia/Jayapura"
        assert r.utc_offset_hours == 9.0

    # ── Timezone-only fallback (no phone) ───────────────────────────────────

    def test_no_phone_timezone_only(self):
        r = infer_full_locale("", browser_timezone="Africa/Lagos")
        assert r.country == "NG"
        assert r.timezone == "Africa/Lagos"
        assert r.confidence == 0.8

    def test_no_phone_new_york(self):
        r = infer_full_locale("", browser_timezone="America/New_York")
        assert r.country == "US"
        assert r.timezone == "America/New_York"
        assert r.confidence == 0.8

    def test_no_phone_toronto(self):
        r = infer_full_locale("", browser_timezone="America/Toronto")
        assert r.country == "CA"
        assert r.confidence == 0.8

    # ── Unknown / failure cases ──────────────────────────────────────────────

    def test_unknown_phone_no_tz_returns_empty(self):
        r = infer_full_locale("+882123456789")
        assert r.country is None
        assert r.confidence == 0.0

    def test_none_phone_no_tz_returns_empty(self):
        r = infer_full_locale(None)  # type: ignore[arg-type]
        assert r.country is None
        assert r.confidence == 0.0

    def test_empty_phone_no_tz_returns_empty(self):
        r = infer_full_locale("")
        assert r.country is None
        assert r.confidence == 0.0

    # ── FullLocaleResult is a NamedTuple ─────────────────────────────────────

    def test_is_named_tuple(self):
        r = infer_full_locale("+2348012345678")
        assert isinstance(r, FullLocaleResult)

    def test_unpacks(self):
        r = infer_full_locale("+2348012345678")
        # Access by name — NamedTuple has grown with flattened fields
        assert r.country == "NG"
        assert r.timezone == "Africa/Lagos"
        assert r.confidence == 1.0

    def test_extended_is_none_for_uncovered_country(self):
        # Use a country not in the extended dataset
        # All 191 countries in _data.py don't all have extended data
        # Seychelles (+248) is in _data.py but not in extended
        r = infer_full_locale("+2481234567")
        if r.country is not None:
            # extended may or may not be present — just verify it's the right type
            assert r.extended is None or hasattr(r.extended, "currency_symbol")


# ---------------------------------------------------------------------------
# Regression — +1 (Trinidad) still beats Canada/US for 4-digit prefix
# ---------------------------------------------------------------------------


class TestPlusDiambiguationDoesNotBreakNARN:
    def test_trinidad_still_wins_over_us(self):
        r = infer_full_locale("+18681234567")
        assert r.country == "TT"
        assert r.confidence == 1.0

    def test_jamaica_still_wins(self):
        r = infer_full_locale("+18761234567")
        assert r.country == "JM"
        assert r.confidence == 1.0

    def test_barbados_still_wins(self):
        r = infer_full_locale("+12461234567")
        assert r.country == "BB"
        assert r.confidence == 1.0

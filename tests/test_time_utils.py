"""Unit tests for utils/time_utils.py."""

import pytest
from utils.time_utils import parse_time, format_time, format_time_short, format_duration, clamp


class TestParseTime:
    """Tests for parse_time()."""

    def test_seconds_only_integer(self):
        assert parse_time("90") == 90.0

    def test_seconds_only_decimal(self):
        assert parse_time("90.5") == 90.5

    def test_seconds_zero(self):
        assert parse_time("0") == 0.0

    def test_mm_ss(self):
        assert parse_time("1:30") == 90.0

    def test_mm_ss_with_decimal(self):
        assert parse_time("1:30.5") == 90.5

    def test_mm_ss_zero_minutes(self):
        assert parse_time("0:45") == 45.0

    def test_hh_mm_ss(self):
        assert parse_time("1:02:30") == 3750.0

    def test_hh_mm_ss_with_decimal(self):
        assert parse_time("1:02:30.5") == 3750.5

    def test_hh_mm_ss_zeros(self):
        assert parse_time("0:00:00") == 0.0

    def test_large_hours(self):
        assert parse_time("10:00:00") == 36000.0

    def test_whitespace_stripped(self):
        assert parse_time("  90  ") == 90.0

    def test_empty_string_raises(self):
        with pytest.raises(ValueError, match="cannot be empty"):
            parse_time("")

    def test_whitespace_only_raises(self):
        with pytest.raises(ValueError, match="cannot be empty"):
            parse_time("   ")

    def test_non_string_raises(self):
        with pytest.raises(ValueError, match="must be a string"):
            parse_time(90)

    def test_invalid_format_raises(self):
        with pytest.raises(ValueError, match="Invalid time format"):
            parse_time("abc")

    def test_negative_raises(self):
        with pytest.raises(ValueError, match="Invalid time format"):
            parse_time("-10")

    def test_too_many_colons_raises(self):
        with pytest.raises(ValueError, match="Invalid time format"):
            parse_time("1:2:3:4")

    def test_invalid_seconds_over_59(self):
        with pytest.raises(ValueError, match="Invalid time format"):
            parse_time("1:60")

    def test_two_fifteen(self):
        """Example use case: 2:15 = 135 seconds."""
        assert parse_time("2:15") == 135.0

    def test_four_forty(self):
        """Example use case: 4:40 = 280 seconds."""
        assert parse_time("4:40") == 280.0


class TestFormatTime:
    """Tests for format_time()."""

    def test_zero(self):
        assert format_time(0) == "00:00:00.0"

    def test_seconds_only(self):
        assert format_time(45.5) == "00:00:45.5"

    def test_minutes_and_seconds(self):
        assert format_time(90) == "00:01:30.0"

    def test_hours(self):
        assert format_time(3661.5) == "01:01:01.5"

    def test_negative_raises(self):
        with pytest.raises(ValueError, match="cannot be negative"):
            format_time(-1)


class TestFormatTimeShort:
    """Tests for format_time_short()."""

    def test_under_one_hour(self):
        assert format_time_short(90) == "1:30.0"

    def test_over_one_hour(self):
        assert format_time_short(3661.5) == "1:01:01.5"

    def test_zero(self):
        assert format_time_short(0) == "0:00.0"

    def test_negative_raises(self):
        with pytest.raises(ValueError, match="cannot be negative"):
            format_time_short(-1)


class TestFormatDuration:
    """Tests for format_duration()."""

    def test_seconds_only(self):
        assert format_duration(2.5) == "2.5s"

    def test_minutes_and_seconds(self):
        assert format_duration(90) == "1m 30.0s"

    def test_hours_minutes_seconds(self):
        assert format_duration(3661.5) == "1h 1m 1.5s"

    def test_zero(self):
        assert format_duration(0) == "0.0s"

    def test_negative_raises(self):
        with pytest.raises(ValueError, match="cannot be negative"):
            format_duration(-1)


class TestClamp:
    """Tests for clamp()."""

    def test_within_range(self):
        assert clamp(5, 0, 10) == 5

    def test_below_min(self):
        assert clamp(-1, 0, 10) == 0

    def test_above_max(self):
        assert clamp(15, 0, 10) == 10

    def test_at_min(self):
        assert clamp(0, 0, 10) == 0

    def test_at_max(self):
        assert clamp(10, 0, 10) == 10

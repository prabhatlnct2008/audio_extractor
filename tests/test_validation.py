"""Unit tests for services/validation.py."""

import os
import tempfile
import pytest
from services.validation import (
    validate_source_file,
    validate_time_range,
    validate_output_path,
    validate_extraction_ready,
    MIN_CLIP_DURATION,
)


class TestValidateSourceFile:

    def test_empty_path(self):
        valid, msg = validate_source_file("")
        assert not valid
        assert "select a video file" in msg.lower()

    def test_none_path(self):
        valid, msg = validate_source_file(None)
        assert not valid

    def test_unsupported_extension(self):
        valid, msg = validate_source_file("/path/to/file.txt")
        assert not valid
        assert "not supported" in msg.lower()

    def test_nonexistent_file(self):
        valid, msg = validate_source_file("/nonexistent/video.mp4")
        assert not valid
        assert "cannot be read" in msg.lower()

    def test_valid_file(self):
        with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as f:
            f.write(b"fake video data")
            path = f.name
        try:
            valid, msg = validate_source_file(path)
            assert valid
            assert msg == ""
        finally:
            os.unlink(path)


class TestValidateTimeRange:

    def test_valid_range(self):
        valid, msg = validate_time_range(10.0, 20.0, 60.0)
        assert valid
        assert msg == ""

    def test_start_negative(self):
        valid, msg = validate_time_range(-1.0, 10.0, 60.0)
        assert not valid
        assert "negative" in msg.lower()

    def test_end_before_start(self):
        valid, msg = validate_time_range(20.0, 10.0, 60.0)
        assert not valid
        assert "greater than start" in msg.lower()

    def test_end_equals_start(self):
        valid, msg = validate_time_range(10.0, 10.0, 60.0)
        assert not valid
        assert "greater than start" in msg.lower()

    def test_end_exceeds_duration(self):
        valid, msg = validate_time_range(10.0, 70.0, 60.0)
        assert not valid
        assert "exceeds" in msg.lower()

    def test_too_short_clip(self):
        valid, msg = validate_time_range(10.0, 10.1, 60.0)
        assert not valid
        assert "too short" in msg.lower()

    def test_minimum_valid_clip(self):
        valid, msg = validate_time_range(10.0, 10.0 + MIN_CLIP_DURATION, 60.0)
        assert valid

    def test_full_duration(self):
        valid, msg = validate_time_range(0.0, 60.0, 60.0)
        assert valid

    def test_zero_duration_allows_any_end(self):
        """When duration is 0 (unknown), skip the duration check."""
        valid, msg = validate_time_range(0.0, 100.0, 0.0)
        assert valid


class TestValidateOutputPath:

    def test_empty_path(self):
        valid, msg = validate_output_path("")
        assert not valid
        assert "choose a save location" in msg.lower()

    def test_non_wav_extension(self):
        valid, msg = validate_output_path("/tmp/output.mp3")
        assert not valid
        assert ".wav" in msg

    def test_unwritable_directory(self):
        valid, msg = validate_output_path("/nonexistent/dir/output.wav")
        assert not valid
        assert "cannot be written" in msg.lower()

    def test_valid_path(self):
        path = os.path.join(tempfile.gettempdir(), "test_output.wav")
        valid, msg = validate_output_path(path)
        assert valid
        assert msg == ""


class TestValidateExtractionReady:

    def test_all_valid(self):
        with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as f:
            f.write(b"fake")
            source = f.name
        output = os.path.join(tempfile.gettempdir(), "out.wav")
        try:
            valid, msg = validate_extraction_ready(source, 0.0, 10.0, 60.0, output)
            assert valid
            assert msg == ""
        finally:
            os.unlink(source)

    def test_missing_source_fails_first(self):
        output = os.path.join(tempfile.gettempdir(), "out.wav")
        valid, msg = validate_extraction_ready("", 0.0, 10.0, 60.0, output)
        assert not valid
        assert "select a video" in msg.lower()

    def test_invalid_range_caught(self):
        with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as f:
            f.write(b"fake")
            source = f.name
        output = os.path.join(tempfile.gettempdir(), "out.wav")
        try:
            valid, msg = validate_extraction_ready(source, 20.0, 10.0, 60.0, output)
            assert not valid
            assert "greater than start" in msg.lower()
        finally:
            os.unlink(source)

    def test_missing_output_caught(self):
        with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as f:
            f.write(b"fake")
            source = f.name
        try:
            valid, msg = validate_extraction_ready(source, 0.0, 10.0, 60.0, "")
            assert not valid
            assert "save location" in msg.lower()
        finally:
            os.unlink(source)

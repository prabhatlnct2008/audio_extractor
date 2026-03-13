"""Unit tests for services/audio_extractor.py."""

import os
import tempfile
import pytest
from services.audio_extractor import extract_audio


class TestExtractAudio:

    def test_nonexistent_source_raises(self):
        with pytest.raises(ValueError, match="Source file not found"):
            extract_audio("/nonexistent/video.mp4", "/tmp/out.wav", 0, 10)

    def test_negative_start_raises(self):
        with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as f:
            f.write(b"fake")
            path = f.name
        try:
            with pytest.raises(ValueError, match="start_seconds must be >= 0"):
                extract_audio(path, "/tmp/out.wav", -1, 10)
        finally:
            os.unlink(path)

    def test_end_before_start_raises(self):
        with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as f:
            f.write(b"fake")
            path = f.name
        try:
            with pytest.raises(ValueError, match="must be greater than"):
                extract_audio(path, "/tmp/out.wav", 20, 10)
        finally:
            os.unlink(path)

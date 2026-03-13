"""Unit tests for utils/file_utils.py."""

import os
import tempfile
import pytest
from utils.file_utils import (
    ensure_wav_extension,
    is_supported_video,
    is_file_readable,
    is_directory_writable,
    get_display_path,
)


class TestEnsureWavExtension:
    """Tests for ensure_wav_extension()."""

    def test_no_extension(self):
        assert ensure_wav_extension("/path/to/file") == "/path/to/file.wav"

    def test_already_wav(self):
        assert ensure_wav_extension("/path/to/file.wav") == "/path/to/file.wav"

    def test_wav_uppercase(self):
        assert ensure_wav_extension("/path/to/file.WAV") == "/path/to/file.WAV"

    def test_wrong_extension(self):
        assert ensure_wav_extension("/path/to/file.mp3") == "/path/to/file.mp3.wav"

    def test_empty_string(self):
        assert ensure_wav_extension("") == ""

    def test_filename_only(self):
        assert ensure_wav_extension("output") == "output.wav"


class TestIsSupportedVideo:
    """Tests for is_supported_video()."""

    def test_mp4(self):
        assert is_supported_video("video.mp4") is True

    def test_mov(self):
        assert is_supported_video("video.mov") is True

    def test_avi(self):
        assert is_supported_video("video.avi") is True

    def test_mkv(self):
        assert is_supported_video("video.mkv") is True

    def test_webm(self):
        assert is_supported_video("video.webm") is True

    def test_wav_not_video(self):
        assert is_supported_video("audio.wav") is False

    def test_txt_not_video(self):
        assert is_supported_video("file.txt") is False

    def test_no_extension(self):
        assert is_supported_video("videofile") is False

    def test_empty(self):
        assert is_supported_video("") is False

    def test_case_insensitive(self):
        assert is_supported_video("video.MP4") is True


class TestIsFileReadable:
    """Tests for is_file_readable()."""

    def test_readable_file(self):
        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(b"test")
            path = f.name
        try:
            assert is_file_readable(path) is True
        finally:
            os.unlink(path)

    def test_nonexistent_file(self):
        assert is_file_readable("/nonexistent/path/file.mp4") is False

    def test_directory_not_file(self):
        assert is_file_readable(tempfile.gettempdir()) is False


class TestIsDirectoryWritable:
    """Tests for is_directory_writable()."""

    def test_writable_directory(self):
        path = os.path.join(tempfile.gettempdir(), "test_output.wav")
        assert is_directory_writable(path) is True

    def test_nonexistent_directory(self):
        assert is_directory_writable("/nonexistent/dir/file.wav") is False


class TestGetDisplayPath:
    """Tests for get_display_path()."""

    def test_short_path(self):
        path = "/short/path.mp4"
        assert get_display_path(path) == path

    def test_long_path_truncated(self):
        path = "/very/long/path/that/goes/on/and/on/and/on/for/a/really/really/long/time/video.mp4"
        result = get_display_path(path, max_length=40)
        assert len(result) <= 40
        assert "video.mp4" in result

    def test_empty_path(self):
        assert get_display_path("") == ""

    def test_none_path(self):
        assert get_display_path(None) is None

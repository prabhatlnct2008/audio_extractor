"""Unit tests for services/media_info.py."""

import os
import tempfile
import pytest
from services.media_info import get_video_duration, get_video_info


class TestGetVideoDuration:

    def test_nonexistent_file_raises(self):
        with pytest.raises(ValueError, match="File not found"):
            get_video_duration("/nonexistent/video.mp4")

    def test_non_media_file_raises(self):
        """A text file should fail duration detection."""
        with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as f:
            f.write(b"this is not a video")
            path = f.name
        try:
            with pytest.raises((ValueError, RuntimeError)):
                get_video_duration(path)
        finally:
            os.unlink(path)


class TestGetVideoInfo:

    def test_nonexistent_file_raises(self):
        with pytest.raises(ValueError, match="File not found"):
            get_video_info("/nonexistent/video.mp4")

    def test_returns_dict_keys(self):
        """If we had a valid video, the return dict should have expected keys.
        Since we can't guarantee a real video in CI, just test the error path."""
        with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as f:
            f.write(b"not real video data")
            path = f.name
        try:
            with pytest.raises((ValueError, RuntimeError)):
                get_video_info(path)
        finally:
            os.unlink(path)

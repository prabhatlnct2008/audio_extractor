"""Centralized validation rules for the Audio Clip Extractor.

All validation functions return a tuple of (is_valid: bool, message: str).
On success, message is empty. On failure, message is a plain-language,
actionable error description.
"""

import os
from utils.file_utils import is_supported_video, is_file_readable, is_directory_writable

# Minimum clip duration in seconds to prevent accidental micro-selections
MIN_CLIP_DURATION = 0.5


def validate_source_file(file_path: str) -> tuple[bool, str]:
    """Validate that a source video file is selected and usable.

    Checks:
        - Path is not empty
        - File has a supported video extension
        - File exists and is readable
    """
    if not file_path:
        return False, "Please select a video file before extracting."

    if not is_supported_video(file_path):
        _, ext = os.path.splitext(file_path)
        return False, (
            f"The file type '{ext}' is not supported. "
            "Please select a video file (.mp4, .mov, .avi, .mkv, etc.)."
        )

    if not is_file_readable(file_path):
        return False, (
            "The selected video file cannot be read. "
            "Please check that the file exists and you have permission to open it."
        )

    return True, ""


def validate_time_range(
    start_seconds: float,
    end_seconds: float,
    duration: float,
) -> tuple[bool, str]:
    """Validate that the clip time range is valid.

    Checks:
        - Start >= 0
        - End > start
        - End <= duration
        - Clip duration >= MIN_CLIP_DURATION
    """
    if start_seconds < 0:
        return False, "Start time cannot be negative."

    if end_seconds <= start_seconds:
        return False, "End time must be greater than start time."

    if duration > 0 and end_seconds > duration:
        return False, (
            f"End time ({end_seconds:.1f}s) exceeds the video duration "
            f"({duration:.1f}s). Please select a range within the video."
        )

    clip_length = end_seconds - start_seconds
    if clip_length < MIN_CLIP_DURATION:
        return False, (
            f"Selected clip is too short ({clip_length:.2f}s). "
            f"Minimum clip duration is {MIN_CLIP_DURATION}s."
        )

    return True, ""


def validate_output_path(output_path: str) -> tuple[bool, str]:
    """Validate the output save path.

    Checks:
        - Path is not empty
        - Path ends with .wav
        - Parent directory exists and is writable
    """
    if not output_path:
        return False, "Please choose a save location before extracting."

    _, ext = os.path.splitext(output_path)
    if ext.lower() != ".wav":
        return False, "Output file must have a .wav extension."

    if not is_directory_writable(output_path):
        return False, (
            "The selected save location cannot be written to. "
            "Please choose a different folder."
        )

    return True, ""


def validate_extraction_ready(
    source_path: str,
    start_seconds: float,
    end_seconds: float,
    duration: float,
    output_path: str,
) -> tuple[bool, str]:
    """Validate that all preconditions for extraction are met.

    Runs all individual validations and returns the first failure found.
    """
    valid, msg = validate_source_file(source_path)
    if not valid:
        return False, msg

    valid, msg = validate_time_range(start_seconds, end_seconds, duration)
    if not valid:
        return False, msg

    valid, msg = validate_output_path(output_path)
    if not valid:
        return False, msg

    return True, ""

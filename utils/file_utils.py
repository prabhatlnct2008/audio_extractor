"""File path and extension utilities for the Audio Clip Extractor."""

import os

# Video file extensions accepted in the file picker
SUPPORTED_VIDEO_EXTENSIONS = {
    ".mp4", ".mov", ".avi", ".mkv", ".webm", ".flv", ".wmv",
    ".m4v", ".mpg", ".mpeg", ".3gp",
}

SUPPORTED_VIDEO_FILETYPES = [
    ("Video files", " ".join(f"*{ext}" for ext in sorted(SUPPORTED_VIDEO_EXTENSIONS))),
    ("All files", "*.*"),
]

WAV_EXTENSION = ".wav"


def ensure_wav_extension(file_path: str) -> str:
    """Ensure the file path ends with .wav extension.

    If the path already has .wav (case-insensitive), returns it unchanged.
    Otherwise appends .wav.

    Args:
        file_path: The file path to check.

    Returns:
        File path guaranteed to end with .wav.
    """
    if not file_path:
        return file_path

    _, ext = os.path.splitext(file_path)
    if ext.lower() == WAV_EXTENSION:
        return file_path
    return file_path + WAV_EXTENSION


def is_supported_video(file_path: str) -> bool:
    """Check if the file has a supported video extension.

    Args:
        file_path: Path to check.

    Returns:
        True if the file extension is in the supported set.
    """
    if not file_path:
        return False
    _, ext = os.path.splitext(file_path)
    return ext.lower() in SUPPORTED_VIDEO_EXTENSIONS


def is_file_readable(file_path: str) -> bool:
    """Check if the file exists and is readable.

    Args:
        file_path: Path to check.

    Returns:
        True if the file exists and can be read.
    """
    return os.path.isfile(file_path) and os.access(file_path, os.R_OK)


def is_directory_writable(file_path: str) -> bool:
    """Check if the parent directory of the given path is writable.

    Args:
        file_path: Full file path whose parent directory to check.

    Returns:
        True if the parent directory exists and is writable.
    """
    parent_dir = os.path.dirname(file_path)
    if not parent_dir:
        parent_dir = "."
    return os.path.isdir(parent_dir) and os.access(parent_dir, os.W_OK)


def get_display_path(file_path: str, max_length: int = 60) -> str:
    """Get a display-friendly version of a file path.

    If the path is longer than max_length, truncates from the middle
    with an ellipsis.

    Args:
        file_path: Full file path.
        max_length: Maximum display length.

    Returns:
        Truncated or full path string.
    """
    if not file_path or len(file_path) <= max_length:
        return file_path

    filename = os.path.basename(file_path)
    if len(filename) >= max_length - 3:
        return "..." + filename[-(max_length - 3):]

    remaining = max_length - len(filename) - 5  # 5 for "/.../"
    return file_path[:remaining] + "/.../" + filename

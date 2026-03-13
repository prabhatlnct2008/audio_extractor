"""Service module for detecting video file metadata using ffprobe."""

import os
import subprocess


def get_video_duration(file_path: str) -> float:
    """Return the duration of a video file in seconds.

    Uses ffprobe to read the container-level duration.

    Args:
        file_path: Absolute or relative path to the video file.

    Returns:
        Duration in seconds as a float.

    Raises:
        ValueError: If the file does not exist, ffprobe returns invalid data,
                    or the probe process exits with a non-zero status.
        RuntimeError: If ffprobe is not installed on the system.
    """
    if not os.path.isfile(file_path):
        raise ValueError(f"File not found: {file_path}")

    cmd = [
        "ffprobe",
        "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        file_path,
    ]

    try:
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=30,
        )
    except FileNotFoundError:
        raise RuntimeError(
            "FFmpeg/ffprobe is not installed. "
            "Please install FFmpeg (https://ffmpeg.org) and ensure it is on your PATH."
        )
    except subprocess.TimeoutExpired:
        raise ValueError(
            f"ffprobe timed out while reading '{file_path}'. "
            "The file may be corrupt or extremely large."
        )

    if result.returncode != 0:
        stderr = result.stderr.strip()
        raise ValueError(
            f"ffprobe failed for '{file_path}' (exit code {result.returncode}): {stderr}"
        )

    raw = result.stdout.strip()
    if not raw:
        raise ValueError(
            f"ffprobe returned no duration for '{file_path}'. "
            "The file may not be a valid media file."
        )

    try:
        duration = float(raw)
    except ValueError:
        raise ValueError(
            f"ffprobe returned invalid duration '{raw}' for '{file_path}'."
        )

    if duration < 0:
        raise ValueError(
            f"ffprobe returned a negative duration ({duration}) for '{file_path}'."
        )

    return duration


def get_video_info(file_path: str) -> dict:
    """Return basic metadata about a video file.

    Args:
        file_path: Absolute or relative path to the video file.

    Returns:
        A dict with keys ``duration`` (float, seconds), ``filename`` (str),
        and ``path`` (str, absolute path).

    Raises:
        ValueError: If the file does not exist or cannot be probed.
        RuntimeError: If ffprobe is not installed.
    """
    abs_path = os.path.abspath(file_path)
    duration = get_video_duration(abs_path)

    return {
        "duration": duration,
        "filename": os.path.basename(abs_path),
        "path": abs_path,
    }

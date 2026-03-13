"""Time parsing, formatting, and conversion utilities for the Audio Clip Extractor.

Supports time formats: SS, MM:SS, HH:MM:SS
All internal time values are represented as float seconds.
"""

import re


# Matches HH:MM:SS, MM:SS, or SS (with optional decimal)
_TIME_PATTERNS = [
    re.compile(r"^(\d+):([0-5]?\d):([0-5]?\d(?:\.\d+)?)$"),   # HH:MM:SS
    re.compile(r"^(\d+):([0-5]?\d(?:\.\d+)?)$"),                # MM:SS
    re.compile(r"^(\d+(?:\.\d+)?)$"),                            # SS
]


def parse_time(time_str: str) -> float:
    """Parse a time string into seconds.

    Accepted formats:
        - "SS" or "SS.ms"       (e.g., "90", "90.5")
        - "MM:SS" or "MM:SS.ms" (e.g., "1:30", "1:30.5")
        - "HH:MM:SS" or "HH:MM:SS.ms" (e.g., "1:02:30")

    Returns:
        Total time in seconds as a float.

    Raises:
        ValueError: If the time string is empty, has an invalid format,
                    or produces a negative value.
    """
    if not isinstance(time_str, str):
        raise ValueError("Time value must be a string.")

    time_str = time_str.strip()
    if not time_str:
        raise ValueError("Time value cannot be empty.")

    # Try HH:MM:SS
    match = _TIME_PATTERNS[0].match(time_str)
    if match:
        hours, minutes, seconds = match.groups()
        total = int(hours) * 3600 + int(minutes) * 60 + float(seconds)
        return total

    # Try MM:SS
    match = _TIME_PATTERNS[1].match(time_str)
    if match:
        minutes, seconds = match.groups()
        total = int(minutes) * 60 + float(seconds)
        return total

    # Try SS
    match = _TIME_PATTERNS[2].match(time_str)
    if match:
        total = float(match.group(1))
        return total

    raise ValueError(
        f"Invalid time format: '{time_str}'. "
        "Use SS, MM:SS, or HH:MM:SS format."
    )


def format_time(seconds: float) -> str:
    """Format seconds into HH:MM:SS.d display string.

    Always shows HH:MM:SS format with one decimal place for consistency.

    Args:
        seconds: Time in seconds (must be >= 0).

    Returns:
        Formatted time string like "00:02:30.5".

    Raises:
        ValueError: If seconds is negative.
    """
    if seconds < 0:
        raise ValueError("Time cannot be negative.")

    total_seconds = seconds
    hours = int(total_seconds // 3600)
    remaining = total_seconds - hours * 3600
    minutes = int(remaining // 60)
    secs = remaining - minutes * 60

    return f"{hours:02d}:{minutes:02d}:{secs:04.1f}"


def format_time_short(seconds: float) -> str:
    """Format seconds into the shortest readable form.

    - If < 1 hour: MM:SS.d
    - If >= 1 hour: HH:MM:SS.d

    Args:
        seconds: Time in seconds (must be >= 0).

    Returns:
        Formatted time string.
    """
    if seconds < 0:
        raise ValueError("Time cannot be negative.")

    hours = int(seconds // 3600)
    remaining = seconds - hours * 3600
    minutes = int(remaining // 60)
    secs = remaining - minutes * 60

    if hours > 0:
        return f"{hours:d}:{minutes:02d}:{secs:04.1f}"
    else:
        return f"{minutes:d}:{secs:04.1f}"


def format_duration(seconds: float) -> str:
    """Format a duration in seconds to a human-readable string.

    Examples: "2.5s", "1m 30.0s", "1h 2m 30.0s"
    """
    if seconds < 0:
        raise ValueError("Duration cannot be negative.")

    hours = int(seconds // 3600)
    remaining = seconds - hours * 3600
    minutes = int(remaining // 60)
    secs = remaining - minutes * 60

    parts = []
    if hours > 0:
        parts.append(f"{hours}h")
    if minutes > 0:
        parts.append(f"{minutes}m")
    parts.append(f"{secs:.1f}s")

    return " ".join(parts)


def clamp(value: float, min_val: float, max_val: float) -> float:
    """Clamp a value between min_val and max_val."""
    return max(min_val, min(value, max_val))

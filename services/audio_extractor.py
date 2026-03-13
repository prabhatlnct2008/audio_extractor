"""Service module for extracting audio segments from video files using FFmpeg."""

import os
import subprocess
import threading
from typing import Callable, Optional


def extract_audio(
    source_path: str,
    output_path: str,
    start_seconds: float,
    end_seconds: float,
) -> str:
    """Extract an audio segment from a video file to a WAV file.

    Uses FFmpeg to decode the video, select the time range, and write
    uncompressed 16-bit PCM audio at 44.1 kHz stereo.

    Args:
        source_path:   Path to the source video file.
        output_path:   Destination path for the extracted WAV file.
        start_seconds: Start of the segment in seconds.
        end_seconds:   End of the segment in seconds.

    Returns:
        The *output_path* on success (same value that was passed in).

    Raises:
        ValueError:  If arguments are invalid or FFmpeg returns an error.
        RuntimeError: If FFmpeg is not installed on the system.
    """
    # ---- input validation ----
    if not os.path.isfile(source_path):
        raise ValueError(f"Source file not found: {source_path}")

    if start_seconds < 0:
        raise ValueError(f"start_seconds must be >= 0, got {start_seconds}")

    if end_seconds <= start_seconds:
        raise ValueError(
            f"end_seconds ({end_seconds}) must be greater than "
            f"start_seconds ({start_seconds})"
        )

    # Ensure the output directory exists
    output_dir = os.path.dirname(output_path)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    cmd = [
        "ffmpeg",
        "-y",                   # overwrite output without asking
        "-i", source_path,
        "-ss", str(start_seconds),
        "-to", str(end_seconds),
        "-vn",                  # drop video stream
        "-acodec", "pcm_s16le",
        "-ar", "44100",
        "-ac", "2",
        output_path,
    ]

    try:
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=300,
        )
    except FileNotFoundError:
        raise RuntimeError(
            "FFmpeg is not installed. "
            "Please install FFmpeg (https://ffmpeg.org) and ensure it is on your PATH."
        )
    except subprocess.TimeoutExpired:
        raise ValueError(
            "FFmpeg timed out while extracting audio. "
            "The source file may be corrupt or the segment too large."
        )

    if result.returncode != 0:
        stderr = result.stderr.strip()
        raise ValueError(
            f"FFmpeg failed (exit code {result.returncode}): {stderr}"
        )

    if not os.path.isfile(output_path):
        raise ValueError(
            f"FFmpeg reported success but the output file was not created: {output_path}"
        )

    return output_path


def extract_audio_async(
    source_path: str,
    output_path: str,
    start_seconds: float,
    end_seconds: float,
    on_complete: Optional[Callable[[str], None]] = None,
    on_error: Optional[Callable[[str], None]] = None,
) -> threading.Thread:
    """Run :func:`extract_audio` in a background daemon thread.

    Args:
        source_path:   Path to the source video file.
        output_path:   Destination path for the extracted WAV file.
        start_seconds: Start of the segment in seconds.
        end_seconds:   End of the segment in seconds.
        on_complete:   Called with *output_path* when extraction succeeds.
        on_error:      Called with an error message string on failure.

    Returns:
        The started :class:`threading.Thread` instance (daemon).
    """

    def _worker() -> None:
        try:
            result_path = extract_audio(
                source_path, output_path, start_seconds, end_seconds
            )
            if on_complete is not None:
                on_complete(result_path)
        except Exception as exc:
            if on_error is not None:
                on_error(str(exc))

    thread = threading.Thread(target=_worker, daemon=True)
    thread.start()
    return thread

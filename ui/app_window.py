"""Main application window for the Audio Clip Extractor.

Composes all UI sections and wires them together for the complete
extraction workflow: open video -> set range -> choose save -> extract.
"""

import os
import subprocess
import sys
import tkinter as tk
from typing import Optional

from ui.source_section import SourceSection
from ui.timeline import Timeline
from ui.time_display import TimeDisplay
from ui.output_section import OutputSection
from ui.action_section import ActionSection
from ui.status_bar import StatusBar
from services.media_info import get_video_info
from services.audio_extractor import extract_audio_async
from services.validation import validate_extraction_ready


class AppWindow(tk.Frame):
    """Top-level application frame containing all UI sections.

    Manages application state and coordinates interactions between
    sections for the full extraction workflow.
    """

    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

        # Application state
        self._source_path: Optional[str] = None
        self._duration: float = 0.0
        self._start_time: float = 0.0
        self._end_time: float = 0.0
        self._output_path: Optional[str] = None
        self._is_extracting: bool = False

        self._build_ui()

    def _build_ui(self) -> None:
        """Create and pack all sections, then wire callbacks."""

        # 1. Source File
        source_frame = tk.LabelFrame(self, text="Source File", padx=4, pady=4)
        source_frame.pack(fill=tk.X, padx=8, pady=(8, 4))

        self.source_section = SourceSection(source_frame)
        self.source_section.pack(fill=tk.X)
        self.source_section.on_file_selected = self._on_file_selected

        # 2. Timeline
        timeline_frame = tk.LabelFrame(self, text="Timeline", padx=4, pady=4)
        timeline_frame.pack(fill=tk.X, padx=8, pady=4)

        self.timeline = Timeline(timeline_frame)
        self.timeline.pack(fill=tk.X, expand=True)
        self.timeline.on_range_changed = self._on_range_changed

        # 3. Time Display / Fine Adjustment
        time_frame = tk.LabelFrame(
            self, text="Clip Range", padx=4, pady=4
        )
        time_frame.pack(fill=tk.X, padx=8, pady=4)

        self.time_display = TimeDisplay(time_frame)
        self.time_display.pack(fill=tk.X)
        self.time_display.set_enabled(False)
        self.time_display.on_time_edited = self._on_time_edited

        # 4. Output
        output_frame = tk.LabelFrame(self, text="Output", padx=4, pady=4)
        output_frame.pack(fill=tk.X, padx=8, pady=4)

        self.output_section = OutputSection(output_frame)
        self.output_section.pack(fill=tk.X)
        self.output_section.on_save_selected = self._on_save_selected

        # 5. Action
        action_frame = tk.Frame(self, padx=4, pady=4)
        action_frame.pack(fill=tk.X, padx=8, pady=4)

        self.action_section = ActionSection(action_frame)
        self.action_section.pack(fill=tk.X)
        self.action_section._extract_btn.config(command=self._on_extract)
        self.action_section._reset_btn.config(command=self._on_reset)

        # 6. Status
        self.status_bar = StatusBar(self, relief=tk.SUNKEN, bd=1)
        self.status_bar.pack(fill=tk.X, side=tk.BOTTOM, padx=8, pady=(4, 8))

    # ------------------------------------------------------------------
    # Source file handling
    # ------------------------------------------------------------------

    def _on_file_selected(self, file_path: str) -> None:
        """Handle a new source video file being chosen."""
        self.status_bar.set_status("Loading video info...", "processing")

        try:
            info = get_video_info(file_path)
        except (ValueError, RuntimeError) as e:
            self.status_bar.set_status(str(e), "error")
            return

        self._source_path = info["path"]
        self._duration = info["duration"]

        # Activate timeline with the video duration
        self.timeline.set_duration(self._duration)
        self._start_time = 0.0
        self._end_time = self._duration

        # Activate time display
        self.time_display.set_duration(self._duration)
        self.time_display.set_enabled(True)
        self.time_display.update_from_timeline(0.0, self._duration)

        # Enable extract button
        self.action_section._extract_btn.config(state=tk.NORMAL)

        from utils.time_utils import format_duration
        dur_str = format_duration(self._duration)
        self.status_bar.set_status(
            f"Video loaded: {info['filename']} ({dur_str})", "info"
        )

    # ------------------------------------------------------------------
    # Timeline <-> Time Display sync
    # ------------------------------------------------------------------

    def _on_range_changed(self, start: float, end: float) -> None:
        """Called when the timeline handles are dragged."""
        self._start_time = start
        self._end_time = end
        self.time_display.update_from_timeline(start, end)

    def _on_time_edited(self, start: float, end: float) -> None:
        """Called when user manually edits time fields."""
        self._start_time = start
        self._end_time = end
        # Update timeline handle positions (no recursive callback due to guard)
        self.timeline.set_range(start, end)

    # ------------------------------------------------------------------
    # Output path handling
    # ------------------------------------------------------------------

    def _on_save_selected(self, path: str) -> None:
        """Called when save location is chosen."""
        self._output_path = path
        self.status_bar.set_status(f"Save location: {path}", "info")

    # ------------------------------------------------------------------
    # Extraction workflow
    # ------------------------------------------------------------------

    def _on_extract(self) -> None:
        """Validate and start the audio extraction."""
        if self._is_extracting:
            return

        # Run full validation
        valid, msg = validate_extraction_ready(
            self._source_path or "",
            self._start_time,
            self._end_time,
            self._duration,
            self._output_path or "",
        )

        if not valid:
            self.status_bar.set_status(msg, "error")
            return

        # Begin extraction
        self._is_extracting = True
        self.action_section.set_extracting(True)
        self.status_bar.set_status("Extracting audio...", "processing")

        # Run in background thread
        extract_audio_async(
            source_path=self._source_path,
            output_path=self._output_path,
            start_seconds=self._start_time,
            end_seconds=self._end_time,
            on_complete=self._extraction_complete,
            on_error=self._extraction_failed,
        )

    def _extraction_complete(self, output_path: str) -> None:
        """Called from background thread on success. Schedule UI update."""
        self.after(0, self._show_extraction_success, output_path)

    def _extraction_failed(self, error_message: str) -> None:
        """Called from background thread on failure. Schedule UI update."""
        self.after(0, self._show_extraction_error, error_message)

    def _show_extraction_success(self, output_path: str) -> None:
        """Update UI after successful extraction (on main thread)."""
        self._is_extracting = False
        self.action_section.set_extracting(False)
        self.status_bar.set_status(
            f"Audio extracted successfully! Saved to: {output_path}",
            "success",
        )

    def _show_extraction_error(self, error_message: str) -> None:
        """Update UI after extraction failure (on main thread)."""
        self._is_extracting = False
        self.action_section.set_extracting(False)
        self.status_bar.set_status(
            f"Extraction failed: {error_message}", "error"
        )

    # ------------------------------------------------------------------
    # Reset
    # ------------------------------------------------------------------

    def _on_reset(self) -> None:
        """Reset all fields to initial state."""
        if self._is_extracting:
            return

        self._source_path = None
        self._duration = 0.0
        self._start_time = 0.0
        self._end_time = 0.0
        self._output_path = None

        self.source_section.reset()
        self.timeline.reset()
        self.time_display.reset()
        self.output_section.reset()
        self.action_section._extract_btn.config(state=tk.DISABLED)
        self.status_bar.set_status("Ready", "ready")

"""Time display and manual entry section for the Audio Clip Extractor.

Shows start time, end time, and clip duration. Supports editable fields
that sync bidirectionally with the timeline handles.
"""

import tkinter as tk
from typing import Callable, Optional

from utils.time_utils import parse_time, format_time, format_duration


class TimeDisplay(tk.Frame):
    """Displays start/end times and clip duration with editable fields.

    The fields sync bidirectionally with the timeline:
    - Timeline drag updates the fields
    - Editing a field and pressing Enter/Tab updates the timeline
    """

    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

        # Callback: called with (start_seconds, end_seconds) when user edits fields
        self.on_time_edited: Optional[Callable[[float, float], None]] = None

        # Guard flag to prevent recursive updates
        self._updating = False

        self._duration: float = 0.0
        self._start_seconds: float = 0.0
        self._end_seconds: float = 0.0

        self._build_ui()

    def _build_ui(self) -> None:
        row = tk.Frame(self)
        row.pack(fill=tk.X, padx=6, pady=4)

        # Start time
        tk.Label(row, text="Start:").pack(side=tk.LEFT, padx=(0, 4))

        self._start_var = tk.StringVar(value="00:00:00.0")
        self._start_entry = tk.Entry(
            row, textvariable=self._start_var, width=12,
            justify=tk.CENTER
        )
        self._start_entry.pack(side=tk.LEFT, padx=(0, 16))
        self._start_entry.bind("<Return>", self._on_entry_commit)
        self._start_entry.bind("<FocusOut>", self._on_entry_commit)

        # End time
        tk.Label(row, text="End:").pack(side=tk.LEFT, padx=(0, 4))

        self._end_var = tk.StringVar(value="00:00:00.0")
        self._end_entry = tk.Entry(
            row, textvariable=self._end_var, width=12,
            justify=tk.CENTER
        )
        self._end_entry.pack(side=tk.LEFT, padx=(0, 16))
        self._end_entry.bind("<Return>", self._on_entry_commit)
        self._end_entry.bind("<FocusOut>", self._on_entry_commit)

        # Clip duration display
        tk.Label(row, text="Duration:").pack(side=tk.LEFT, padx=(0, 4))

        self._duration_label = tk.Label(
            row, text="0.0s", fg="#555555"
        )
        self._duration_label.pack(side=tk.LEFT)

        # Helper text
        self._helper_label = tk.Label(
            self, text="Format: SS, MM:SS, or HH:MM:SS",
            fg="#999999", font=("TkDefaultFont", 8)
        )
        self._helper_label.pack(anchor=tk.W, padx=6)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def update_from_timeline(self, start_seconds: float, end_seconds: float) -> None:
        """Update display fields from timeline drag (external update).

        Uses a guard flag to prevent triggering on_time_edited back.
        """
        if self._updating:
            return

        self._updating = True
        try:
            self._start_seconds = start_seconds
            self._end_seconds = end_seconds

            self._start_var.set(format_time(start_seconds))
            self._end_var.set(format_time(end_seconds))

            clip_len = end_seconds - start_seconds
            self._duration_label.config(text=format_duration(max(0, clip_len)))
        finally:
            self._updating = False

    def set_duration(self, duration: float) -> None:
        """Store the video duration for validation of manual entries."""
        self._duration = duration

    def set_enabled(self, enabled: bool) -> None:
        """Enable or disable the entry fields."""
        state = tk.NORMAL if enabled else tk.DISABLED
        self._start_entry.config(state=state)
        self._end_entry.config(state=state)

    def reset(self) -> None:
        """Reset fields to initial state."""
        self._duration = 0.0
        self._start_seconds = 0.0
        self._end_seconds = 0.0
        self._start_var.set("00:00:00.0")
        self._end_var.set("00:00:00.0")
        self._duration_label.config(text="0.0s")
        self.set_enabled(False)

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    def _on_entry_commit(self, event: tk.Event) -> None:
        """Handle manual time entry when user presses Enter or leaves field."""
        if self._updating:
            return

        self._updating = True
        try:
            new_start = self._parse_field(self._start_var.get(), self._start_seconds)
            new_end = self._parse_field(self._end_var.get(), self._end_seconds)

            # Clamp to valid range
            if self._duration > 0:
                new_start = max(0.0, min(new_start, self._duration - 0.5))
                new_end = max(new_start + 0.5, min(new_end, self._duration))

            self._start_seconds = new_start
            self._end_seconds = new_end

            # Update display to show the validated values
            self._start_var.set(format_time(new_start))
            self._end_var.set(format_time(new_end))

            clip_len = new_end - new_start
            self._duration_label.config(text=format_duration(max(0, clip_len)))

            # Notify parent to update timeline
            if self.on_time_edited is not None:
                self.on_time_edited(new_start, new_end)
        finally:
            self._updating = False

    def _parse_field(self, value: str, fallback: float) -> float:
        """Parse a time field value, returning fallback on failure."""
        try:
            return parse_time(value)
        except ValueError:
            return fallback

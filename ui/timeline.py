"""Custom draggable timeline widget for selecting audio clip range.

The timeline displays the full video duration as a horizontal track,
with draggable start and end handles. The selected region between the
handles is highlighted. Handle positions are synchronized with time
values via callbacks.
"""

import tkinter as tk
from typing import Callable, Optional

from utils.time_utils import format_time_short, clamp

# Visual constants
TRACK_HEIGHT = 8
HANDLE_WIDTH = 12
HANDLE_HEIGHT = 28
TRACK_COLOR = "#cccccc"
SELECTED_COLOR = "#4a90d9"
HANDLE_COLOR_START = "#2e7d32"
HANDLE_COLOR_END = "#c62828"
DISABLED_COLOR = "#e0e0e0"
LABEL_FONT = ("TkDefaultFont", 9)
PADDING_X = 20
PADDING_TOP = 25
PADDING_BOTTOM = 25
MIN_HANDLE_GAP_SECONDS = 0.5  # Minimum gap between handles


class Timeline(tk.Canvas):
    """A Canvas-based timeline with draggable start/end handles.

    Usage:
        timeline = Timeline(parent)
        timeline.set_duration(120.0)  # Activate with 2-minute video
        timeline.on_range_changed = callback  # (start_s, end_s) -> None
    """

    def __init__(self, parent, **kwargs):
        kwargs.setdefault("height", 80)
        kwargs.setdefault("bg", "#f5f5f5")
        kwargs.setdefault("highlightthickness", 0)
        super().__init__(parent, **kwargs)

        self._duration: float = 0.0
        self._start_seconds: float = 0.0
        self._end_seconds: float = 0.0
        self._enabled: bool = False

        # Drag state
        self._dragging: Optional[str] = None  # "start", "end", or None

        # Callback: called with (start_seconds, end_seconds) when range changes
        self.on_range_changed: Optional[Callable[[float, float], None]] = None

        # Canvas item IDs (created on first draw)
        self._items_created = False

        # Bind events
        self.bind("<ButtonPress-1>", self._on_press)
        self.bind("<B1-Motion>", self._on_drag)
        self.bind("<ButtonRelease-1>", self._on_release)
        self.bind("<Configure>", self._on_resize)

        # Initial draw
        self.after(10, self._draw)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def set_duration(self, duration: float) -> None:
        """Set the total video duration and activate the timeline.

        Resets start to 0 and end to the full duration.
        """
        self._duration = duration
        self._start_seconds = 0.0
        self._end_seconds = duration
        self._enabled = duration > 0
        self._draw()
        self._notify_change()

    def set_range(self, start: float, end: float) -> None:
        """Set the clip range programmatically (e.g., from manual entry).

        Values are clamped to valid bounds. Used for bidirectional sync
        with the time display fields.
        """
        if not self._enabled:
            return

        start = clamp(start, 0.0, self._duration - MIN_HANDLE_GAP_SECONDS)
        end = clamp(end, start + MIN_HANDLE_GAP_SECONDS, self._duration)

        self._start_seconds = start
        self._end_seconds = end
        self._draw()

    def get_range(self) -> tuple[float, float]:
        """Return the current (start_seconds, end_seconds)."""
        return self._start_seconds, self._end_seconds

    def reset(self) -> None:
        """Reset the timeline to disabled state."""
        self._duration = 0.0
        self._start_seconds = 0.0
        self._end_seconds = 0.0
        self._enabled = False
        self._draw()

    # ------------------------------------------------------------------
    # Coordinate conversion
    # ------------------------------------------------------------------

    def _track_bounds(self) -> tuple[float, float, float, float]:
        """Return (x_left, y_top, x_right, y_bottom) of the track area."""
        w = self.winfo_width()
        h = self.winfo_height()
        x_left = PADDING_X
        x_right = w - PADDING_X
        y_center = h // 2
        y_top = y_center - TRACK_HEIGHT // 2
        y_bottom = y_center + TRACK_HEIGHT // 2
        return x_left, y_top, x_right, y_bottom

    def _seconds_to_x(self, seconds: float) -> float:
        """Convert a time value in seconds to an x-coordinate on the canvas."""
        x_left, _, x_right, _ = self._track_bounds()
        if self._duration <= 0:
            return x_left
        ratio = seconds / self._duration
        return x_left + ratio * (x_right - x_left)

    def _x_to_seconds(self, x: float) -> float:
        """Convert an x-coordinate on the canvas to a time value in seconds."""
        x_left, _, x_right, _ = self._track_bounds()
        track_width = x_right - x_left
        if track_width <= 0:
            return 0.0
        ratio = (x - x_left) / track_width
        return clamp(ratio * self._duration, 0.0, self._duration)

    # ------------------------------------------------------------------
    # Drawing
    # ------------------------------------------------------------------

    def _draw(self) -> None:
        """Redraw the entire timeline."""
        self.delete("all")

        w = self.winfo_width()
        h = self.winfo_height()
        if w < 50 or h < 30:
            return

        x_left, y_top, x_right, y_bottom = self._track_bounds()
        y_center = h // 2

        if not self._enabled:
            # Disabled state: gray track with "Load a video" message
            self.create_rectangle(
                x_left, y_top, x_right, y_bottom,
                fill=DISABLED_COLOR, outline="#bbbbbb", width=1
            )
            self.create_text(
                w // 2, y_center,
                text="Load a video to activate the timeline",
                fill="#999999", font=LABEL_FONT
            )
            return

        # Background track
        self.create_rectangle(
            x_left, y_top, x_right, y_bottom,
            fill=TRACK_COLOR, outline="#bbbbbb", width=1
        )

        # Selected region highlight
        start_x = self._seconds_to_x(self._start_seconds)
        end_x = self._seconds_to_x(self._end_seconds)

        self.create_rectangle(
            start_x, y_top, end_x, y_bottom,
            fill=SELECTED_COLOR, outline="", width=0
        )

        # Start handle
        self._draw_handle(start_x, y_center, HANDLE_COLOR_START, "start")

        # End handle
        self._draw_handle(end_x, y_center, HANDLE_COLOR_END, "end")

        # Time labels
        start_label = format_time_short(self._start_seconds)
        end_label = format_time_short(self._end_seconds)

        self.create_text(
            start_x, y_center + HANDLE_HEIGHT // 2 + 10,
            text=start_label, fill=HANDLE_COLOR_START, font=LABEL_FONT,
            anchor=tk.N
        )

        self.create_text(
            end_x, y_center + HANDLE_HEIGHT // 2 + 10,
            text=end_label, fill=HANDLE_COLOR_END, font=LABEL_FONT,
            anchor=tk.N
        )

        # Duration labels at track edges
        self.create_text(
            x_left, y_top - 8,
            text="0:00.0", fill="#888888", font=LABEL_FONT,
            anchor=tk.S
        )
        self.create_text(
            x_right, y_top - 8,
            text=format_time_short(self._duration), fill="#888888",
            font=LABEL_FONT, anchor=tk.S
        )

    def _draw_handle(self, x: float, y_center: float, color: str, tag: str) -> None:
        """Draw a single handle at the given x position."""
        half_w = HANDLE_WIDTH // 2
        half_h = HANDLE_HEIGHT // 2
        self.create_rectangle(
            x - half_w, y_center - half_h,
            x + half_w, y_center + half_h,
            fill=color, outline="#333333", width=1,
            tags=(tag, "handle")
        )

    # ------------------------------------------------------------------
    # Mouse event handling
    # ------------------------------------------------------------------

    def _on_press(self, event: tk.Event) -> None:
        """Begin dragging the nearest handle if the click is close enough."""
        if not self._enabled:
            return

        start_x = self._seconds_to_x(self._start_seconds)
        end_x = self._seconds_to_x(self._end_seconds)

        dist_start = abs(event.x - start_x)
        dist_end = abs(event.x - end_x)

        # Hit threshold: must be within handle width
        threshold = HANDLE_WIDTH + 4

        if dist_start <= threshold and dist_start <= dist_end:
            self._dragging = "start"
        elif dist_end <= threshold:
            self._dragging = "end"
        else:
            self._dragging = None

    def _on_drag(self, event: tk.Event) -> None:
        """Update handle position during drag."""
        if not self._enabled or self._dragging is None:
            return

        seconds = self._x_to_seconds(event.x)

        if self._dragging == "start":
            # Start handle: clamp to [0, end - MIN_GAP]
            max_start = self._end_seconds - MIN_HANDLE_GAP_SECONDS
            self._start_seconds = clamp(seconds, 0.0, max(0.0, max_start))
        elif self._dragging == "end":
            # End handle: clamp to [start + MIN_GAP, duration]
            min_end = self._start_seconds + MIN_HANDLE_GAP_SECONDS
            self._end_seconds = clamp(seconds, min_end, self._duration)

        self._draw()
        self._notify_change()

    def _on_release(self, event: tk.Event) -> None:
        """End the drag operation."""
        self._dragging = None

    def _on_resize(self, event: tk.Event) -> None:
        """Redraw when the canvas is resized."""
        self._draw()

    # ------------------------------------------------------------------
    # Notification
    # ------------------------------------------------------------------

    def _notify_change(self) -> None:
        """Notify the parent about the current range."""
        if self.on_range_changed is not None:
            self.on_range_changed(self._start_seconds, self._end_seconds)

"""Status bar widget for the Audio Clip Extractor."""

import tkinter as tk

# Color mapping for status types
_STATUS_COLORS = {
    "ready": "#888888",
    "info": "#2266cc",
    "success": "#228822",
    "error": "#cc2222",
    "processing": "#cc8800",
}


class StatusBar(tk.Frame):
    """A single-line status bar that displays messages with color-coded types."""

    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

        self._label = tk.Label(
            self,
            text="Ready",
            anchor=tk.W,
            fg=_STATUS_COLORS["ready"],
            padx=6,
            pady=2,
        )
        self._label.pack(fill=tk.X)

    def set_status(self, message: str, status_type: str = "info") -> None:
        """Update the status bar text and color.

        Args:
            message: The status message to display.
            status_type: One of "ready", "info", "success", "error",
                         "processing".  Determines the text color.
        """
        color = _STATUS_COLORS.get(status_type, _STATUS_COLORS["info"])
        self._label.config(text=message, fg=color)

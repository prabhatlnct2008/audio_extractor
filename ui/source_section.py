"""Source file selection section for the Audio Clip Extractor."""

import os
import tkinter as tk
from tkinter import filedialog
from typing import Callable, Optional

from utils.file_utils import SUPPORTED_VIDEO_FILETYPES, get_display_path


class SourceSection(tk.Frame):
    """A section that lets the user choose a video source file.

    Displays an "Open Video" button together with labels showing the
    selected filename and full path.
    """

    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

        self.on_file_selected: Optional[Callable[[str], None]] = None

        # --- top row: button -------------------------------------------------
        btn_frame = tk.Frame(self)
        btn_frame.pack(fill=tk.X, padx=6, pady=(4, 2))

        self._open_btn = tk.Button(
            btn_frame, text="Open Video", command=self._browse
        )
        self._open_btn.pack(side=tk.LEFT)

        # --- filename label (prominent) --------------------------------------
        self._name_label = tk.Label(
            self,
            text="No file selected",
            font=("TkDefaultFont", 11, "bold"),
            anchor=tk.W,
        )
        self._name_label.pack(fill=tk.X, padx=6)

        # --- full-path label (read-only, smaller) ----------------------------
        self._path_label = tk.Label(
            self,
            text="",
            anchor=tk.W,
            fg="#666666",
        )
        self._path_label.pack(fill=tk.X, padx=6, pady=(0, 4))

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _browse(self) -> None:
        """Open the native file dialog and handle selection."""
        file_path = filedialog.askopenfilename(
            title="Select a video file",
            filetypes=SUPPORTED_VIDEO_FILETYPES,
        )

        # User cancelled — do nothing
        if not file_path:
            return

        self._show_file(file_path)

        if self.on_file_selected is not None:
            self.on_file_selected(file_path)

    def _show_file(self, file_path: str) -> None:
        """Update the labels with the chosen file's information."""
        filename = os.path.basename(file_path)
        display_path = get_display_path(file_path)

        self._name_label.config(text=filename)
        self._path_label.config(text=display_path)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def reset(self) -> None:
        """Reset the section to its initial state."""
        self._name_label.config(text="No file selected")
        self._path_label.config(text="")

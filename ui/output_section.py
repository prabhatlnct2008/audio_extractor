"""Output path selection section for the Audio Clip Extractor."""

import tkinter as tk
from tkinter import filedialog
from typing import Callable, Optional

from utils.file_utils import ensure_wav_extension, get_display_path


class OutputSection(tk.Frame):
    """A section for choosing the output save location.

    The 'Choose Save Location' button opens a native save dialog defaulting
    to WAV files.  The selected path is guaranteed to carry a .wav extension.
    """

    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

        self._output_path: Optional[str] = None
        self.on_save_selected: Optional[Callable[[str], None]] = None

        # --- button row ------------------------------------------------------
        btn_frame = tk.Frame(self)
        btn_frame.pack(fill=tk.X, padx=6, pady=(4, 2))

        self._choose_btn = tk.Button(
            btn_frame,
            text="Choose Save Location",
            command=self._open_save_dialog,
        )
        self._choose_btn.pack(side=tk.LEFT)

        # --- path label (read-only) ------------------------------------------
        self._path_label = tk.Label(
            self,
            text="No save location selected",
            anchor=tk.W,
            fg="#666666",
        )
        self._path_label.pack(fill=tk.X, padx=6, pady=(0, 4))

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    def _open_save_dialog(self) -> None:
        """Open a native save-as dialog and store the chosen path."""
        path = filedialog.asksaveasfilename(
            title="Save Audio Clip As",
            defaultextension=".wav",
            filetypes=[("WAV files", "*.wav"), ("All files", "*.*")],
        )

        # User cancelled — do nothing.
        if not path:
            return

        path = ensure_wav_extension(path)
        self._output_path = path

        display = get_display_path(path)
        self._path_label.config(text=display, fg="#000000")

        if self.on_save_selected is not None:
            self.on_save_selected(path)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def get_output_path(self) -> Optional[str]:
        """Return the currently selected output path, or None."""
        return self._output_path

    def reset(self) -> None:
        """Clear the current selection and restore the default label."""
        self._output_path = None
        self._path_label.config(text="No save location selected", fg="#666666")

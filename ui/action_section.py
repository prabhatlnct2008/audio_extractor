"""Action buttons section for the Audio Clip Extractor."""

import tkinter as tk


class ActionSection(tk.Frame):
    """A section containing the Extract Audio and Reset buttons.

    Currently layout-only; buttons are not wired to any action yet.
    """

    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=6)

        self._extract_btn = tk.Button(
            btn_frame,
            text="Extract Audio",
            width=16,
            state=tk.DISABLED,
        )
        self._extract_btn.pack(side=tk.LEFT, padx=(0, 8))

        self._reset_btn = tk.Button(
            btn_frame,
            text="Reset",
            width=10,
        )
        self._reset_btn.pack(side=tk.LEFT)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def set_extracting(self, extracting: bool) -> None:
        """Enable or disable buttons based on extraction state.

        When *extracting* is True both buttons are disabled so the user
        cannot trigger another extraction or reset mid-process.  When
        False the buttons are re-enabled.
        """
        state = tk.DISABLED if extracting else tk.NORMAL
        self._extract_btn.config(state=state)
        self._reset_btn.config(state=state)

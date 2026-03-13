"""Audio Clip Extractor — Main entry point.

Launches the Tkinter-based desktop application for extracting
audio clips from video files and saving them as .wav files.
"""

import tkinter as tk
import sys
import os

# Ensure the project root is on the path when running from packaged app
if getattr(sys, "frozen", False):
    # Running as a packaged app (py2app / PyInstaller)
    os.chdir(os.path.dirname(sys.executable))

from ui.app_window import AppWindow


def main():
    root = tk.Tk()
    root.title("Audio Clip Extractor")
    root.minsize(700, 500)
    root.geometry("750x550")

    app = AppWindow(root)
    app.pack(fill=tk.BOTH, expand=True)

    root.mainloop()


if __name__ == "__main__":
    main()

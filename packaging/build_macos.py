"""PyInstaller build configuration for macOS .app bundle.

Run this script to build the Audio Clip Extractor as a standalone
macOS application:

    python packaging/build_macos.py

The resulting .app bundle will be placed in the dist/ directory.
"""

import os
import subprocess
import sys


def find_ffmpeg() -> str:
    """Locate the ffmpeg binary on the system."""
    for cmd in ["ffmpeg", "/usr/local/bin/ffmpeg", "/opt/homebrew/bin/ffmpeg"]:
        try:
            result = subprocess.run(
                ["which", cmd], capture_output=True, text=True
            )
            if result.returncode == 0:
                return result.stdout.strip()
        except FileNotFoundError:
            continue
    return ""


def find_ffprobe() -> str:
    """Locate the ffprobe binary on the system."""
    for cmd in ["ffprobe", "/usr/local/bin/ffprobe", "/opt/homebrew/bin/ffprobe"]:
        try:
            result = subprocess.run(
                ["which", cmd], capture_output=True, text=True
            )
            if result.returncode == 0:
                return result.stdout.strip()
        except FileNotFoundError:
            continue
    return ""


def build():
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    main_script = os.path.join(project_root, "main.py")

    if not os.path.isfile(main_script):
        print(f"Error: main.py not found at {main_script}")
        sys.exit(1)

    # Collect FFmpeg binaries to bundle
    add_binary_args = []
    ffmpeg_path = find_ffmpeg()
    ffprobe_path = find_ffprobe()

    if ffmpeg_path:
        add_binary_args.extend(["--add-binary", f"{ffmpeg_path}:."])
        print(f"Bundling ffmpeg from: {ffmpeg_path}")
    else:
        print("WARNING: ffmpeg not found. The app will require ffmpeg on PATH.")

    if ffprobe_path:
        add_binary_args.extend(["--add-binary", f"{ffprobe_path}:."])
        print(f"Bundling ffprobe from: {ffprobe_path}")
    else:
        print("WARNING: ffprobe not found. The app will require ffprobe on PATH.")

    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name", "AudioClipExtractor",
        "--windowed",
        "--onedir",
        "--noconfirm",
        "--clean",
        "--add-data", f"{os.path.join(project_root, 'ui')}:ui",
        "--add-data", f"{os.path.join(project_root, 'services')}:services",
        "--add-data", f"{os.path.join(project_root, 'utils')}:utils",
        *add_binary_args,
        main_script,
    ]

    print("Building macOS app bundle...")
    print(f"Command: {' '.join(cmd)}")

    result = subprocess.run(cmd, cwd=project_root)
    if result.returncode != 0:
        print("Build failed!")
        sys.exit(1)

    print("\nBuild complete!")
    print(f"App bundle: {os.path.join(project_root, 'dist', 'AudioClipExtractor.app')}")


if __name__ == "__main__":
    build()

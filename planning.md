# Audio Clip Extractor — Planning Document

## 1. Project Objective

Build a lightweight, single-purpose macOS desktop application using Python and Tkinter that allows non-technical users to extract a specific audio segment from a video file and save it as a `.wav` file. The application must be launchable with a single click (no terminal required) and provide a clear, minimal interface centered around: open video, define clip range via draggable timeline, choose save location, and extract.

---

## 2. Functional Requirements

Extracted from `application_flow.md` and `instructions.md`:

### 2.1 Application Launch
- Launch via click on macOS (no terminal)
- Main window opens at a usable size
- Entire workflow visible without scrolling

### 2.2 Video File Selection
- "Open Video" button triggers native file picker
- Supported video formats accepted (e.g., mp4, mov, avi, mkv)
- Selected file path and name displayed in UI
- Duration detected and displayed (if available)
- Unsupported or unreadable files produce clear error messages

### 2.3 Clip Range Selection (Draggable Timeline)
- Horizontal timeline represents full video duration
- Draggable start handle and end handle
- Highlighted region between handles shows selected segment
- Handles cannot cross each other
- Start always < end
- Range must stay within video duration
- Live-updating timestamp display during drag
- Minimum clip duration enforced to prevent accidental micro-selections

### 2.4 Fine Adjustment / Manual Time Entry (Optional)
- Start and end time fields displayed (editable or read-only)
- If editable, changes sync bidirectionally with timeline handles
- Accepted formats: SS, MM:SS, or HH:MM:SS

### 2.5 Save Location Selection
- "Choose Save Location" button triggers native save dialog
- Output path displayed in UI
- `.wav` extension enforced automatically
- Existing file replacement prompts user confirmation

### 2.6 Audio Extraction
- "Extract Audio" button validates all preconditions before proceeding
- Preconditions: video selected, valid range, save path chosen
- During extraction: button disabled, status shows "Extracting..."
- On success: success message with output path, optional "Open Folder" action
- On failure: clear, actionable error message
- User's previously entered values preserved after extraction

### 2.7 Error Handling
- Plain-language error messages
- Covers: no video, invalid time, start >= end, out-of-range, no save path, unwritable folder, unreadable source, unexpected failures

### 2.8 Status Feedback
- Status label reflecting current state: Ready, Video selected, Save location selected, Invalid input, Extracting, Success, Error

---

## 3. Assumptions

1. **FFmpeg dependency**: Audio extraction will use FFmpeg (via `pydub` or direct `subprocess` call). FFmpeg must be bundled or available on the user's system. For v1, we will bundle FFmpeg with the packaged app.
2. **Single video at a time**: Only one video can be loaded and processed at a time.
3. **Local files only**: No network/cloud file access.
4. **WAV-only output**: No other audio formats for v1.
5. **macOS primary target**: While Tkinter is cross-platform, packaging and UX testing targets macOS.
6. **Python 3.9+**: Target runtime.
7. **No video playback**: Timeline is duration-based, not media-playback-based.
8. **Reasonable file sizes**: The app handles normal local video files; extremely large files (>10GB) may have slower duration detection but should still work.
9. **Single-threaded extraction with UI responsiveness**: Extraction runs in a background thread to keep UI responsive.

---

## 4. Risks and Implementation Challenges

| Risk | Impact | Mitigation |
|------|--------|------------|
| FFmpeg bundling complexity on macOS | High — app won't work without it | Use py2app/PyInstaller with FFmpeg binary included; test packaged app early |
| Tkinter Canvas drag precision | Medium — poor UX if drag is jittery | Implement smooth mouse tracking with proper coordinate math; test at multiple window sizes |
| Duration detection for unusual formats | Medium — some containers may not report duration easily | Use `ffprobe` as primary, fall back to `pydub`; handle missing duration gracefully |
| macOS file dialog behavior in packaged apps | Medium — dialogs may not appear foreground | Test with py2app early; apply known Tkinter macOS workarounds |
| Thread safety with Tkinter | High — Tkinter is not thread-safe | Use `after()` polling or queue-based communication for background thread results |
| Large file extraction time | Low-Medium — user may think app froze | Show extraction progress or at minimum a clear "Extracting..." state |
| Handle synchronization with manual entry | Medium — bidirectional sync can create feedback loops | Use flag-based guard to prevent recursive updates |

---

## 5. UI Behavior Expectations

### Layout (top to bottom)
1. **Source File Section** — "Open Video" button + file path display
2. **Timeline Section** — Draggable horizontal timeline with start/end handles and highlighted region
3. **Time Display / Fine Adjustment Section** — Start time, end time, clip duration labels/fields
4. **Output Section** — "Choose Save Location" button + output path display
5. **Action Section** — "Extract Audio" button (+ optional "Reset" button)
6. **Status Section** — Status message label

### Interaction Flow
- Timeline is disabled until a video is loaded
- Extract button validates all fields before proceeding
- Double-click prevention during extraction
- Status updates at every significant state change

### Window Behavior
- Fixed or resizable with minimum size constraint
- Timeline redraws correctly on resize if resizable

---

## 6. Major Modules / Components

| Module | Responsibility |
|--------|---------------|
| `main.py` | Application entry point, window setup |
| `ui/app_window.py` | Main window layout, section composition |
| `ui/source_section.py` | Video file selection UI |
| `ui/timeline.py` | Custom Canvas-based draggable timeline widget |
| `ui/time_display.py` | Start/end time display and optional manual entry |
| `ui/output_section.py` | Save location selection UI |
| `ui/action_section.py` | Extract button and reset controls |
| `ui/status_bar.py` | Status message display |
| `services/media_info.py` | Video duration detection (ffprobe/pydub) |
| `services/audio_extractor.py` | Audio extraction logic (FFmpeg-based) |
| `services/validation.py` | All validation rules centralized |
| `utils/time_utils.py` | Time parsing, formatting, conversion utilities |
| `utils/file_utils.py` | File path handling, extension enforcement |
| `packaging/` | py2app/PyInstaller config, build scripts |

---

## 7. Validation Rules

| Rule | When Enforced |
|------|--------------|
| Video file must be selected | Before extraction |
| File must be readable and supported | On file selection |
| Duration must be detected | On file selection |
| Start < End | On handle drag, manual entry, and extraction |
| Handles cannot cross | During drag interaction |
| Range within video duration | On handle drag, manual entry, and extraction |
| Minimum clip duration (e.g., 0.5s) | On handle drag and extraction |
| Save path must be selected | Before extraction |
| Output extension must be `.wav` | On save path selection |
| Save directory must be writable | Before extraction |
| No duplicate extraction while processing | On extract button click |

---

## 8. Packaging Expectations (macOS)

- Package as a `.app` bundle using **py2app** or **PyInstaller**
- Bundle FFmpeg binary inside the app
- Include all Python dependencies
- App icon (default or custom)
- Launchable by double-clicking — no terminal required
- Native file dialogs work correctly from packaged app
- Test on macOS to verify file picker, save dialog, and extraction all work in packaged form
- Provide a build script (`build.sh` or `Makefile`) for reproducible builds

---

## 9. Testing Strategy

### 9.1 Unit Tests
- Time parsing and formatting (`time_utils.py`)
- Validation logic (`validation.py`)
- File extension enforcement (`file_utils.py`)

### 9.2 Integration Tests
- Duration detection from sample video files
- Audio extraction produces valid `.wav` output
- Extraction with various start/end combinations

### 9.3 UI / Manual Tests
- Open video → path displayed correctly
- Timeline activates after video load
- Drag start handle → timestamp updates live
- Drag end handle → timestamp updates live
- Handles cannot cross
- Manual time entry syncs with timeline (if implemented)
- Choose save location → path displayed
- Extract with valid inputs → success message
- Extract with missing fields → validation error shown
- Extract with invalid range → error shown
- Re-extraction after error works
- Very short clips (0.5s–1s)
- Large video files
- Cancel file/save dialogs → no crash, no state corruption
- Window resize → timeline redraws correctly

### 9.4 Packaging Tests
- Built `.app` launches on macOS by double-click
- File picker works from packaged app
- Extraction works from packaged app
- FFmpeg is accessible inside bundle

---

## 10. Open Questions and Resolutions

| Question | Resolution |
|----------|-----------|
| Which library for audio extraction? | Use FFmpeg via subprocess (most reliable). Optionally wrap with pydub for convenience. |
| Manual time entry: editable or read-only? | Start with editable fields that sync bidirectionally with the timeline for maximum usability. |
| Minimum clip duration? | Enforce 0.5 seconds minimum to prevent accidental micro-selections. |
| Resize support? | Support window resizing with timeline redraw. Set a minimum window size. |
| What video formats to accept in file picker? | Accept common formats: `.mp4`, `.mov`, `.avi`, `.mkv`, `.webm`, `.flv`, `.wmv`. Let FFmpeg handle actual codec support. |
| Replace existing output file? | Prompt user via system dialog (handled by native save dialog on macOS). |
| Progress indicator during extraction? | v1: show "Extracting..." status text. Future: add progress bar if feasible. |

---

## 11. Definition of Done — Version One

Version one is complete when:

- [ ] User can launch the app on macOS by clicking it (packaged `.app`)
- [ ] User can select a video file via native file picker
- [ ] Selected file path and duration are displayed
- [ ] Draggable timeline with start/end handles works correctly
- [ ] Handles cannot cross; range stays within video duration
- [ ] Timestamps update live during drag
- [ ] Manual time entry fields sync with timeline
- [ ] User can choose a save location via native save dialog
- [ ] `.wav` extension is enforced automatically
- [ ] "Extract Audio" validates all preconditions before proceeding
- [ ] Extraction runs without freezing the UI
- [ ] Success message shows output path
- [ ] Error messages are clear and actionable
- [ ] Common edge cases handled (no video, invalid range, no save path, unwritable location)
- [ ] Code is modular and organized by responsibility
- [ ] `planning.md` and `phases.md` are complete and up to date
- [ ] Basic unit tests pass for core logic (validation, time utils)

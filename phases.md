# Audio Clip Extractor — Implementation Phases

## Phase Overview

The implementation is organized into 7 phases. Phases 1–3 establish the foundation. Phases 4A, 4B, and 4C are independent parallel tracks that can be implemented simultaneously. Phases 5–7 are sequential integration, packaging, and finalization steps.

```
Phase 1: Project Setup & Core Utilities
    │
Phase 2: Core Services (media info + extraction)
    │
Phase 3: Main Window Shell & Layout
    │
    ├──────────────────┼──────────────────┐
Phase 4A:          Phase 4B:          Phase 4C:
Timeline Widget    Validation &       Output Section &
& Drag Logic       Error Display      Save Location
    │                  │                  │
    └──────────────────┼──────────────────┘
                       │
Phase 5: Integration & Extraction Workflow
    │
Phase 6: macOS Packaging
    │
Phase 7: Testing, Polish & Completion Checklist
```

---

## Phase 1: Project Setup & Core Utilities

**Goal**: Establish the project structure, dependencies, and foundational utility modules.

**Scope**:
- Create directory structure (`ui/`, `services/`, `utils/`, `packaging/`, `tests/`)
- Set up `requirements.txt` with dependencies (pydub, etc.)
- Implement `utils/time_utils.py` — time parsing (SS, MM:SS, HH:MM:SS), formatting, seconds-to-display conversion
- Implement `utils/file_utils.py` — `.wav` extension enforcement, path validation helpers
- Create `main.py` entry point skeleton

**Deliverables**:
- Project directory structure
- `requirements.txt`
- `utils/time_utils.py` with unit tests
- `utils/file_utils.py` with unit tests
- `main.py` skeleton

**Dependencies**: None

**Validation Checkpoints**:
- [ ] All utility functions have passing unit tests
- [ ] Time parsing handles SS, MM:SS, HH:MM:SS formats correctly
- [ ] Time parsing rejects invalid inputs gracefully
- [ ] File extension enforcement works for edge cases (no extension, wrong extension, correct extension)

**Parallel**: This phase must complete before Phase 2 and Phase 3. It is the foundation.

---

## Phase 2: Core Services (Media Info & Audio Extraction)

**Goal**: Build the backend services that detect video duration and extract audio segments.

**Scope**:
- Implement `services/media_info.py` — detect video duration using `ffprobe` (subprocess), fallback to `pydub`
- Implement `services/audio_extractor.py` — extract audio segment using FFmpeg subprocess, output as `.wav`
- Handle errors: unreadable file, missing audio stream, extraction failure
- Background thread execution support (extraction runs off the main thread)

**Deliverables**:
- `services/media_info.py` with duration detection
- `services/audio_extractor.py` with segment extraction
- Integration tests with a sample video file
- Error handling for common failure modes

**Dependencies**: Phase 1 (utilities)

**Validation Checkpoints**:
- [ ] Duration detection works for `.mp4`, `.mov`, `.avi` test files
- [ ] Duration detection returns clear error for non-video files
- [ ] Audio extraction produces a valid `.wav` file for a given time range
- [ ] Extraction with start=0, end=full_duration works
- [ ] Extraction with a mid-range segment works
- [ ] Extraction handles missing FFmpeg gracefully (clear error)

**Parallel**: Can run in parallel with Phase 3 once Phase 1 is complete.

---

## Phase 3: Main Window Shell & Layout

**Goal**: Build the main application window with all UI sections laid out (non-functional placeholders where needed).

**Scope**:
- Implement `ui/app_window.py` — main Tkinter window with section frames
- Implement `ui/source_section.py` — "Open Video" button + file path label (functional file picker)
- Implement `ui/output_section.py` — "Choose Save Location" button + output path label (placeholder)
- Implement `ui/action_section.py` — "Extract Audio" button + optional "Reset" button (placeholder)
- Implement `ui/status_bar.py` — status message label
- Set minimum window size
- Wire up the "Open Video" button to a native file dialog

**Deliverables**:
- `ui/app_window.py` composing all sections
- `ui/source_section.py` with working file picker
- `ui/output_section.py` (layout only)
- `ui/action_section.py` (layout only)
- `ui/status_bar.py`
- Launchable app shell via `main.py`

**Dependencies**: Phase 1 (project structure)

**Validation Checkpoints**:
- [ ] App launches and shows the main window
- [ ] All six sections are visible without scrolling
- [ ] "Open Video" opens native file dialog
- [ ] Selected file path displays correctly
- [ ] Window has a sensible minimum size
- [ ] Status bar shows "Ready" on launch

**Parallel**: Can run in parallel with Phase 2 once Phase 1 is complete.

---

## Phase 4A: Timeline Widget & Drag Logic

**Goal**: Build the custom draggable timeline Canvas widget with start/end handles and highlighted selection region.

**Scope**:
- Implement `ui/timeline.py` — custom Tkinter Canvas widget
- Draw timeline track representing full video duration
- Draw start handle (draggable) and end handle (draggable)
- Highlight selected region between handles
- Mouse event handling: press, drag, release on handles
- Handle crossing prevention
- Live timestamp update during drag (callback-based)
- Implement `ui/time_display.py` — start/end time labels and editable fields
- Bidirectional sync: drag updates fields, field edits update handle positions
- Guard against recursive update loops
- Timeline disabled state when no video is loaded
- Redraw on window resize

**Deliverables**:
- `ui/timeline.py` — fully interactive timeline widget
- `ui/time_display.py` — synchronized time display/entry
- Callback interface for parent to receive range changes

**Dependencies**: Phase 3 (window shell to host the widget)

**Validation Checkpoints**:
- [ ] Timeline renders correctly for various durations (10s, 60s, 3600s)
- [ ] Start handle drags smoothly and updates start time display live
- [ ] End handle drags smoothly and updates end time display live
- [ ] Handles cannot cross each other
- [ ] Selected region highlight updates correctly
- [ ] Manual time entry updates handle positions
- [ ] Timeline is disabled/grayed when no video is loaded
- [ ] Timeline redraws properly on window resize
- [ ] Minimum selection duration (0.5s) is enforced

**Parallel**: Can run in parallel with Phase 4B and Phase 4C.

---

## Phase 4B: Validation Engine & Error Display

**Goal**: Centralize all validation rules and wire error/status messages into the UI.

**Scope**:
- Implement `services/validation.py` — all validation rules as pure functions
  - `validate_source_file(path)` — file exists, readable, supported format
  - `validate_time_range(start, end, duration)` — start < end, within bounds, minimum duration
  - `validate_output_path(path)` — path set, `.wav` extension, directory writable
  - `validate_extraction_ready(source, start, end, output)` — all preconditions met
- Wire status bar to show validation errors clearly
- Define error message constants (plain language, actionable)

**Deliverables**:
- `services/validation.py` with all validation functions
- Unit tests for every validation rule
- Error message constants

**Dependencies**: Phase 1 (utilities for time/file logic)

**Validation Checkpoints**:
- [ ] Each validation function returns clear pass/fail with message
- [ ] All validation rules from the functional spec are covered
- [ ] Unit tests pass for valid and invalid inputs
- [ ] Error messages are plain language and actionable

**Parallel**: Can run in parallel with Phase 4A and Phase 4C.

---

## Phase 4C: Output Section & Save Location

**Goal**: Make the save location section fully functional with native save dialog and path display.

**Scope**:
- Wire `ui/output_section.py` "Choose Save Location" button to native save dialog
- Enforce `.wav` extension on selected path
- Display chosen output path in UI
- Handle user cancellation of save dialog (no state change)
- Existing file replacement handled by native dialog

**Deliverables**:
- Fully functional `ui/output_section.py`
- `.wav` extension auto-enforcement
- Cancellation handling

**Dependencies**: Phase 3 (window shell)

**Validation Checkpoints**:
- [ ] Save dialog opens and allows folder/file selection
- [ ] Chosen path displays correctly in UI
- [ ] `.wav` extension is appended if missing
- [ ] Cancelling the dialog leaves state unchanged
- [ ] Path with spaces and special characters handled correctly

**Parallel**: Can run in parallel with Phase 4A and Phase 4B.

---

## Phase 5: Integration & Extraction Workflow

**Goal**: Wire all components together into the complete extraction workflow.

**Scope**:
- Connect "Open Video" → media info service → timeline activation
- Connect timeline range → time display → validation
- Connect "Choose Save Location" → output path → validation
- Connect "Extract Audio" button to full workflow:
  1. Validate all preconditions (via `validation.py`)
  2. Disable UI controls during extraction
  3. Run extraction in background thread
  4. Poll for completion via Tkinter `after()`
  5. Show success or error in status bar
  6. Re-enable UI controls
- Implement optional "Open Folder" action on success
- Implement optional "Reset" button
- Prevent duplicate extraction clicks

**Deliverables**:
- Fully wired application with end-to-end extraction workflow
- Background thread extraction with UI responsiveness
- Complete status flow: Ready → Video selected → Range set → Save location chosen → Extracting → Success/Error

**Dependencies**: Phase 4A, Phase 4B, Phase 4C (all parallel tracks complete)

**Validation Checkpoints**:
- [ ] Happy path works end to end: open video → set range → choose save → extract → success
- [ ] Invalid inputs blocked at extraction time with clear messages
- [ ] UI remains responsive during extraction
- [ ] Extract button disabled during processing
- [ ] Error during extraction shows clear message and allows retry
- [ ] Reset clears all fields and returns to "Ready" state
- [ ] Re-extraction after success works
- [ ] Re-extraction after error works

**Parallel**: This phase is sequential — requires all Phase 4 tracks to complete.

---

## Phase 6: macOS Packaging

**Goal**: Package the application as a clickable `.app` for macOS.

**Scope**:
- Choose packaging tool (py2app or PyInstaller)
- Create packaging configuration (`setup.py` for py2app or `.spec` for PyInstaller)
- Bundle FFmpeg binary inside the app
- Create build script (`build.sh`)
- Test packaged app on macOS:
  - Launches by double-click
  - File picker works
  - Save dialog works
  - Extraction works
  - FFmpeg accessible inside bundle
- Handle macOS-specific Tkinter quirks (e.g., window focus, dialog z-order)

**Deliverables**:
- `packaging/setup.py` or `packaging/app.spec`
- `packaging/build.sh` build script
- Documentation for building the app
- Verified `.app` bundle

**Dependencies**: Phase 5 (working integrated application)

**Validation Checkpoints**:
- [ ] Build script produces a `.app` bundle without errors
- [ ] App launches by double-click on macOS
- [ ] All file dialogs work correctly from packaged app
- [ ] Extraction produces valid `.wav` from packaged app
- [ ] FFmpeg is found and executes within the bundle
- [ ] App works for a non-technical user (no terminal needed)

**Parallel**: This phase is sequential — requires Phase 5 to complete.

---

## Phase 7: Testing, Polish & Completion Checklist

**Goal**: Final round of testing, edge case handling, code cleanup, and completion verification.

**Scope**:
- Run all unit tests and fix failures
- Perform full manual test pass (see testing strategy in `planning.md`)
- Test edge cases:
  - Very short clips (0.5s–1s)
  - Large video files
  - Invalid/corrupt video files
  - User cancels dialogs mid-flow
  - Rapid repeated clicks
  - Window resize during drag
- Code review and refactor:
  - Remove dead code
  - Ensure consistent naming
  - Verify module boundaries are clean
- Update `planning.md` and `phases.md` with final status
- Complete the Definition of Done checklist

**Deliverables**:
- All unit tests passing
- Manual test results documented
- Clean, refactored codebase
- Updated planning documents
- Completed Definition of Done checklist

**Dependencies**: Phase 6 (packaged app for macOS testing)

**Validation Checkpoints**:
- [ ] All unit tests pass
- [ ] Happy path manual test passes
- [ ] Edge case tests pass or are documented as known limitations
- [ ] Code is modular, readable, and well-organized
- [ ] No obvious security issues (path traversal, command injection in FFmpeg calls)
- [ ] Definition of Done checklist in `planning.md` is fully satisfied
- [ ] `planning.md` and `phases.md` reflect final state

**Parallel**: This phase is sequential — final step.

---

## Parallel Execution Summary

| Phase | Can Parallel With | Must Wait For |
|-------|-------------------|---------------|
| Phase 1 | — | — |
| Phase 2 | Phase 3 | Phase 1 |
| Phase 3 | Phase 2 | Phase 1 |
| Phase 4A | Phase 4B, 4C | Phase 3 |
| Phase 4B | Phase 4A, 4C | Phase 1 |
| Phase 4C | Phase 4A, 4B | Phase 3 |
| Phase 5 | — | Phase 4A, 4B, 4C |
| Phase 6 | — | Phase 5 |
| Phase 7 | — | Phase 6 |

**Maximum parallelism**: Phases 4A, 4B, and 4C can all be implemented simultaneously, which is the widest parallel section. Phases 2 and 3 can also run in parallel after Phase 1.

# Audio Clip Extractor — Functional Documentation

## 1. Purpose

The Audio Clip Extractor is a simple desktop utility built with Tkinter for macOS users who want to extract a specific portion of audio from a video file and save it as a `.wav` file.

The tool is designed for single-click usability on Mac. The user should be able to launch the app like a normal desktop application, open a video, define the audio segment they want by setting a start time and end time, choose where the extracted file will be saved, and then perform the extraction.

The application is intended to stay minimal, focused, and easy to use for non-technical users.

---

## 2. Primary Goal

Allow a user to:

* Open a video file from their Mac
* Specify a start point for extraction
* Specify an end point for extraction
* Choose the destination where the output file will be saved
* Extract only the audio from that selected section
* Save the extracted audio as a `.wav` file

---

## 3. User Type

This application is meant for a basic desktop user who:

* Works on macOS
* Wants a very small utility for audio extraction
* Does not want to use complex editing software
* Prefers a direct graphical interface instead of command-line tools

---

## 4. Scope

### Included in Scope

The first version of the application should include:

* Opening a local video file
* Showing the selected file path or file name
* Accepting start time and end time input
* Validating the time range
* Allowing the user to choose an output save location
* Saving the result as a `.wav` file
* Showing success and error messages
* Running as a simple clickable app on macOS

### Out of Scope for Initial Version

The first version does not need:

* A video preview player
* Waveform visualization
* Drag-based timeline editing
* Multi-clip extraction
* Batch processing
* Audio enhancement or normalization
* Support for multiple export audio formats
* Cloud upload or online storage
* User accounts or settings sync

---

## 5. Product Overview

The application has one simple workflow:

1. The user opens the app on Mac by clicking the application icon.
2. The user selects a video file from their computer.
3. The user enters the start and end time of the portion they want.
4. The user selects the location and file name for the extracted audio.
5. The user clicks the extract button.
6. The application processes the request and saves the selected audio portion as a `.wav` file.
7. The user receives a success message with the saved file location.

---

## 6. Functional Requirements

## 6.1 Application Launch

When the user opens the app on macOS:

* The application should launch through a normal click, without requiring terminal usage.
* The main window should open in a usable size.
* The interface should be simple enough that the main action flow is visible without scrolling.

Expected user experience:

* User clicks the app icon
* App opens to the main extraction screen

---

## 6.2 Open Video File

The application should provide a clearly visible control to open a video file.

### User Action

The user clicks a button such as `Open Video`.

### System Behavior

* The system opens a native file picker dialog.
* The user can browse local folders and choose a video file.
* After selection, the application stores the selected source file path for processing.
* The selected file name or full path should be displayed on the screen.

### Validation

* If no file is selected, extraction must not proceed.
* If the file type is unsupported or unreadable, the application should show a clear error.

### Display Requirement

After file selection, the UI should show:

* File name
* Full path or shortened path
* Optional duration if available

---

## 6.3 Clip Range Selection

The application should allow the user to define the start and end of the extraction range using a visual draggable timeline instead of relying only on manual time entry.

### Core Interaction

The user should be able to:

* View a horizontal timeline representing the loaded video duration
* Drag a start handle to set the clip start point
* Drag an end handle to set the clip end point
* Visually see the selected range between the two handles
* Optionally fine-tune the values through time input fields if those are kept in the interface

### Functional Behavior

Once a video is selected:

* The application should load the total duration of the video
* The timeline should become active
* The left handle should represent the clip start point
* The right handle should represent the clip end point
* The highlighted region between the handles should represent the portion to be extracted

### Handle Movement Rules

* The start handle can move only from the beginning of the video up to just before the end handle
* The end handle can move only from just after the start handle up to the end of the video
* The handles must never cross each other
* The system should always maintain a valid range

### Visual Feedback

The timeline should clearly show:

* Full media duration
* Current start point
* Current end point
* Highlighted selected segment
* Current time values corresponding to both handles

Recommended display:

* Start time shown near or below the start handle
* End time shown near or below the end handle
* Selected clip duration shown nearby

### Precision Behavior

Dragging should feel controlled and usable for normal clip selection.

Recommended support:

* Smooth dragging with live updating time values
* Ability to make small adjustments with reasonable precision
* Optional arrow-key or fine-adjust controls in later versions

### Optional Manual Inputs

If manual time fields remain in the interface:

* Changes in the timeline should update the time fields
* Changes in the time fields should update handle positions
* Both input methods should remain synchronized

### Validation Rules

* A clip range cannot exist without a selected video
* Start must always be less than end
* Selected range must remain within the video duration
* Extremely tiny accidental selections should either be blocked or clearly shown

---

## 6.4 Start and End Time Display

Even when drag-based selection is the main interaction, the interface should still display the exact start and end times currently selected.

### Display Requirement

The app should show:

* Current clip start time
* Current clip end time
* Optional total selected clip length

### Behavior

* These displayed values should update live while the user drags either handle
* If manual editing is allowed, entered values should be validated and reflected back on the timeline

---

## 6.5 Save Location Selection

The application should allow the user to choose where the output `.wav` file will be saved.

### User Action

The user clicks a button such as `Choose Save Location` or `Browse`.

### System Behavior

* A native save dialog opens.
* The user can select a folder and file name.
* The output should be saved in `.wav` format.
* If the user does not type `.wav`, the application should automatically ensure the output file uses the `.wav` extension.

### Display Requirement

The chosen output path should be displayed in the interface so the user can confirm where the file will be saved.

### Validation Rules

* Extraction must not begin unless a valid output path is selected.
* If the file already exists, the system should ask whether the user wants to replace it.

---

## 6.6 Extract Audio

The application should provide a primary action button such as `Extract Audio`.

### Preconditions

Extraction can begin only when:

* A video file has been selected
* A valid start time is entered
* A valid end time is entered
* A valid save location is selected

### System Behavior

When the user clicks the extract button:

* The system validates all required fields
* The system reads the selected video file
* The system extracts only the audio between the start and end points
* The system converts or saves the audio as `.wav`
* The system writes the output to the chosen save location

### During Processing

The interface should:

* Prevent duplicate clicks while extraction is in progress
* Show a visible processing state such as `Extracting...`
* Optionally show a progress indicator if feasible

### On Success

The interface should show:

* A success message
* The output file path
* An optional button to open the containing folder

### On Failure

The interface should show a clear error message describing the likely problem.

---

## 6.7 Error Handling

The tool should handle common user and system errors gracefully.

### Example Error Cases

* No video selected
* Invalid time format
* Start time is after end time
* End time is outside video duration
* Save path not selected
* Output folder is not writable
* Source video cannot be read
* Extraction process fails unexpectedly

### Error Message Principles

Messages should:

* Be plain language
* Tell the user what went wrong
* Suggest what to fix when possible

Examples:

* `Please select a video file before extracting.`
* `Enter a valid start time in SS, MM:SS, or HH:MM:SS format.`
* `End time must be greater than start time.`
* `The selected save location cannot be written to.`

---

## 6.8 Success Handling

After a successful extraction:

* The app should confirm that the audio file was created
* The saved file path should remain visible
* The user should not lose their previously entered values unless they reset them manually

Recommended success message:

`Audio extracted successfully and saved as WAV.`

Recommended additional action:

* `Open Folder`
* `Extract Another Clip`

---

## 7. Screen-Level Functional Description

## 7.1 Main Window

The application should have a single main screen.

### Main Window Sections

#### A. Source File Section

Purpose: choose the video file.

Content:

* Label for source video
* `Open Video` button
* Read-only display area showing selected file path

#### B. Timeline Selection Section

Purpose: visually define the extraction range.

Content:

* Horizontal draggable timeline
* Start handle
* End handle
* Highlighted selected region
* Visible current start and end timestamps
* Optional selected clip duration display

#### C. Fine Adjustment Section

Purpose: allow precise review or manual correction of selected values.

Content:

* Start time display or input field
* End time display or input field
* Optional clip duration display
* Helper text if manual entry is supported

#### D. Output Section

Purpose: choose where the `.wav` file will be saved.

Content:

* `Choose Save Location` button
* Read-only display area for output path

#### E. Action Section

Purpose: start extraction.

Content:

* `Extract Audio` primary button
* Optional `Reset` button

#### F. Status Section

Purpose: show messages.

Content:

* Status label for ready, processing, success, or error states

---

## 8.1 Standard Happy Path

1. User launches the app.
2. User clicks `Open Video`.
3. User selects a local video file.
4. App shows the selected file path.
5. App activates the draggable timeline.
6. User drags the start handle to the desired clip beginning.
7. User drags the end handle to the desired clip ending.
8. App updates the displayed timestamps live.
9. User clicks `Choose Save Location`.
10. User selects a destination and file name.
11. App shows the save path.
12. User clicks `Extract Audio`.
13. App validates inputs.
14. App extracts the selected audio portion.
15. App saves the result as `.wav`.
16. App shows success message and saved location.

---

## 8.2 Invalid Input Flow

1. User opens a video.
2. User enters an invalid time format.
3. User clicks `Extract Audio`.
4. App blocks extraction.
5. App shows a clear validation message.
6. User corrects the input.
7. User retries extraction.

---

## 8.3 Missing Save Location Flow

1. User opens a video.
2. User enters valid start and end times.
3. User does not choose save location.
4. User clicks `Extract Audio`.
5. App blocks extraction.
6. App requests that the user choose an output location.

---

## 9. Data and Field Logic

## 9.1 Source Video Path

Purpose:

* Holds the selected input file location

Behavior:

* Populated only through file picker
* Read-only in UI
* Cleared on reset

## 9.2 Start Time

Purpose:

* Defines beginning of audio segment

Behavior:

* Entered manually by user
* Validated before extraction

## 9.3 End Time

Purpose:

* Defines end of audio segment

Behavior:

* Entered manually by user
* Must be greater than start time

## 9.4 Output File Path

Purpose:

* Defines where extracted `.wav` will be stored

Behavior:

* Populated via save dialog
* Must end with `.wav`

## 9.5 Status Message

Purpose:

* Gives user feedback on system state

Possible states:

* Ready
* Video selected
* Save location selected
* Invalid input
* Extracting
* Success
* Error

---

## 10. Validation Rules Summary

The application should enforce the following:

* Video file must be selected before extraction
* Start handle and end handle must define a valid range
* Start must be less than end
* Selected range must stay within the video duration
* Save path is required
* Output file must be `.wav`
* If manual time entry is enabled, entered values must stay synchronized with the timeline and pass validation

---

## 11. macOS Functional Expectations

Because the tool is intended for Mac and must work through a simple click, the product should behave like a normal lightweight Mac app.

### Required User Experience

* The user should not need to run Python manually
* The user should not need to open Terminal
* The user should launch the tool by clicking an app icon or packaged application file

### Functional Expectation for Delivery

The final delivered application should behave as:

* A self-contained clickable desktop utility for macOS
* Easy to open and use by a non-technical user

---

## 12. Non-Functional Expectations

Even though this document is focused on functionality, the following are important for the product experience:

### Simplicity

The UI should be very minimal and understandable in under a minute.

### Reliability

The extraction should consistently produce the expected `.wav` output when valid inputs are supplied.

### Responsiveness

The app should respond quickly for normal local files and should indicate when processing is underway.

### Clarity

The app should always make it obvious:

* Which file is selected
* What clip range is being extracted
* Where the output will be saved
* Whether extraction succeeded or failed

---

## 13. Suggested Functional Enhancements for Later Versions

These are future enhancements and should not block version one:

* Embedded video preview player
* Play/pause and scrubbing controls
* Automatic duration detection display
* Preset buttons to mark current playback time as start or end
* Waveform-based selection
* Recently used save folder memory
* Drag-and-drop video import
* Batch extraction from one or many videos
* Export to MP3 or AAC in addition to WAV
* Keyboard shortcuts
* Folder auto-open after success

---

## 14. Acceptance Criteria

The application should be considered functionally complete for version one when all of the following are true:

* User can launch the app on a Mac by clicking it
* User can select a video file from local storage
* User can select a valid clip range using draggable timeline handles
* User can select an output save path
* User can extract audio from the chosen range
* Output is saved in `.wav` format
* User sees a success message after completion
* Invalid inputs are blocked with clear errors
* The app does not require terminal interaction for normal use

---

## 15. Example Use Case

A user has a lecture video and wants only the audio from minute 2:15 to minute 4:40.

The user opens the app, selects the lecture video, drags the start handle on the timeline to `2:15`, drags the end handle to `4:40`, chooses the Desktop as the save location, names the file `lecture_clip.wav`, and clicks `Extract Audio`.

The application processes the request and saves the selected audio portion as a `.wav` file on the Desktop.

---

## 16. Final Functional Summary

This product is a single-purpose Mac desktop utility that lets a user extract a chosen audio segment from a video and save it as a `.wav` file. The entire product should revolve around a straightforward flow: open video, define range, choose save location, and extract. The interface should remain lightweight, understandable, and usable with a normal click on macOS.

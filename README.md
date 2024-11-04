# GhostInk

**GhostInk** is a Python utility to streamline debugging and etch(task) tracking by printing detailed file information for each call. This tool eliminates the need to manually add `print` statements and hunt for line numbers or file names, providing an organized, colorful output to track etchings, debug info, and errors across your project.

---

## Installation

To install `GhostInk`, add it to your project with pip(soon will be available, but for the moment just clone the repo):

```bash
pip install ghosink
```

Then, import `GhostInk` into your Python files:

```python
from ghosink import GhostInk
```

---

## Usage

### Initialize GhostInk

To start, create a `GhostInk` instance with optional parameters:

```python
ink = GhostInk(
    title="My Project Debugger",
    project_root=".",         # Set the project root for relative path display
    log_to_file=True,         # Enable/disable logging to a file
    log_file="debug.log"      # Specify log file name if logging is enabled
)
```

### Adding etchings (tasks) with Modes

Add etchings with `inkdrop`, assigning modes such as `TODO`, `INFO`, `DEBUG`, `WARN`, or `ERROR`. Modes allow you to manage and filter etchings effectively.

```python
ink.inkdrop("Refactor this method", mode=GhostInk.mode.TODO)
ink.inkdrop("This is debug info", mode=GhostInk.mode.DEBUG)
```

### Printing Location Information with `haunt`

If you simply want to print the current file location (file, line, function, and timestamp) without adding a etch, use `haunt`:

```python
ink.haunt("Executing important operation")
```

### Viewing and Filtering etchings with `whisper`

View all tracked etchings using `whisper`, with optional filters by mode or file name:

```python
ink.whisper(mode_mask=GhostInk.mode.TODO)
ink.whisper(file_mask="main.py")
```

---

## Key Methods

1. **`haunt(msg: str = None)`**  
   - Prints file, line, function, and timestamp for tracking execution points.
   - **Parameters**:
     - `msg`: Optional message displayed before the file information.

2. **`inkdrop(etch_input: any, mode: mode = mode.TODO)`**  
   - Adds a etch with text and a specific mode to the etch list.
   - **Parameters**:
     - `etch_input`: Text, dictionary, or object to record as a etch.
     - `mode`: etch mode (TODO, INFO, DEBUG, WARN, ERROR).

3. **`whisper(filter_mode: str = None, filter_filename: str = None)`**  
   - Prints filtered etchings based on mode and filename.
   - **Parameters**:
     - `filter_mode`: Filter etchings by mode.
     - `filter_filename`: Filter etchings by specific file name.

4. **`_color_text(mode: mode, text: str = "")`**  
   - Colors output based on etch mode (internal use).

5. **`_get_relative_path()`**  
   - Retrieves relative path, line number, and function name for etchings.

---

## Example

```python
from ghosink import GhostInk

# Initialize with logging enabled
ink = GhostInk(title="Project Debugger", log_to_file=True)

# Add etchings
ink.inkdrop("Fix memory leak", mode=GhostInk.mode.TODO)
ink.inkdrop("Checkpoint reached", mode=GhostInk.mode.INFO)
ink.inkdrop("Debug, Error, Warn itchs", mode=GhostInk.mode.DEBUG)

# Print a debug statement with file details
ink.haunt("Debugging current function")

# View all etchings
ink.whisper()
```

### Example Output

![example output](assets/main_out.png)

---

## Benefits

- No more manually adding and searching for `print` statements!
- Clearly organized, color-coded outputs make etchings easy to spot and review.
- Optional file logging to retain records and analyze later.
- Filters for viewing etchings by file and mode allow better focus and etch management.

---

**Start using GhostInk** and turn your debug prints into an organized, colorful log. Perfect for developers who want a better way to keep track of etchings and debug information without losing context!

---

## Inspired By

This project is inspired by the [icecream](https://github.com/gruns/icecream) library.

---

## Contributing

Contributions are welcome! If you have suggestions or improvements, please create a pull request.

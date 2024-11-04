# GhostInk

**GhostInk** is a Python utility to streamline debugging and etch(task) tracking by printing detailed file information for each call. This tool eliminates the need to manually add `print` statements and hunt for line numbers or file names, providing an organized, colorful output to track etchings, debug info, and errors across your project.

---

## Installation

To install `GhostInk`, add it to your project with pip:

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

### Adding etchings (tasks) with Shades

Add etchings with `inkdrop`, assigning Shades such as `TODO`, `INFO`, `DEBUG`, `WARN`, or `ERROR`. Shades allow you to manage and filter etchings effectively.

```python
ink.inkdrop("Refactor this method", Shade=GhostInk.Shade.TODO)
ink.inkdrop("This is debug info", Shade=GhostInk.Shade.DEBUG)
```

### Printing Location Information with `haunt`

If you simply want to print the current file location (file, line, function, and timestamp) without adding a etch, use `haunt`:

```python
ink.haunt("Executing important operation")
```

### Viewing and Filtering etchings with `whisper`

View all tracked etchings using `whisper`, with optional filters by Shade or file name:

```python
ink.whisper(shade_mask=GhostInk.Shade.TODO)
ink.whisper(file_mask="main.py")
```

---

## Key Methods

1. **`haunt(msg: str = None)`**  
   - Prints file, line, function, and timestamp for tracking execution points.
   - **Parameters**:
     - `msg`: Optional message displayed before the file information.

2. **`inkdrop(etch_input: any, Shade: Shade = Shade.TODO)`**  
   - Adds a etch with text and a specific Shade to the etch list.
   - **Parameters**:
     - `etch_input`: Text, dictionary, or object to record as a etch.
     - `Shade`: etch Shade (TODO, INFO, DEBUG, WARN, ERROR).

3. **`whisper(filter_Shade: str = None, filter_filename: str = None)`**  
   - Prints filtered etchings based on Shade and filename.
   - **Parameters**:
     - `shade_mask`: Filter etchings by Shade.
     - `file_mask`: Filter etchings by specific file name.

---

## Example

```python
from ghosink import GhostInk

# Initialize with logging enabled
ink = GhostInk(title="Project Debugger", log_to_file=True)

# Add etchings
ink.inkdrop("Fix memory leak", Shade=GhostInk.Shade.TODO)
ink.inkdrop("Checkpoint reached", Shade=GhostInk.Shade.INFO)
ink.inkdrop("Debug, Error, Warn itchs", Shade=GhostInk.Shade.DEBUG)

# Print a debug statement with file details
ink.haunt("Debugging current function")

# View all etchings
ink.whisper()
```

### Example Output

![example output](assets/example_output.png)

---

## Benefits

- No more manually adding and searching for `print` statements!
- Clearly organized, color-coded outputs make etchings easy to spot and review.
- Optional file logging to retain records and analyze later.
- Filters for viewing etchings by file and Shade allow better focus and etch management.

---

**Start using GhostInk** and turn your debug prints into an organized, colorful log. Perfect for developers who want a better way to keep track of etchings and debug information without losing context!

---

## Inspired By

This project is inspired by the [icecream](https://github.com/gruns/icecream) library.

---

## Contributing

Contributions are welcome! If you have suggestions or improvements, please create a pull request.

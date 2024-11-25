# GhostInk

**GhostInk** is a Python utility to streamline debugging and entry(task) tracking by printing detailed file information for each call. This tool eliminates the need to manually add `print` statements and hunt for line numbers or file names, providing an organized, colorful output to track entries, debug info, and errors across your project.

---

## Installation

To install `GhostInk`, add it to your project with pip:

```bash
pip install ghostink
```

Then, import `GhostInk` into your Python files:

```python
from ghostink import GhostInk
```

---

## Usage

### Initialize GhostInk

To start, create a `GhostInk` instance with optional parameters:

```python
ink = GhostInk(
    title="My Project Debugger",
    project_root=".",  # Set the project root for relative path display
)
```

The environment variable `GHOSTINK` takes precedence over directly passing `project_root` argument during initialization.

### Adding entries (tasks) with Shades

Add entries with `inkdrop`, assigning Shades such as `TODO`, `INFO`, `DEBUG`, `WARN`, or `ERROR`. Shades allow you to manage and filter entries effectively.

```python
ink.inkdrop("Refactor this method", Shade=GhostInk.Shade.TODO)
# inkdrop can be aliased to just drop
ink.drop("This is debug info", Shade=GhostInk.Shade.DEBUG, tags=["database"])
```

### Printing Location Information with `haunt`

If you simply want to print the current file location (file, line, function, and timestamp) without adding a entry, use `haunt`:

```python
# can be aliased to ink.ln()
ink.haunt("Executing important operation")
```

### Viewing and Filtering entries with `whisper`

View all tracked entries using `whisper`, with optional filters by Shade or file name:

```python
ink.whisper(filter_shade=GhostInk.Shade.TODO)
ink.whisper(filter_file="main.py")
ink.whisper(filter_tag=["database"]) # str type can also be passed
```

---

## Key Methods

1. **`haunt(msg: str = None)`**  
   - Prints file, line, function, and timestamp for tracking execution points.
   - **Parameters**:
     - `msg`: Optional message displayed before the file information.

2. **`inkdrop(entry_input: any, Shade: Shade = Shade.TODO, tags: List[str] = []`**
   - Adds an entry with text and a specific Shade to the entry list.
   - **Parameters**:
     - `entry_input`: Text, dictionary, or object to record as a entry.
     - `Shade`: entry Shade (TODO, INFO, DEBUG, WARN, ERROR).
     - `tags`: Tags for the task

3. **`def tabloid(filename: Optional[str] = None):`**:
   - Load a more detailed entry from a file.
   - **Parameters**:
     - `filename`: The name of the file to load the entries from, the files are located in the *`project_root/.ghost/the title of the instance`*.

4. **`whisper(filter_shade: str = None, filter_file: str = None, filter_tag: List[str] = None)`**  
   - Prints filtered entries based on Shade and filename.
   - **Parameters**:
     - `filter_shade`: Filter entries by Shade.
     - `filter_file`: Filter entries by specific file name.
     - `filter_tag`: Filter entries by specific tag (Tag).

5. **`get_shades(self):`**
   - return all the shades

---

## Example

```python
from ghostink import GhostInk

ink = GhostInk(title="Project Debugger")
ink.drop("Fix memory leak", shade=GhostInk.Shade.WARN,
         tags=['leaks', 'memory'])
shades = ink.get_shades()
ink.drop("Checkpoint reached", shade=shades.INFO)
ink.drop("this is an importatnt TODO note DO NOT IGNORE")


ink.whisper(filter_tag=['memory'])

ink.haunt('just another line')

```

### Example Output

```bash
   Project Debugger

[WARN] Fix memory leak
 #leaks   #memory
(Ln:4 - <module> in ghostink/main.py)

Printed from: ghostink/main.py at line 13
Review completed entries and remove them as necessary.

just another line
└── main.py:15 in <module>() at 03:50:40``
```

---

## An import trick

- to make `GhostInk` available in all file projects without the import statements, you can use `ghostall()`.

```python
# in a parentfile
from ghostink import ghostall
from subfile import buster
ghostall()

buster()
```

```python
# in a subfile
def buster():
  ink = GhostInk()
  ink.drop('now it work like a builtin function')
  ink.whisper()
```

---

## **`Ghosty`** cli: soon

---

## Benefits

- No more manually adding and searching for `print` statements!
- Clearly organized, color-coded outputs make entries easy to spot and review.
- Optional file logging to retain records and analyze later.
- Filters for viewing entries by file and Shade allow better focus and entry management.

---

**Start using GhostInk** and turn your debug prints into an organized, colorful log. Perfect for developers who want a better way to keep track of entries and debug information without losing context!

---

## Inspired By

This project is inspired by the [icecream](https://github.com/gruns/icecream) library.

---

## GhostInk in other languages

- Go: [GhostInk](https://github.com/Yandelf00/GhostInk.git)

---

## Contributing

Contributions are welcome! If you have suggestions or improvements, please create a pull request.

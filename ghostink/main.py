from ghostink import GhostInk

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

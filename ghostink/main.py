from ghostink import GhostInk

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

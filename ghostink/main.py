from ghostink import GhostInk

# Initialize with logging enabled
ink = GhostInk(title="Project Debugger", log_to_file=True)

# Add etchings
ink.inkdrop("Fix memory leak", shade=GhostInk.Shade.TODO)
ink.inkdrop("Checkpoint reached", shade=GhostInk.Shade.INFO, echoes=["t", "h"])
ink.inkdrop("Debug, Error, Warn itchs",
            shade=GhostInk.Shade.DEBUG, echoes=["test", "hi bck"])

# Print a debug statement with file details

# View all etchings
# ink.whisper(echo_mask=["h"])
ink.whisper()
# ink.whisper()

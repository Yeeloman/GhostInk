from ghostink import GhostInk

ink = GhostInk(title="Project Debugger")
ink.drop("Fix memory leak", shade=GhostInk.Shade.WARN,
         echoes=['leaks', 'memory'])
ink.drop("Checkpoint reached", shade=GhostInk.Shade.INFO)
ink.drop("this is an importatnt TODO note DO NOT IGNORE")

ink.whisper()

ink.ln()

ink.whisper(echo_mask=['memory'])

ink.haunt('just another line')

ink.whisper(shade_mask=ink.Shade.WARN)

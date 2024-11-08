from ghostink import GhostInk


ink = GhostInk()
shade = ink.get_shades()
ink.drop("test", shade.TODO, ['testing'])
ink.whisper()

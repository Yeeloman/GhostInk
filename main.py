from ghostink import GhostInk


ink = GhostInk()
shade = ink.get_shades()
ink.drop('this an info ask', shade.INFO, ['database', 'api'])
ink.drop(filename="test")
ink.whisper()

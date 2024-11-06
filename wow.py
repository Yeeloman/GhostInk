from ghostink import ghostall


ghostall()


def func():
    return 1 + 2


ink = GhostInk()

ink.drop(func())
ink.whisper()

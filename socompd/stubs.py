from . import mpdCommand


@mpdCommand("listplaylists")
def listPlaylists():
    return None

@mpdCommand("listplaylistinfo")
def listPlaylistInfo():
    return None

@mpdCommand("commands")
def commands():
    return None

@mpdCommand("tagtypes")
def tagtypes():
    return None

@mpdCommand("urlhandlers")
def urlHandlers():
    return None

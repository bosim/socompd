import mpdserver

from . import mpd, dev


class ListPlaylists(mpdserver.Command):
    pass

mpd.requestHandler.RegisterCommand(ListPlaylists)

class ListPlaylistInfo(mpdserver.Command):
    formatArg=[("name", mpdserver.OptStr)]
    pass

mpd.requestHandler.RegisterCommand(ListPlaylistInfo)

class Commands(mpdserver.Command):
    pass

mpd.requestHandler.RegisterCommand(Commands)

class TagTypes(mpdserver.Command):
    pass

mpd.requestHandler.RegisterCommand(TagTypes)

class UrlHandlers(mpdserver.Command):
    pass

mpd.requestHandler.RegisterCommand(UrlHandlers)

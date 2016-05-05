import mpdserver

from . import mpd, dev, events

class Add(mpdserver.Command):
    formatArg=[("uri", mpdserver.OptStr)]

    def handle_args(self, uri):
        dev.add_uri_to_queue(uri)
        self.playlist.playlist_time = 0
        events['playlist'] = True

mpd.requestHandler.RegisterCommand(Add)

class Clear(mpdserver.Command):
    def handle_args(self):
        dev.clear_queue()
        self.playlist.playlist_time = 0
        events['playlist'] = True

mpd.requestHandler.RegisterCommand(Clear)

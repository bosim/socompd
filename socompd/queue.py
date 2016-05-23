import mpdserver

from . import mpd, dev

class Add(mpdserver.Command):
    formatArg=[("uri", mpdserver.OptStr)]

    def handle_args(self, uri):
        if uri.startswith('http://'):
            uri = uri.replace('http://', 'x-rincon-mp3radio://')
        if uri.find('#') >= 0:
            uri = uri[:uri.find('#')]

        dev.add_uri_to_queue(uri)

mpd.requestHandler.RegisterCommand(Add)

class AddId(Add):
    pass

mpd.requestHandler.RegisterCommand(AddId)

class Clear(mpdserver.Command):
    def handle_args(self):
        dev.clear_queue()

mpd.requestHandler.RegisterCommand(Clear)


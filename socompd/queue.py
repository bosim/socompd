from . import dev

class Add(object):
    #formatArg=[("uri", mpdserver.OptStr)]

    def handle_args(self, uri):
        if uri.startswith('http://'):
            uri = uri.replace('http://', 'x-rincon-mp3radio://')
        if uri.find('#') >= 0:
            uri = uri[:uri.find('#')]

        dev.add_uri_to_queue(uri)

#mpd.requestHandler.RegisterCommand(Add)

class AddId(Add):
    pass

#mpd.requestHandler.RegisterCommand(AddId)

class Clear(object):
    def handle_args(self):
        dev.clear_queue()

#mpd.requestHandler.RegisterCommand(Clear)


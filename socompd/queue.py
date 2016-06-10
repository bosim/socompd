from . import dev, mpdCommand

@mpdCommand("add")
def add(uri):
    if uri.startswith('http://'):
        uri = uri.replace('http://', 'x-rincon-mp3radio://')
    if uri.find('#') >= 0:
        uri = uri[:uri.find('#')]

    dev.add_uri_to_queue(uri)

@mpdCommand("addid")
def addId(uri):
    return add(uri)

@mpdCommand("clear")
def clear():
    dev.clear_queue()


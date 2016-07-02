import time

from socompd import devices, mpdCommand
from socompd.utils import songToText

class playlistStore(object):
    def __init__(self):
        self.playlist = []
        self.version = 0

    def getCurrentPlaylist(self):
        dev = devices.currentDevice()

        if self.playlist and self.version == devices.event_state.playlist_version:
            return self.playlist
        else:
            self.playlist = []

            for i, element in enumerate(dev.get_queue(max_items=9999)):
                song = {
                    'file': element.title, 
                    'id': i, 
                    'title': element.title, 
                    'album': hasattr(element, 'album') and element.album or '',  
                    'artist': hasattr(element, 'creator') and element.creator or ''
                }

                self.playlist.append(song)
            
            self.version = devices.event_state.playlist_version

            return self.playlist

playlist_store = playlistStore()

@mpdCommand("playlistinfo")
def playlistInfo(position=None):
    current_playlist = playlist_store.getCurrentPlaylist()

    if position:
        return songToText(current_playlist[str(position)])
    else:
        result = ""
        for song in current_playlist:
            result += songToText(song)
        return result

@mpdCommand("add")
def add(uri):
    dev = devices.currentDevice()

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
    dev = devices.currentDevice()
    dev.clear_queue()

@mpdCommand("delete")
def delete(id):
    dev = devices.currentDevice()
    pos = int(id)
    dev.remove_from_queue(pos)

@mpdCommand("deleteId")
def deleteId(id):
    dev = devices.currentDevice()
    pos = int(id)
    dev.remove_from_queue(pos)


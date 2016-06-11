import time

from socompd import dev, mpdCommand
from socompd.events import event_state
from socompd.utils import songToText

class playlistStore(object):
    def __init__(self):
        self.playlist = []
        self.version = 0

    def getCurrentPlaylist(self):
        if self.playlist and self.version == event_state.playlist_version:
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
            
            self.version = event_state.playlist_version

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

@mpdCommand("delete")
def delete(id):
    pos = int(id)
    dev.remove_from_queue(pos)

@mpdCommand("deleteId")
def deleteId(id):
    pos = int(id)
    dev.remove_from_queue(pos)


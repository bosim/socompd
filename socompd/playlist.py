import time
import mpdserver

from . import mpd, dev


class MpdPlaylist(mpdserver.MpdPlaylist):
    playlist=[]

    def songIdToPosition(self,i):
        for e in self.playlist:
            if e.songId==i: 
                return e.playlistPosition

    def handlePlaylist(self):
        self.playlist = []
        for i, element in enumerate(dev.get_queue(max_items=9999)):
            self.playlist.append(mpdserver.MpdPlaylistSong(
                file=element.title.encode("utf-8"), songId=i, 
                title=element.title.encode("utf-8"), 
                album=hasattr(element, 'album') and element.album.encode("utf-8") or '',  
                artist=hasattr(element, 'creator') and element.creator.encode("utf-8") or ''
            ))
        return self.playlist

    def delete(self, songid):
        dev.remove_from_queue(songid)

mpd.requestHandler.Playlist=MpdPlaylist

import time
import mpdserver

from . import mpd, dev


class MpdPlaylist(mpdserver.MpdPlaylist):
    playlist=[mpdserver.MpdPlaylistSong(file='file0',songId=0)]

    def songIdToPosition(self,i):
        for e in self.playlist:
            if e.songId==i: 
                return e.playlistPosition


    def handlePlaylist(self):
        if hasattr(self, "playlist") and hasattr(self, "playlist_time"):
            if self.playlist_time + 60 > time.time():
                return self.playlist
        else:
            self.playlist = []
            for i, element in enumerate(dev.get_queue(max_items=9999)):
                self.playlist.append(mpdserver.MpdPlaylistSong(
                    file=element.title.encode("utf-8"), songId=i, 
                    title=element.title.encode("utf-8"), 
                    album=hasattr(element, 'album') and element.album.encode("utf-8") or '',  
                    artist=hasattr(element, 'creator') and element.creator.encode("utf-8") or ''
                ))
            self.playlist_time = int(time.time())
            return self.playlist


    def move(self,i,j):
        pass


mpd.requestHandler.Playlist=MpdPlaylist

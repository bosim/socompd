import time
import mpdserver

from . import mpd, dev

from events import event_state

class MpdPlaylist(mpdserver.MpdPlaylist):
    playlist=[]
    current_version=0
    version_counter=0
    
    def version(self):
        return event_state.playlist_version

    def songIdToPosition(self,i):
        for e in self.playlist:
            if e.songId==i: 
                return e.playlistPosition

    def handlePlaylist(self):

        if event_state.playlist_version == self.current_version:
            return self.playlist

        print "Updated playlist"
        self.playlist = []

        for i, element in enumerate(dev.get_queue(max_items=9999)):
            song = mpdserver.MpdPlaylistSong(
                file=element.title.encode("utf-8"), 
                songId=i, 
                title=element.title.encode("utf-8"), 
                album=hasattr(element, 'album') and element.album.encode("utf-8") or '',  
                artist=hasattr(element, 'creator') and element.creator.encode("utf-8") or ''
            )
            self.playlist.append(song)

        self.current_version = event_state.playlist_version

        return self.playlist

    def delete(self, songid):
        dev.remove_from_queue(songid)

mpd.requestHandler.Playlist=MpdPlaylist

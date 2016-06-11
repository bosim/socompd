import time
import socket

from . import dev, mpdCommand

from .events import event_state, event_thread

class Idle(object):
    def toMpdMsg(self):
        self.socket._sock.settimeout(0.1)

        while True:
            event_thread.lock.acquire()
            orig_playlist_count = event_thread.playlist_count
            orig_transport_count = event_thread.transport_count
            orig_rendering_count = event_thread.rendering_count
            event_thread.lock.release()

            buf = None

            try:
                buf = self.socket.readline()
            except socket.timeout:
                buf = ""
            except socket.error:
                return ""

            if buf == None:
                return ""

            buf = buf.replace('\r', '').replace('\n', '')

            if buf and buf.lower() == "noidle":
                self.socket._sock.settimeout(None)
                return ""

            event_thread.lock.acquire()
            new_playlist_count = event_thread.playlist_count
            new_transport_count = event_thread.transport_count
            new_rendering_count = event_thread.rendering_count
            event_thread.lock.release()            

            if new_playlist_count > orig_playlist_count:
                try:
                    self.socket.write("changed: playlist\nOK\n")
                    self.socket.flush()
                except socket.error:
                    return ""

            if new_transport_count > orig_transport_count:
                try:
                    self.socket.write("changed: player\nOK\n")
                    self.socket.flush()
                except socket.error:
                    return ""

            if new_rendering_count > orig_rendering_count:
                try:
                    self.socket.write("changed: mixer\nOK\n")
                    self.socket.flush()
                except socket.error:
                    return ""



#mpd.requestHandler.RegisterCommand(Idle)

@mpdCommand("currentsong")
def currentSong():
    current_song = dev.get_current_track_info()

    result = ""
    result = result + "file: " + current_song.get('uri') + '\n'
    result = result + "Id: " + str(int(current_song.get('playlist_position'))-1) + '\n'
    result = result + "Position: " + str(int(current_song.get('playlist_position'))-1) + '\n'
    result = result + "Artist: " + current_song.get('artist') + '\n'
    result = result + "Album: " + current_song.get('album') + '\n'
    result = result + "Title: " + current_song.get('title') + '\n'
    result = result + "Name: " + current_song.get('title') + '\n'
        
    return result

@mpdCommand("status")
def status():
    result = ''

    state = event_state.transport_state
        
    if state == 'PAUSED_PLAYBACK':
        result += 'state: pause\n'
    elif state == 'STOPPED':
        result += 'state: stop\n'
    elif state == 'PLAYING':
        result += 'state: play\n'

    result += 'volume: ' + str(event_state.volume) + '\n'
        
    track = dev.get_current_track_info()

    result += "song: " + str(int(track.get('playlist_position'))-1) + "\n"
    result += "songid: " + str(int(track.get('playlist_position'))-1) + "\n"

    (hours, mins, seconds,) = track.get('position').split(':')
    position_seconds =  int(mins) * 60 + int(seconds)

    (hours, mins, seconds,) = track.get('duration').split(':')
    duration_seconds =  int(mins) * 60 + int(seconds)

    result += 'time: ' + str(position_seconds) + ':' + str(duration_seconds) + '\n'
    result += 'elapsed: ' + str(position_seconds) + '.000\n'

    result += "bitrate: 128\n"
    result += "xfade: 0\n"
    #result += "playlist: " + str(self.playlist.version()) + "\n"
    #result += "playlistlength: " + str(self.playlist.length()) + "\n"

    return result

@mpdCommand("stats")
def stats():
    result = ""
    result += "artists: %d\n" % len(dev.music_library.get_artists(max_items=9999))
    result += "albums: %d\n" % len(dev.music_library.get_albums(max_items=9999))
    result += "songs: %d\n" % len(dev.music_library.get_tracks(max_items=9999))
    result += "uptime: -1\n"
    result += "playtime: 100\n"
    result += "db_playtime: -1\n"
    result += "db_update: -1\n"
    return result

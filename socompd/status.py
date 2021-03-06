import time
import socket

from socompd import devices, mpdCommand, mpdIdleCommand
from socompd.playlist import playlist_store

@mpdIdleCommand()
def Idle(s):
    while True:
        orig_playlist_count = devices.event_state.playlist_count
        orig_transport_count = devices.event_state.transport_count
        orig_rendering_count = devices.event_state.rendering_count

        buf = None

        try:
            buf = s.recv(8)

            if not buf:
                return

            buf = buf.decode("utf-8").replace('\r', '').replace('\n', '')

            if buf and buf.lower() == "noidle":
                return

        except socket.timeout:
            buf = bytes()
        except socket.error:
            return

        new_playlist_count = devices.event_state.playlist_count
        new_transport_count = devices.event_state.transport_count
        new_rendering_count = devices.event_state.rendering_count

        if new_playlist_count > orig_playlist_count:
            try:
                s.sendall(bytes("changed: playlist\nOK\n", "utf-8"))
            except socket.error:
                return

        if new_transport_count > orig_transport_count:
            try:
                s.sendall(bytes("changed: player\nOK\n", "utf-8"))
            except socket.error:
                return

        if new_rendering_count > orig_rendering_count:
            try:
                s.sendall(bytes("changed: mixer\nOK\n", "utf-8"))
            except socket.error:
                return

@mpdCommand("currentsong")
def currentSong():
    dev = devices.currentDevice()
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
    dev = devices.currentDevice()
    result = ''

    state = devices.event_state.transport_state
        
    if state == 'PAUSED_PLAYBACK':
        result += 'state: pause\n'
    elif state == 'STOPPED':
        result += 'state: stop\n'
    elif state == 'PLAYING':
        result += 'state: play\n'

    result += 'volume: ' + str(devices.event_state.volume) + '\n'
        
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
    result += "playlistlength: " + str(len(playlist_store.getCurrentPlaylist())) + "\n"
    result += "playlist: " + str(playlist_store.version) + "\n"

    return result

@mpdCommand("stats")
def stats():
    dev = devices.currentDevice()
    result = ""
    result += "artists: %d\n" % len(dev.music_library.get_artists(max_items=9999))
    result += "albums: %d\n" % len(dev.music_library.get_albums(max_items=9999))
    result += "songs: %d\n" % len(dev.music_library.get_tracks(max_items=9999))
    result += "uptime: -1\n"
    result += "playtime: 100\n"
    result += "db_playtime: -1\n"
    result += "db_update: -1\n"
    return result

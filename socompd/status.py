import mpdserver
import time

from . import mpd, dev

from .events import event_state, event_thread

class Idle(mpdserver.Command):
    def handle_args(self):
	pass

    def toMpdMsg(self):
        orig_playlist_count = event_thread.playlist_count
        orig_transport_count = event_thread.transport_count
        orig_rendering_count = event_thread.rendering_count

        result = []

        while True:
            if event_thread.playlist_count > orig_playlist_count:
                result.append("changed: playlist\n")
            if event_thread.transport_count > orig_transport_count:
                result.append("changed: player\n")
            if event_thread.rendering_count > orig_rendering_count:
                result.append("changed: mixer\n")

            if len(result) > 0:
                break

            time.sleep(0.5)

        return "".join(result)


mpd.requestHandler.RegisterCommand(Idle)


class CurrentSong(mpdserver.Command):
    def toMpdMsg(self):
        current_song = dev.get_current_track_info()

        result = ""
	result = result + "Id: " + str(int(current_song.get('playlist_position'))-1) + '\n'
	result = result + "Position: " + str(int(current_song.get('playlist_position'))-1) + '\n'
        result = result + "Artist: " + current_song.get('artist').encode("utf-8") + '\n'
        result = result + "Album: " + current_song.get('album').encode("utf-8") + '\n'
        result = result + "Title: " + current_song.get('title').encode("utf-8") + '\n'
        result = result + "Name: " + current_song.get('title').encode("utf-8") + '\n'
        
        return result

mpd.requestHandler.RegisterCommand(CurrentSong)

class Status(mpdserver.Command):
    def toMpdMsg(self):
        result = ''

        state = event_state.transport_state

	if state == 'PAUSED_PLAYBACK':
	    result += 'state: pause\n'
        elif state == 'STOPPED':
            result += 'state: stop\n'
        elif state == 'PLAYING':
            result += 'state: play\n'

	result += "song: " + str(int(event_state.current_song or 0)-1)  + "\n"
	result += "songid: " + str(int(event_state.current_song or 0)-1) + "\n"

        result += 'volume: ' + str(event_state.volume) + '\n'

	(hours, mins, seconds,) = "0:0:0".split(':')
        position_seconds =  int(mins) * 60 + int(seconds)

	(hours, mins, seconds,) = event_state.current_track_duration and event_state.current_track_duration.split(':') or (0,0,0,)
        duration_seconds =  int(mins) * 60 + int(seconds)

        result += 'time: ' + str(position_seconds) + ':' + str(duration_seconds) + '\n'
        result += 'elapsed: ' + str(position_seconds) + '.000\n'

	result += "bitrate: 128\n"
	result += "xfade: 0\n"
	result += "playlist: 3\n"
	result += "playlistlength: " + str(event_state.playlist_length) + "\n"
        print "Playlist length", event_state.playlist_length
        return result

mpd.requestHandler.RegisterCommand(Status)


class Stats(mpdserver.Command):
    def toMpdMsg(self):
        result = ""
        result += "artists: %d\n" % len(dev.music_library.get_artists(max_items=9999))
        result += "albums: %d\n" % len(dev.music_library.get_albums(max_items=9999))
        result += "songs: %d\n" % len(dev.music_library.get_tracks(max_items=9999))
        result += "uptime: -1\n"
        result += "playtime: 100\n"
        result += "db_playtime: -1\n"
        result += "db_update: -1\n"
        return result

    

mpd.requestHandler.RegisterCommand(Stats)

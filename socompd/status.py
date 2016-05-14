import mpdserver
import time

from Queue import Empty

from . import mpd, dev, sub_rendering, sub_transport

class State(object):
    def __init__(self):
        self.volume = None
        self.playlist_length = None
        self.current_song = None
        self.transport_state = None
        self.current_track_duration = None

event_state = State()

class Idle(mpdserver.Command):
    def handle_args(self):
	pass

    def toMpdMsg(self):
        for i in xrange(0, 100):
            try:
                event = sub_rendering.events.get(timeout=0.5)
                event_state.volume = event.variables.get('volume').get('Master')
                print "Got volume", event_state.volume
                return "changed: mixer\n"
            except Empty:
                pass
            
            try:
                event = sub_transport.events.get(timeout=0.5)
                print event.variables
                event_state.transport_state = event.variables.get('transport_state')
                event_state.playlist_length = event.variables.get('number_of_tracks')
                event_state.current_song = event.variables.get('current_track')
                event_state.current_track_duration = event.variables.get('current_track_duration')
                return "changed: player\n"
            except Empty:
                pass

        return ""

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

        return result

mpd.requestHandler.RegisterCommand(Status)

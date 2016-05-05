import mpdserver
import time

from Queue import Empty

from . import mpd, dev, sub_rendering, sub_transport


class Idle(mpdserver.Command):
    def handle_args(self):
	pass

    def toMpdMsg(self):
        for i in xrange(0, 100):
            try:
                event = sub_rendering.events.get(timeout=0.5)
                return "changed: mixer\n"
            except Empty:
                pass
            
            try:
                event = sub_transport.events.get(timeout=0.5)
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

        info = dev.get_current_transport_info()
        track = dev.get_current_track_info()

        state = info.get('current_transport_state')

        if dev.play_mode == 'NORMAL':
            result += "repeat: 0\n"
            result += "random: 0\n"
        elif dev.play_mode == 'REPEAT_ALL':
            result += "repeat: 1\n"
            result += "random: 0\n"
        elif dev.play_mode == 'SHUFFLE':
            result += "repeat: 1\n"
            result += "random: 1\n"
        elif dev.play_mode == 'SHUFFLE_NOREPEAT':
            result += "repeat: 1\n"
            result += "random: 1\n"

	if state == 'PAUSED_PLAYBACK':
	    result += 'state: pause\n'
        elif state == 'STOPPED':
            result += 'state: stop\n'
        elif state == 'PLAYING':
            result += 'state: play\n'

	result += "song: " + str(int(track.get('playlist_position'))-1) + "\n"
	result += "songid: " + str(int(track.get('playlist_position'))-1) + "\n"

        result += 'volume: ' + str(dev.volume) + '\n'

	(hours, mins, seconds,) = track.get('position').split(':')
        position_seconds =  int(mins) * 60 + int(seconds)

	(hours, mins, seconds,) = track.get('duration').split(':')
        duration_seconds =  int(mins) * 60 + int(seconds)

        result += 'time: ' + str(position_seconds) + ':' + str(duration_seconds) + '\n'
        result += 'elapsed: ' + str(position_seconds) + '.000\n'

	result += "bitrate: 128\n"
	result += "xfade: 0\n"
	result += "playlist: 3\n"
	result += "playlistlength: " + str(self.playlist.length()) + "\n"

        return result

mpd.requestHandler.RegisterCommand(Status)

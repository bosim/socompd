import mpdserver

from . import mpd, dev

class PlayId(mpdserver.PlayId):
    def handle_args(self,songId):
        dev.play_from_queue(songId)

mpd.requestHandler.RegisterCommand(PlayId)

class Play(mpdserver.Command):
    formatArg=[("aux", mpdserver.OptStr)]
    def handle_args(self, aux=None):
        dev.play()

mpd.requestHandler.RegisterCommand(Play)

class Next(mpdserver.Command):
    def handle_args(self):
        dev.next()

mpd.requestHandler.RegisterCommand(Next)

class Previous(mpdserver.Command):
    def handle_args(self):
        dev.previous()

mpd.requestHandler.RegisterCommand(Previous)

class Pause(mpdserver.Command):
    formatArg=[("aux", mpdserver.OptStr)]
    def handle_args(self, **kwargs):
        info = dev.get_current_transport_info()

        if info.get('current_transport_state') == "PAUSED_PLAYBACK":
            dev.play()
        else:
            dev.pause()


mpd.requestHandler.RegisterCommand(Pause)

class SetVol(mpdserver.Command):
    formatArg=[("vol", mpdserver.OptStr)]
    
    def handle_args(self, vol):
        dev.volume = int(vol)

mpd.requestHandler.RegisterCommand(SetVol)

class SeekId(mpdserver.Command):
    formatArg=[
        ("id", mpdserver.OptStr),
        ("pos", mpdserver.OptStr)
    ]

    def handle_args(self, id, pos):
        seconds = int(pos)

        hours = seconds / 3600
        seconds = seconds - (hours * 3600)

        minutes = seconds / 60
        seconds = seconds - (minutes * 60)

        ts = "%02d:%02d:%02d" % (hours, minutes, seconds)
        print ts

        dev.seek(ts)

mpd.requestHandler.RegisterCommand(SeekId)

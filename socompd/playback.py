from . import dev, mpdCommand

@mpdCommand("playid")
def playId(songId):
    dev.play_from_queue(songId)

@mpdCommand("play")
def play(aux=None):
    dev.play()

@mpdCommand("next")
def next():
    dev.next()

@mpdCommand("previous")
def previous():
    dev.previous()

@mpdCommand("pause")
def pause(aux=None):
    info = dev.get_current_transport_info()

    if info.get('current_transport_state') == "PAUSED_PLAYBACK":
        dev.play()
    else:
        dev.pause()

@mpdCommand("setvol")
def setVol(self, vol):
    dev.volume = int(vol)

@mpdCommand("seekid")
def seekId(self, id, pos):
    seconds = int(pos)

    hours = seconds / 3600
    seconds = seconds - (hours * 3600)
    
    minutes = seconds / 60
    seconds = seconds - (minutes * 60)

    ts = "%02d:%02d:%02d" % (hours, minutes, seconds)

    dev.seek(ts)


from . import devices, mpdCommand

@mpdCommand("playid")
def playId(songId):
    dev = devices.currentDevice()

    id = int(songId)
    dev.play_from_queue(id)

@mpdCommand("play")
def play(aux=None):
    dev = devices.currentDevice()
    dev.play()

@mpdCommand("next")
def next():
    dev = devices.currentDevice()
    dev.next()

@mpdCommand("previous")
def previous():
    dev = devices.currentDevice()
    dev.previous()

@mpdCommand("pause")
def pause(aux=None):
    dev = devices.currentDevice()
    info = dev.get_current_transport_info()

    if info.get('current_transport_state') == "PAUSED_PLAYBACK":
        dev.play()
    else:
        dev.pause()

@mpdCommand("setvol")
def setVol(vol):
    dev = devices.currentDevice()
    dev.volume = int(vol)

@mpdCommand("seekid")
def seekId(id, pos):
    dev = devices.currentDevice()

    seconds = int(pos)

    hours = seconds // 3600
    seconds = seconds - (hours * 3600)
    
    minutes = seconds // 60
    seconds = seconds - (minutes * 60)

    ts = "%02d:%02d:%02d" % (hours, minutes, seconds)
    dev.seek(ts)

@mpdCommand("outputs")
def outputs():
    print("Outputs called")
    result = ""

    dev = devices.currentDevice()
    groups = devices.getGroups()

    for (i, group) in enumerate(groups):
        result += "outputid: %d\n" % i
        result += "outputname: %s (%s -%s)\n" % (
            group.uid,
            group.coordinator.player_name, 
            group.coordinator.ip_address
        )

        result += "outputenabled: %d\n" % (dev.uid == group.coordinator.uid)

    return result

@mpdCommand("enableoutput")
def enableOutput(id):
    id = int(id)
    devs = devices.getGroups()

    if id < len(devs):
        devices.selectDevice(devs[id].coordinator)


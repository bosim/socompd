import soco
import urllib
import time

dev = list(soco.discover())[0]

funcs = {}
idle_command = None

def mpdCommand(name):
    def decorator(func):
        funcs[name] = func
        return func

    return decorator

def mpdIdleCommand():
    def decorator(func):
        idle_command = func
        return func

    return decorator

import socompd.server
import socompd.playlist
import socompd.playback
import socompd.queue
import socompd.status
import socompd.collection
import socompd.stubs



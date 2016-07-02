import soco
import urllib
import time

from socompd.events import (
    State, EventTransportThread, EventRenderingThread, EventQueueThread
)

class Devices(object):
    def __init__(self):
        self.devs = list(soco.discover())
        self.dev = self.devs[0]
        self.groups = list(self.dev.all_groups)
        self.event_state = State()

        self.startEventThreads()

    def startEventThreads(self):
        self.event_transport_thread = EventTransportThread(self)
        self.event_transport_thread.start()
        self.event_rendering_thread = EventRenderingThread(self)
        self.event_rendering_thread.start()
        self.event_queue_thread = EventQueueThread(self)
        self.event_queue_thread.start()

    def getGroups(self):
        return self.groups

    def selectDevice(self, dev):
        self.dev = dev
        self.startEventThreads()

    def currentDevice(self):
        return self.dev

devices = Devices()

from socompd.utils import mpdCommand, mpdIdleCommand

import socompd.server
import socompd.playlist
import socompd.playback
import socompd.status
import socompd.collection
import socompd.stubs



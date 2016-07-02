import threading

from queue import Empty

from soco.services import Queue


class State(object):
    def __init__(self):
        self.volume = None
        self.playlist_length = None
        self.current_song = None
        self.transport_state = None
        self.current_track_duration = None
        self.playlist_version = 0
        self.transport_count = 0
        self.playlist_count = 0
        self.rendering_count = 0

class EventTransportThread(threading.Thread):
    def __init__(self, devices):
        super(EventTransportThread, self).__init__()

        self.devices = devices
        dev = self.devices.currentDevice()
        
        self.sub_transport = dev.avTransport.subscribe()

    def run(self):
        while True:
            try:
                event = self.sub_transport.events.get(timeout=1.0)

                self.devices.event_state.transport_state = event.variables.get('transport_state')
                self.devices.event_state.playlist_length = event.variables.get('number_of_tracks')
                self.devices.event_state.current_song = event.variables.get('current_track')
                self.devices.event_state.current_track_duration = event.variables.get('current_track_duration')

                self.devices.event_state.transport_count = self.devices.event_state.transport_count + 1
            except Empty:
                pass

class EventRenderingThread(threading.Thread):
    def __init__(self, devices):
        super(EventRenderingThread, self).__init__()

        self.devices = devices
        dev = self.devices.currentDevice()

        self.sub_rendering = dev.renderingControl.subscribe()

    def run(self):
        while True:
            try:
                event = self.sub_rendering.events.get(timeout=1.0)

                self.devices.event_state.volume = event.variables.get('volume').get('Master')
                self.devices.event_state.rendering_count = self.devices.event_state.rendering_count + 1
            except Empty:
                pass

class EventQueueThread(threading.Thread):
    def __init__(self, devices):
        super(EventQueueThread, self).__init__()
        
        self.devices = devices
        dev = self.devices.currentDevice()

        self.sub_queue = Queue(dev).subscribe()

    def run(self):
        while True:
            try:
                event = self.sub_queue.events.get(timeout=1.0)
                
                self.devices.event_state.playlist_count = self.devices.event_state.playlist_count + 1
                self.devices.event_state.playlist_version = self.devices.event_state.playlist_version + 1
                
            except Empty:
                pass

            


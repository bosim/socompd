import threading

from queue import Empty

from soco.services import Queue

from . import dev


class State(object):
    def __init__(self):
        self.volume = None
        self.playlist_length = None
        self.current_song = None
        self.transport_state = None
        self.current_track_duration = None

        self.playlist_version = 0

event_state = State()


class EventThread(threading.Thread):
    def __init__(self):
        super(EventThread, self).__init__()

        self.sub_rendering = dev.renderingControl.subscribe()
        self.sub_transport = dev.avTransport.subscribe()
        self.sub_queue = Queue(dev).subscribe()
        
        self.playlist_count = 0
        self.transport_count = 0
        self.rendering_count = 0

        self.lock = threading.Lock()

    def run(self):
        while True:
            try:
                event = self.sub_transport.events.get(timeout=0.1)

                event_state.transport_state = event.variables.get('transport_state')
                event_state.playlist_length = event.variables.get('number_of_tracks')
                event_state.current_song = event.variables.get('current_track')
                event_state.current_track_duration = event.variables.get('current_track_duration')

                self.lock.acquire()
                self.transport_count = self.transport_count + 1
                self.lock.release()
            except Empty:
                pass

            try:
                event = self.sub_rendering.events.get(timeout=0.1)
                event_state.volume = event.variables.get('volume').get('Master')
                self.lock.acquire()
                self.rendering_count = self.rendering_count + 1
                self.lock.release()

            except Empty:
                pass

            try:
                event = self.sub_queue.events.get(timeout=0.1)
                self.lock.acquire()
                self.playlist_count = self.playlist_count + 1
                self.lock.release()

                event_state.playlist_version = event_state.playlist_version  + 1
            except Empty:
                pass
            
event_thread = EventThread()
event_thread.start()

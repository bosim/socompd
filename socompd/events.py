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
        self.lock = threading.Lock()
        self.transport_count = 0
        self.playlist_count = 0
        self.rendering_count = 0


event_state = State()

class EventTransportThread(threading.Thread):
    def __init__(self):
        super(EventTransportThread, self).__init__()
        self.sub_transport = dev.avTransport.subscribe()

    def run(self):
        while True:
            try:
                event = self.sub_transport.events.get(timeout=1.0)

                event_state.lock.acquire()
                event_state.transport_state = event.variables.get('transport_state')
                event_state.playlist_length = event.variables.get('number_of_tracks')
                event_state.current_song = event.variables.get('current_track')
                event_state.current_track_duration = event.variables.get('current_track_duration')

                event_state.transport_count = event_state.transport_count + 1
                event_state.lock.release()
            except Empty:
                pass


class EventQueueThread(threading.Thread):
    def __init__(self):
        super(EventQueueThread, self).__init__()
        self.sub_queue = Queue(dev).subscribe()

    def run(self):
        while True:
            try:
                event = self.sub_queue.events.get(timeout=1.0)
                
                event_state.lock.acquire()
                event_state.playlist_count = event_state.playlist_count + 1
                event_state.playlist_version = event_state.playlist_version  + 1
                event_state.lock.release()
                
            except Empty:
                pass

class EventRenderingThread(threading.Thread):
    def __init__(self):
        super(EventRenderingThread, self).__init__()
        self.sub_rendering = dev.renderingControl.subscribe()

    def run(self):
        while True:
            try:
                event = self.sub_rendering.events.get(timeout=1.0)

                event_state.lock.acquire()
                event_state.volume = event.variables.get('volume').get('Master')
                event_state.rendering_count = event_state.rendering_count + 1
                event_state.lock.release()
            except Empty:
                pass

            
event_transport_thread = EventTransportThread()
event_transport_thread.start()
event_queue_thread = EventQueueThread()
event_queue_thread.start()
event_rendering_thread = EventRenderingThread()
event_rendering_thread.start()


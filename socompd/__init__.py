import soco
import urllib
import time

dev = list(soco.discover())[0]

from socompd.utils import mpdCommand, mpdIdleCommand

import socompd.server
import socompd.playlist
import socompd.playback
import socompd.status
import socompd.collection
import socompd.stubs



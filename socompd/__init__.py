import mpdserver
import soco
import urllib
import time

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

dev = list(soco.discover())[0]

mpd=mpdserver.MpdServerDaemon(9999)
mpd.requestHandler.RegisterCommand(mpdserver.Outputs)

sub_rendering = dev.renderingControl.subscribe()
sub_transport = dev.avTransport.subscribe()

import playlist
import playback
import queue
import status
import collection
import stubs

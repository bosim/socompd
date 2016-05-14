#!/usr/bin/python
""" This is a simple howto example."""

import socompd


# Set the user defined playlist class

print """Starting a mpd server on port 9999
Type Ctrl+C to exit

To try it, type in another console
$ mpc -p 9999 play
Or launch a MPD client with port 9999
"""
if __name__ == "__main__":
    try:
        while socompd.mpd.wait(1) : pass
    except KeyboardInterrupt:
        print "Stopping MPD server"
        socompd.mpd.quit()


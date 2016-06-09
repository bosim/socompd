#!/usr/bin/python

import socompd
import socketserver

class ThreadedTCPServer(
        socketserver.ThreadingMixIn, socketserver.TCPServer
):
    pass

# Set the user defined playlist class

print (" Starting a mpd server on port 9999\n"
  "Type Ctrl+C to exit\n\n"
  "To try it, type in another console\n"
  "$ mpc -p 9999 play\n"
  "Or launch a MPD client with port 9999 "
)

if __name__ == "__main__":

    server = ThreadedTCPServer(
        ("localhost", 9999), 
        socompd.server.MpdHandler
    )

    server.serve_forever()


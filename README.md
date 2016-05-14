# socompd
A minimal implementation of mpd that relay commands to Sonos. So this program acts as a mpd proxy i.e. you can use a mpd client for controlling your Sonos device.

This is work in progress

# Installing

* You need https://github.com/bosim/python-mpd-server
* You need https://github.com/SoCo/SoCo
* A mpd client (ideally Cantata)

Create a virtualenv

     $ mkdir src/socompd
     $ virtualenv .
     $ source bin/action

Now get the required components

     (socompd) $ git clone https://github.com/bosim/python-mpd-server.git
     (socompd) $ cd python-mpd-server
     (socompd) $ python setup.py install
     (socompd) $ git clone https://github.com/SoCo/SoCo.git
     (socompd) $ cd SoCo
     (socompd) $ python setup.py install
     (socompd) $ git clone https://github.com/bosim/socompd.git
     (socompd) $ cd socompd
     (socompd) $ python socompd.py

Connect with your mpd client to localhost:9999, notice this only works with one sonos device right now. On the todo list
to be able to select the sonos device.

# What works?

* Playing, stopping, forward, previous on play controls
* Controlling the volume
* Browsing the library
* Showing the queue and partially also modifying it

# Tested client

* Cantata 2.0.0, most things works, except for library, but folders can be browsed.

# Author

* Bo Simonsen <bo@geekworld.dk>

import mpdserver

import urllib

from . import mpd, dev


class LsInfo(mpdserver.Command):
    formatArg=[("directory",mpdserver.OptStr)]

    def toMpdMsg(self):
        result = ""
        if self.args.get('directory'):
            for album in dev.get_albums():
                if album.title.encode("utf-8") == self.args.get('directory'):
                    for track in dev.browse(album):
                        result = result + "file: " + urllib.unquote(track.resources[0].uri).encode("utf-8") + "\n"
            
        else:
            for album in dev.get_albums():
                result = result + "directory: " + album.title.encode("utf-8") + "\n"

        return result

mpd.requestHandler.RegisterCommand(LsInfo)

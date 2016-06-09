import urllib

from . import dev


class LsInfo(object):
    #formatArg=[("directory",mpdserver.OptStr)]

    def toMpdMsg(self):
        result = ""
        if self.args.get('directory', '') and self.args.get('directory', '') != '/':
            for album in dev.get_music_library_information('albums'):
                argument = self.args.get('directory')
                if argument.endswith(album.title.encode("utf-8")):
                    for track in dev.browse(album):
                        result = result + "file: " + urllib.unquote(track.resources[0].uri).encode("utf-8") + "\n"
                        result = result + "Title: " + track.title.encode("utf-8") + "\n"
                        result = result + "Artist: " + track.creator.encode("utf-8") + "\n"
                        result = result + "Album : " + track.album.encode("utf-8") + "\n"
            
        else:
            dirs = []
            for album in dev.get_music_library_information('albums'):
                dirs.append(album.creator.encode("utf-8") + " - " + album.title.encode("utf-8"))
            dirs.sort()
            
            result = '\n'.join(['directory: ' + dirname for dirname in dirs]) + "\n"

        return result

#mpd.requestHandler.RegisterCommand(LsInfo)

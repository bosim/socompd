import urllib
from soco.music_library import MusicLibrary

from . import devices, mpdCommand


@mpdCommand("lsinfo")
def lsInfo(directory=None):
    dev = devices.currentDevice()

    music_library = MusicLibrary(dev)
    result = ""
    if directory and directory != "/":
        for album in music_library.get_music_library_information('albums'):
            if directory.endswith(album.title):
                for track in music_library.browse(album):
                    result += "file: " + urllib.parse.unquote(
                        track.resources[0].uri
                    ) + "\n"
                    result += "Title: " + track.title + "\n"
                    result += "Artist: " + track.creator + "\n"
                    result += "Album : " + track.album + "\n"
            
    else:
        dirs = []
        for album in dev.get_music_library_information('albums'):
            dirs.append(album.creator + " - " + album.title)

        dirs.sort()            

        dirs_str = ['directory: ' + dirname for dirname in dirs]
        result = '\n'.join(dirs_str) + "\n"

    return result



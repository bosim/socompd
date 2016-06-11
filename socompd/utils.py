
def songToText(song):
    result = ""
    if "file" in song:
        result += "file: " + str(song["file"]) + "\n"
    if "id" in song:
        result += "Id: " + str(song["id"]) + "\n"
    if "title" in song:
        result += "Title: " + str(song["title"]) + "\n"
    if "artist" in song:
        result += "Artist: " + str(song["artist"]) + "\n"
    if "album" in song:
        result += "Album: " + str(song["album"]) + "\n"

    return result



class Playlist(object):

  def __init__(self, name):
    self.name = name
    self.tracks = []

  def __str__(self):
    playlistAsStr = "** Playlist %s **" % self.name
    i = 1
    for track in self.tracks:
      if i > 10:
        playlistAsStr += "\n... (%d tracks)" % len(self.tracks)
        break
      playlistAsStr += "\n%s) %s" % (i, str(track))
      i += 1
    return playlistAsStr

  def addTrack(self, track):
    self.tracks.append(track)


class Track(object):

  GM_NAME = "track"
  GM_HITS_KEY = "song_hits"
  GM_TITLE_KEY = "title"
  GM_ID_KEY = "nid"

  def __init__(self, name, artist):
    self.name = name
    self.artist = artist

  def __str__(self):
    return "%s - %s" % (self.name, self.artist)


class Album(object):

  GM_NAME = "album"
  GM_HITS_KEY = "album_hits"
  GM_TITLE_KEY = "name"
  GM_ID_KEY = "albumId"

  def __init__(self, name, artist):
    self.name = name
    self.artist = artist

  def __str__(self):
    return "%s - %s" % (self.name, self.artist)

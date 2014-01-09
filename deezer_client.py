
import requests

from resources import Album, Playlist, Track


class DeezerClient(object):

  _BASE_URI = "http://api.deezer.com"

  def __init__(self, userId=None):
    self._userId = userId

  def getAlbums(self):
    albums = requests.get("%s/user/%s/albums" % (self._BASE_URI,
                                                 self._userId)).json()
    albumsList = [Album(album["title"].encode("utf-8"),
                  album["artist"]["name"].encode("utf-8")) \
                 for album in albums["data"]]
    while albums.get("next"):
      albums = requests.get(albums["next"]).json()
      albumsList += [Album(album["title"].encode("utf-8"),
                          album["artist"]["name"].encode("utf-8")) \
                          for album in albums["data"]]
    return albumsList

  def getPlaylistsIds(self):
    playlists = requests.get("%s/user/%s/playlists" % (self._BASE_URI,
                                                       self._userId)).json()
    return [playlist["id"] for playlist in playlists["data"]]

  def getTotalNbTracks(self):
    playlists = requests.get("%s/user/%s/playlists" % (self._BASE_URI,
                                                       self._userId)).json()
    return sum([playlist["nb_tracks"] for playlist in playlists["data"]])

  def getPlaylist(self, playlistId):
    playlistDict = requests.get("%s/playlist/%s" % (self._BASE_URI,
                                                    playlistId)).json()
    playlist = Playlist(playlistDict["title"].encode("utf-8"))
    for track in playlistDict["tracks"]["data"]:
      playlist.addTrack(Track(track["title"].encode("utf-8"),
                              track["artist"]["name"].encode("utf-8")))
    return playlist

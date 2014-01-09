import logging
import re

from gmusicapi import Mobileclient
from resources import Track

LOGGER = logging.getLogger(__name__)


class GoogleMusicClient(object):

  def __init__(self, username, password):
    self._username = username
    self._password = password
    self._apiClient = None

  def initConnection(self):
    self._apiClient = Mobileclient(debug_logging=False)
    if not self._apiClient.login(self._username, self._password):
      raise RuntimeError("Could not connect %s to Google Music." % \
                          self._username)

  def addPlaylist(self, playlist):
    plid = self._apiClient.create_playlist(playlist.name)
    tids = []
    for track in playlist.tracks:
      aaid = self._getAllAccessTrackId(track)
      if aaid:
        try:
          tid = self._apiClient.add_aa_track(aaid)
          if tid:
            tids.append(tid)
          else:
            LOGGER.warning( "Could not add track %s to library.", str(track))
        except:
          LOGGER.error("Could not add track %s to library.", str(track))
          continue
      else:
        LOGGER.warning("Track %s not found.", str(track))
    self._apiClient.add_songs_to_playlist(plid, tids)

  def addAlbum(self, album):
    aaid = self._getAllAccessAlbumId(album)
    if aaid:
      albumInfo = self._apiClient.get_album_info(aaid, include_tracks=True)
      for track in albumInfo["tracks"]:
        try:
          self._apiClient.add_aa_track(track[Track.GM_ID_KEY])
        except:
          LOGGER.error("Could not add track %s to library.", str(track))
          continue
    else:
      LOGGER.warning("Album %s not found.", str(album))

  def _getAllAccessFirstResult(self, resource):
    queryStr = re.sub("[-:\(\)\",]","", "%s %s" % (resource.name,
                                                   resource.artist))
    queryStr = re.sub("\s+", "+", queryStr)
    searchResults = self._apiClient.search_all_access(queryStr)
    gmusicResources = searchResults.get(resource.GM_HITS_KEY)
    if gmusicResources:
      firstResult = gmusicResources[0][resource.GM_NAME]
      return firstResult[resource.GM_ID_KEY]
    else:
      return None

  def _getAllAccessTrackId(self, track):
    return self._getAllAccessFirstResult(track)

  def _getAllAccessAlbumId(self, album):
    return self._getAllAccessFirstResult(album)

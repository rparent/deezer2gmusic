from argparse import ArgumentParser
import getpass
import logging
import logging.config
import sys

from deezer_client import DeezerClient
from google_music_client import GoogleMusicClient
from resources import Playlist

logging.config.fileConfig("./logging.conf")
LOGGER = logging.getLogger("deezer2gmusic")


class Synchronizer(object):

  def __init__(self, deezerClient, gmusicClient):
    self._deezerClient = deezerClient
    self._gmusicClient = gmusicClient

  def initConnection(self):
    self._gmusicClient.initConnection()

  def syncPlaylists(self, forceYes=False):
    playlistsDeezerIds = self._deezerClient.getPlaylistsIds()
    for plid in playlistsDeezerIds:
      playlist = self._deezerClient.getPlaylist(plid)
      if forceYes:
        LOGGER.info("Syncing playlist %s..." % playlist.name)
      else:
        LOGGER.info(str(playlist))
        answer = raw_input("Do you want to sync this playlist to gmusic? [y/N]")
        if answer.lower() not in ["y", "yes"]:
          continue
      self._gmusicClient.addPlaylist(playlist)

  def syncAlbums(self, forceYes=False):
    deezerAlbums = self._deezerClient.getAlbums()
    for album in deezerAlbums:
      LOGGER.info(str(album))
      if not forceYes:
        answer = raw_input("Do you want to sync this album to gmusic? [y/N]")
        if answer.lower() not in ["y", "yes"]:
          continue
      self._gmusicClient.addAlbum(album)


def main():
  argParser = ArgumentParser(description="Synchronize your Deezer music to "
                                         "Google Music")
  argParser.add_argument("-d", "--deezer-uid", dest="deezer_uid", type=str,
                         help="Your Deezer user id", required=True)
  argParser.add_argument("-g", "--gmusic-username", dest="gmusic_username",
                         help="Your Google user name", required=True, type=str)
  argParser.add_argument("-p", "--playlists", dest="sync_playlists",
                         action="store_true", help="Add this option to sync "
                         "your Deezer playlists to Google Music")
  argParser.add_argument("-a", "--albums", dest="sync_albums",
                         action="store_true", help="Add this option to sync "
                         "your Deezer albums to Google Music")
  argParser.add_argument("-f", "--force", dest="force_yes", action="store_true",
                         help="Add this option to force yes all answers.")
  args = argParser.parse_args()
  if not args.sync_playlists and not args.sync_albums:
    print "You must specify at least one of -p or -a options."
    argParser.print_help()
    sys.exit(1)
  gmusicPassword = getpass.getpass("Please enter your google music password: ")
  deezerClient = DeezerClient(args.deezer_uid)
  gmusicClient = GoogleMusicClient(args.gmusic_username, gmusicPassword)
  synchronizer = Synchronizer(deezerClient, gmusicClient)
  synchronizer.initConnection()
  if args.sync_albums:
    synchronizer.syncAlbums(args.force_yes)
  if args.sync_playlists:
    synchronizer.syncPlaylists(args.force_yes)


if __name__ == "__main__":
  main()

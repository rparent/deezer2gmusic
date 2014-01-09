This script adds all your Deezer albums and/or playlists to Google Music.

**Requirements**

You need to install [requests][requests-ws] and [gmusicapi][gmusicapi-ws] before running the script. This can be done with `pip`:

    pip install requests gmusicapi

You also need to have an [All-Access account][aa-account] on Google Music, otherwise you won't be able to add songs that are not already in your library.


**Run the script**

Simply launch script with correct options. A help message is available by typing

    python deezer2gmusic.py -h


[requests-ws]: http://docs.python-requests.org/en/latest/
[gmusicapi-ws]: https://github.com/simon-weber/Unofficial-Google-Music-API
[aa-account]: https://play.google.com/about/music/

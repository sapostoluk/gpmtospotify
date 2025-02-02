#!/usr/bin/env python3

import os
import argparse
import json
from gmusicapi import Mobileclient
import codecs

LIBRARY = 'gpm_library.txt'

def touch_file(name):
    """
    Creates a file if it doesn't exist and returns a bool telling if the file
    existed.
    """
    if not os.path.exists(name):
        print(f'File \'{name}\' not found. Creating it.')
        with open(name, 'w'):
            pass
        return False
    return True


def file_read_json(filename):
    with open(filename, encoding='utf-8') as file:
        return json.load(file)


def file_write_json(filename, container):
    file = codecs.open(filename, 'w', 'utf-8')
    file.write(container)
    file.close()


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--playlist', action='store',
                        help='Stores playlist')
    return parser.parse_args()


def authenticate():
    api = Mobileclient()
    api.perform_oauth(open_browser=True)
    api.oauth_login(Mobileclient.FROM_MAC_ADDRESS)
    return api


def get_songs(library):
    """Returns a new library of songs that only include artist, song, and album"""
    songs = []
    for song in library:
        title, artist = song['title'], song['artist']
        songs.append('{} - {}'.format(title, artist))
    songs2 = '\n'.join(songs)
    return songs2

def get_playlists():
    """returns a list of playlists"""
    api.get_all_playlists()

def main():
    args = parse_args()
    playlist = args.playlist

    api = authenticate()
    library = api.get_all_songs()
    playlists = api.get_all_user_playlist_contents()

    existed = touch_file(LIBRARY)

    new_songs = get_songs(library)

    file_write_json(LIBRARY, new_songs)
    print('Updated library')


if __name__ == '__main__':
    main()

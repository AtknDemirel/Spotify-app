import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import sys

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Search for the playlist by name
playlist_name = 'Top 100 Artists (Monthly Listenership)'
results = sp.search(q=playlist_name, type='playlist')


top10_artists = {}
albums_of_top10_artists = []
songs_of_albums = []

# Retrieve the first matching playlist
if results['playlists']['total'] > 0:
    playlist = results['playlists']['items'][0]
    playlist_id = playlist['id']
    print("Playlist Name:", playlist['name'])
    print("Playlist ID:", playlist_id)

    # Retrieve each track in the playlist
    #for artist,  & popularity
    tracks = sp.playlist_tracks(playlist_id, limit=10)
    file_path = 'artists.txt'  # Path to the file
    with open(file_path, 'w') as file:
        for item in tracks['items']:
            track = item['track']
            artists = track['artists']
            if len(artists) > 0:
                first_artist = artists[0]
                artist_id = first_artist['id']
                artist_name = first_artist['name']

                top10_artists[artist_name] = artist_id
                file.write(f"{artist_name}, ID: {artist_id}\n")

else:
    print("Playlist not found.")
    sys.exit(1)

# Path to the file
album_path = 'albums.txt'  
track_path = 'tracks.txt'

# avaliable markets, total_tracks, release_date, album_type
# check what comes from normal api
with open(album_path, 'w') as album_file, open(track_path, 'w') as track_file:
    for idx, id in enumerate(top10_artists.values()):
        albums = sp.artist_albums(id, album_type='album')  # Limiting to 50 albums in this example
        albums_of_top10_artists.append([id])
        album_file.flush()

        for album in albums['items']:
            album_name = album['name']
            album_id = album['id']
            album_date = album['release_date']
            total_tracks = album['total_tracks']
            album_type = album['album_type']

            albums_of_top10_artists[idx].append(album_name)
            album_file.write(f"Artist ID: {id} || Album ID: {album_id} || Album Name: {album_name} || ")
            album_file.write(f"Release Date: {album_date} || No. of Tracks: {total_tracks} || Album Type: {album_type}\n")

            album_file.flush()
            tracks = sp.album_tracks(album_id)

            for song in tracks['items']:
                song_id = song['id']
                track_full = sp.track(song_id)
                song_name = track_full['name']
                disc_number = track_full['disc_number']
                duration = track_full['duration_ms']
                track_number = track_full['track_number']
                # The number of the track. If an album has several discs, the track number is the number on the specified disc
                available_markets_track = track_full['available_markets']
                popularity = track_full['popularity']
                disc_number_track = track['disc_number']

                all_artists = []
                for dict in song['artists']:
                    all_artists.append(dict['name'])

                track_file.write(f"Artist ID: {id} || Album ID: {album_id} || Song ID: {song_id} || Song Name: {song_name} || ")
                track_file.write(f"All Artists: {str(all_artists)} || Disc Number: {disc_number} || Duration (milliseconds): {duration} || ")
                track_file.write(f"Track Number: {track_number} || Popularity: {popularity} || Disk Number: {disc_number_track} || ")
                track_file.write(f"Available Markets: {str(available_markets_track)}\n")
                
                track_file.flush()
            track_file.write("\n")
        album_file.write("\n")

album_file.close()
track_file.close()

"""
USEFUL DATA WHICH CAN BE ACQUIRED FROM EACH SONG
1. Available Markets -> list of strings -> ['TR']
2. Release Date -> string -> 2023-03-14'
3. Release Date Precision -> string -> 'day'

"""

"""
country_codes = [
    "US",  # United States
    "TR",  # Turkey (officially Türkiye), 
    "RU",  # Russia
    "ZA",  # South Africa
    "NG",  # Nigeria
    "AE",  # United Arab Emirates
    "QA",  # Qatar
    
    "AZ",  # Azerbaijan
    
    "GB",  # United Kingdom
    "IT",  # Italy
    "JP",  # Japan
    "KR",  # South Korea
    "BR",  # Brazil
    "MX",  # Mexico
    "IN",  # India
    "PK",  # Pakistan
    "CN",  # China -> does not return any data
]
"""

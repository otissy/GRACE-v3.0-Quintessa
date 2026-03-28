import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os

class SpotifyManager:
    def __init__(self):
        # Tokens from .env
        scope = "user-library-modify user-read-currently-playing playlist-modify-public playlist-modify-private"
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=os.getenv("SPOTIFY_CLIENT_ID"),
            client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
            redirect_uri=os.getenv("SPOTIFY_REDIRECT_URI", "http://localhost:8888/callback"),
            scope=scope
        ))

    def get_current_track(self):
        track = self.sp.current_user_playing_track()
        if track:
            return {
                "name": track['item']['name'],
                "artist": track['item']['artists'][0]['name'],
                "uri": track['item']['uri']
            }
        return None

    def like_current_song(self):
        current = self.get_current_track()
        if current:
            self.sp.current_user_saved_tracks_add([current['uri']])
            return f"Liked '{current['name']}' by {current['artist']}. Anything else, Stark?"
        return "Nothing playing right now. Want me to sing?"

    def add_to_playlist(self, keyword):
        current = self.get_current_track()
        if not current:
            return "No track found. Play something first."
            
        # 1. Find the playlist ID containing the keyword
        playlists = self.sp.current_user_playlists()
        target_id = None
        for pl in playlists['items']:
            if keyword.lower() in pl['name'].lower():
                target_id = pl['id']
                break
        
        if target_id:
            self.sp.playlist_add_items(target_id, [current['uri']])
            return f"Added '{current['name']}' to your '{pl['name']}' module. Strategic vibing initiated."
        else:
            return f"Couldn't find an orbital module (playlist) matching '{keyword}'."

if __name__ == "__main__":
    sm = SpotifyManager()
    # print(sm.like_current_song())

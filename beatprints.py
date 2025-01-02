import os, dotenv
from BeatPrints import lyrics, poster, spotify

dotenv.load_dotenv()

# Spotify credentials
CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

# Initialize components
ly = lyrics.Lyrics()
ps = poster.Poster("./")
sp = spotify.Spotify(CLIENT_ID, CLIENT_SECRET)

# Search for a track
search = sp.get_track("try everything", limit=1)

# Get the track's metadata and lyrics
metadata = search[0]
lyrics = ly.get_lyrics(metadata)
highlighted_lyrics = ly.select_lines(lyrics, "5-9")

# Generate the track poster
ps.track(metadata, highlighted_lyrics)
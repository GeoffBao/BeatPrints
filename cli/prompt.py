import questionary

from rich import print
# Import submodules explicitly to avoid eager heavy imports via package __init__
from BeatPrints import lyrics as lyrics_mod
from BeatPrints import spotify as spotify_mod
from BeatPrints import poster as poster_mod
from BeatPrints import errors as errors_mod

from cli.conf import *
from cli import exutils, validate

_ly = None
_ps = None
_sp = None


def _get_lyrics():
    global _ly
    if _ly is None:
        _ly = lyrics_mod.Lyrics()
    return _ly


def _get_poster():
    global _ps
    if _ps is None:
        _ps = poster_mod.Poster(POSTERS_DIR)
    return _ps


def _get_spotify():
    global _sp
    if _sp is None:
        _sp = spotify_mod.Spotify(CLIENT_ID, CLIENT_SECRET)
    return _sp


def select_track(limit: int):
    """
    Prompts the user to search for a track and selects one from the results.

    Args:
        limit (int): The maximum number of search results to display.

    Returns:
        TrackMetadata: The selected track from the search results.
    """
    repeat = True
    prompt = f"🎺 • Type out the track you love the most:"

    while repeat:
        query = questionary.text(prompt, style=exutils.default).ask()
        result = _get_spotify().get_track(query, limit=limit)

        # Clear the Screen
        exutils.clear()

        print(f'{len(result)} results found for "{query}"!')
        print(exutils.tablize_track(result))

        repeat = questionary.confirm(
            "🥞 • Not what you wanted? Want to search again?",
            default=True,
            style=exutils.default,
        ).ask()

        if not repeat:
            choice = questionary.text(
                f"🍀 • Select the track you like:",
                validate=validate.NumericValidator(limit=len(result)),
                style=exutils.default,
            ).ask()

            exutils.clear()
            return result[int(choice) - 1]


def select_album(limit: int, shuffle: bool = True):
    """
    Prompts the user to search for an album and selects one from the results.

    Args:
        limit (int): The maximum number of search results to display.
        shuffle (bool): Whether to shuffle the search results. Defaults to True

    Returns:
        AlbumMetadata: The selected album from the search results.
    """
    repeat = True
    prompt = f"💿️ • Type out the album you love the most:"

    while repeat:
        query = questionary.text(prompt, style=exutils.default).ask()
        result = sp.get_album(query, limit, shuffle)

        # Clear the screen
        exutils.clear()

        print(f'{len(result)} results found for "{query}"!')
        print(exutils.tablize_albums(result))

        repeat = questionary.confirm(
            "🥞 • Not what you wanted? Want to search again?",
            default=True,
            style=exutils.default,
        ).ask()

        if not repeat:
            choice = questionary.text(
                f"🍀 • Select the album you like:",
                validate=validate.NumericValidator(limit=len(result)),
                style=exutils.default,
            ).ask()

            exutils.clear()
            return result[int(choice) - 1]


def handle_lyrics(track: spotify.TrackMetadata):
    """
    Retrieves and selects lyrics for a given track.

    Args:
        track (TrackMetadata): The track for which to fetch lyrics.

    Returns:
        str: The selected lyrics from the track.
    """
    try:
        lyrics_result = _get_lyrics().get_lyrics(track)
        print(exutils.format_lyrics(track.name, track.artist, lyrics_result))

        selection_range = questionary.text(
            "🎀 • Select any 4 of your favorite lines (e.g., 2-5, 7-10):",
            validate=validate.SelectionValidator(lyrics_result),
            style=exutils.default,
        ).ask()

        return ly.select_lines(lyrics_result, selection_range)

    except errors_mod.NoLyricsAvailable:
        print("\n😦 • Couldn't find lyrics from sources.")

        return questionary.text(
            "🎀 • Paste your lyrics below:",
            validate=validate.LineCountValidator,
            style=exutils.default,
        ).ask()


def poster_features():
    """
    Prompts the user for poster customization features.

    Returns:
        tuple: A tuple containing theme, accent, and image path options.
    """
    features = questionary.form(
        theme=questionary.select(
            "💫 • Which theme do you prefer?",
            choices=[
                "Light",
                "Dark",
                "Catppuccin",
                "Gruvbox",
                "Nord",
                "RosePine",
                "Everforest",
            ],
            default="Light",
            style=exutils.default,
        ),
        accent=questionary.confirm(
            "🌈 • Add a color accent?", default=False, style=exutils.default
        ),
        cimage=questionary.confirm(
            "🥞 • Use a custom image?", default=False, style=exutils.default
        ),
    ).ask()

    cimage_path = (
        questionary.path(
            "╰─ 🍞 • Provide the file path to the image:",
            validate=validate.ImagePathValidator,
            style=exutils.default,
        )
        .skip_if(not features["cimage"], default=None)
        .ask()
    )

    return features["theme"], features["accent"], cimage_path


def create_poster():
    """
    Creates a poster based on user input.
    """
    try:
        poster_type = questionary.select(
            "🎨 • What type of poster would you like to create?",
            choices=["Song Poster", "Album Poster"],
            style=exutils.default,
        ).ask()

        theme, accent, image = poster_features()

        # Clear the screen
        exutils.clear()

        if poster_type == "Song Poster":
            track = select_track(SEARCH_LIMIT)

            if track:
                lyrics = handle_lyrics(track)
                _get_poster().track(track, lyrics, accent, theme, image)

        else:
            index = questionary.confirm(
                "🍙 • Number the tracks?", style=exutils.default
            ).ask()

            shuffle = questionary.confirm(
                "🚀 • Do you want to shuffle the tracks?", style=exutils.default
            ).ask()

            album = select_album(SEARCH_LIMIT, shuffle)
            if album:
                _get_poster().album(album, index, accent, theme, image)

    except KeyboardInterrupt and KeyError:
        print("🤚 Exiting...")
        exit(0)


def main():
    exutils.clear()
    create_poster()

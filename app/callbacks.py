from aiogram.filters.callback_data import CallbackData

# mypy: ignore-errors


class Lyrics(CallbackData, prefix='lyrics'):
    title: str
    track_id: str


class ArtistAlbum(CallbackData, prefix='artist'):
    title: str
    artist_id: str


class Album(CallbackData, prefix='album'):
    title: str
    album_id: str


class GetAlbum(CallbackData, prefix='get_album'):
    title: str
    album_id: str


class GetAlbumTrackList(CallbackData, prefix='get_album_track_list'):
    title: str
    album_id: str


class Track(CallbackData, prefix='track'):
    title: str
    track_id: str


class GetTrack(CallbackData, prefix='get_track'):
    title: str
    track_id: str


# class ArtistClip(CallbackData, prefix='artist_clip'):
#     title: str
#     artist_id: str


# class Clip(CallbackData, prefix='clip'):
#     title: str
#     clip_id: str
#     clip_title: str

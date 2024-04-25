from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.i18n import gettext as _

from app import callbacks as app_callbacks


async def social_link_title(link):
    if link.type == 'official':
        return '🌐 official'
    return f'🌐 {link.social_network}'


async def get_search_type_keyboard() -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=_('Track 🎵'), callback_data='track'),
                InlineKeyboardButton(text=_('Album 📀'), callback_data='album'),
                InlineKeyboardButton(text=_('Artist 🎤'), callback_data='artist'),
            ],
            [
                InlineKeyboardButton(text=_('Similiar Suggestions 🗒'), callback_data='similar'),
            ]
        ]
    )
    return ikb


async def get_track_extras(track) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=_('{} Lyrics 💬').format(track.title),
                                  callback_data=app_callbacks.Lyrics(title='lyrics', track_id=str(track.id)).pack())],
        ]
    )
    return ikb


async def get_artist_keyboard(artist_brief) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=await social_link_title(link),
                                     url=f'{link.href}') for link in artist_brief.artist.links
            ],
            [
                InlineKeyboardButton(text=_('Get Albums By {} 📀').format(artist_brief.artist.name),
                                     callback_data=app_callbacks.ArtistAlbum(title='artist_album',
                                                                             artist_id=str(artist_brief.artist.id)).pack())
            ],
            # [
            #     InlineKeyboardButton(text=f"Get Music Clips By {artist_brief.artist.name} 📹",
            #                          callback_data=app_callbacks.ArtistClip(title="artist_clip",
            #                                                                 artist_id=str(artist_brief.artist.id)).pack())
            # ]
        ]
    )
    return ikb


async def get_artist_albums_keyboard(albums) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=f'📀  {album.title}  {album.year}',
                                     callback_data=app_callbacks.Album(title='album', album_id=str(album.id)).pack())
            ] for album in albums
        ]
    )
    return ikb


async def get_album_keyboard(album) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=_('🎵  Get Track List'),
                                     callback_data=app_callbacks.GetAlbumTrackList(title='get_album_track_list', album_id=str(album.id)).pack()),
            ],
            [
                InlineKeyboardButton(text=_('📀  Get Album Tracks'),
                                     callback_data=app_callbacks.GetAlbum(title='get_album', album_id=str(album.id)).pack())
            ]

        ]
    )
    return ikb


async def get_album_track_list_keyboard(tracks) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=_('🎵  {}').format(track.title),
                                     callback_data=app_callbacks.GetTrack(title='get_track', track_id=str(track.id)).pack())
            ]for track in tracks

        ]
    )
    return ikb


async def get_track_keyboard(track) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=_('🎵  Get Track'),
                                     callback_data=app_callbacks.GetTrack(title='get_track', track_id=str(track.id)).pack())
            ]
        ]
    )
    return ikb


async def get_artist_clips_keyboard(videos) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=f'📹 {clip.title}', callback_data=app_callbacks.Clip(
                    title='clip', clip_title=clip.title, clip_id=str(clip.provider_video_id)).pack())
            ] for clip in videos
        ]
    )
    return ikb


# async def get_clip_link(title, id) -> InlineKeyboardMarkup:
#     url = f'https://frontend.vh.yandex.ru/player/{id}?no_ad=true&service=ya-video&from=ya-music-android'
#     ikb = InlineKeyboardMarkup(
#         inline_keyboard=[
#             [
#                 InlineKeyboardButton(text=title, url=url)
#             ]
#         ]
#     )
#     return ikb

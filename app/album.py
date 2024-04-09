from aiogram import types
from aiogram.utils.i18n import gettext as _

from app import keyboard, template
from app import track as app_track


async def get_cover(album):
    cover = None

    if album.cover_uri:
        cover_url = (
            f"https://{album.cover_uri.replace('%%', '400x400')}"
        )
        cover = types.URLInputFile(url=cover_url, filename=f'{album.title}.jpeg')
    else:
        cover = types.FSInputFile(
            path='app/images/backup.jpg', filename=f'{album.title}.jpeg'
        )

    return cover


async def get_album(callback, client, album):
    album = await client.albums_with_tracks(album.id)
    tracks = []
    for volume in album.volumes:
        tracks += volume
    for track in tracks:
        await app_track.get_track(callback, track)


async def get_album_track_list(callback, client, album):
    album = await client.albums_with_tracks(album.id)
    tracks = []
    for volume in album.volumes:
        tracks += volume
    return await callback.message.answer(
        text=_('Album Tracks'),
        reply_markup=await keyboard.get_album_track_list_keyboard(tracks)
    )


async def process_album(callback, album):

    title = 'N.A'
    artists = 'N.A'
    genre = 'N.A'
    explicit = 'False'
    year = 'N.A'
    track_count = 'N.A'
    album_caption = await template.get_album_caption_text()

    # with open("debug.txt", "w") as hh:
    #     hh.write(str(album))

    if album.title:
        title = album.title
    if album.artists:
        artists = ', '.join(artist.name for artist in album.artists)
    if album.genre:
        genre = album.genre
    if album.content_warning:
        explicit = 'True'
    if album.year:
        year = album.year
    if album.track_count:
        track_count = album.track_count
    await callback.bot.send_photo(
        callback.message.chat.id,
        photo=await get_cover(album),
        caption=album_caption.format(title, artists, genre, explicit, year, track_count),
        reply_markup=await keyboard.get_album_keyboard(album),
    )

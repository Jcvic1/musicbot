from aiogram import types
from yandex_music import Track

from app import keyboard, template, utils


async def get_cover(track: Track) -> types.URLInputFile | types.FSInputFile:
    cover = None

    if track.cover_uri:
        cover_url = (
            f"https://{track.cover_uri.replace('%%', '400x400')}"
        )
        cover = types.URLInputFile(url=cover_url, filename=f'{track.title}.jpeg')
    else:
        cover = types.FSInputFile(
            path='app/images/backup.jpg', filename=f'{track.title}.jpeg'
        )

    return cover


async def get_track(callback: types.CallbackQuery, track: Track) -> types.CallbackQuery:
    track_thumbnail_url = f"https://{track.cover_uri.replace('%%', '400x400')}"
    download_info = await track.get_download_info_async()
    max_bitrate = max(info.bitrate_in_kbps for info in download_info)
    url = await list(
        filter(
            lambda t: t.codec == 'mp3' and t.bitrate_in_kbps == max_bitrate,
            download_info,
        )
    )[0].get_direct_link_async()

    return await utils.download_audio(callback, track, url, track_thumbnail_url)


async def process_track(callback: types.CallbackQuery, track: Track) -> types.CallbackQuery:

    title = 'N.A'
    artists = 'N.A'
    albums = 'N.A'
    genre = 'N.A'
    explicit = 'False'
    duration = 'N.A'
    year = 'N.A'
    track_position = 'N.A'
    track_caption = await template.get_track_caption_text()

    # with open("debug.txt", "w") as hh:
    #     hh.write(str(track))

    if track.title:
        title = track.title
    if track.artists:
        artists = ', '.join(artist.name for artist in track.artists)
    if track.albums[0]:
        albums = track.albums[0].title
    if track.albums[0].genre:
        genre = track.albums[0].genre
    if track.content_warning:
        explicit = 'True'
    if track.duration_ms:
        duration = await utils.seconds_to_minutes_seconds(track.duration_ms / 1000)
    if track.albums[0].year:
        year = track.albums[0].year
    if track.albums[0].track_position:
        track_position = track.albums[0].track_position.index
    await callback.bot.send_photo(
        callback.message.chat.id,
        photo=await get_cover(track),
        caption=track_caption.format(
            title, artists, albums, genre, explicit, duration, year, track_position
        ),
        reply_markup=await keyboard.get_track_keyboard(track),
    )

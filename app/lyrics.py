import re
import textwrap
from aiogram.utils.markdown import hbold
from aiogram.utils.i18n import gettext as _
from yandex_music.exceptions import NotFoundError


async def remove_timestamps(text):
    timestamp_pattern = r'\[\d{2}:\d{2}\.\d{2}\]'
    text_without_timestamps = re.sub(timestamp_pattern, '', text)

    return text_without_timestamps


async def get_sync_lyrics(callback, track):
    try:
        sync_lyrics = await track.get_lyrics_async('LRC')
        lyrics_with_timestamp = await sync_lyrics.fetch_lyrics_async()
        # with open("debug.txt", "w") as hh:
        #     hh.write(str(lyrics_with_timestamp))
    except NotFoundError:
        await callback.answer()
        await callback.message.answer(
            _("Lyrics Not Found !"),
        )

    else:
        lyrics = await remove_timestamps(lyrics_with_timestamp)
        lyrics_title = f"\n\n{hbold(track.title)}\n\n{hbold(', '.join(artist.name for artist in track.artists))}\n\n"

        full_text = lyrics_title + lyrics

        chunks = textwrap.wrap(full_text, width=4096, replace_whitespace=False)
        await callback.answer()
        for chunk in chunks:
            await callback.message.answer(chunk)


async def get_lyrics(callback, track_id, track):
    supplements = await track.get_supplement_async(track_id)
    try:
        lyrics = supplements.lyrics.full_lyrics
        # with open("debug.txt", "w") as hh:
        #     hh.write(str(lyrics))
    except AttributeError:
        await get_sync_lyrics(callback, track)
    else:
        lyrics = supplements.lyrics.full_lyrics

        lyrics_title = f"\n\n{hbold(track.title)}\n\n{hbold(', '.join(artist.name for artist in track.artists))}\n\n"

        full_text = lyrics_title + lyrics

        chunks = textwrap.wrap(full_text, width=4096, replace_whitespace=False)
        await callback.answer()
        for chunk in chunks:
            await callback.message.answer(chunk)

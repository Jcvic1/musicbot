import os
from datetime import datetime

import aiohttp
import eyed3
from aiogram import types
from aiogram.utils.i18n import gettext as _
from yandex_music import ClientAsync, Search, Track

from app import album as app_album
from app import artist as app_artist
from app import keyboard
from app import track as app_track


async def seconds_to_minutes_seconds(seconds: int) -> str:
    minutes, remainder = divmod(seconds, 60)
    return f'{int(minutes)}:{int(remainder):02d}'


async def calculate_age_and_birthday(birthdate: str) -> tuple[str, bool]:
    date = datetime.strptime(birthdate, '%Y-%m-%d')

    today = datetime.now()

    age = str(today.year - date.year - ((today.month, today.day) < (date.month, date.day)))

    is_birthday_today: bool = today.month == date.month and today.day == date.day

    return age, is_birthday_today


async def download_data(url: str, username: str, type: str) -> str | bytes | None:
    result = None
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if type == 'audio':
                audio_data = await response.read()
                audio_path = f"{username.replace('/', '')}.mp3"
                with open(audio_path, 'wb') as audio_file:
                    audio_file.write(audio_data)

                result = audio_path
            elif type == 'cover':
                cover_data = None
                if response.status == 200:
                    cover_data = await response.read()
                    result = cover_data
                else:
                    result = cover_data

    return result


async def download_audio(callback: types.CallbackQuery, track: Track, audio_url: str, cover_url: str) -> types.CallbackQuery:
    audio_path = await download_data(audio_url, callback.from_user.username, 'audio')

    audiofile = eyed3.load(audio_path)

    if audiofile.tag is None:
        audiofile.tag = eyed3.id3.Tag()

    if track.title:
        audiofile.tag.title = track.title
    if track.artists:
        audiofile.tag.artist = ', '.join(artist.name for artist in track.artists)
    if track.albums:
        audiofile.tag.album = track.albums[0].title
    if track.artists:
        audiofile.tag.album_artist = ', '.join(artist.name for artist in track.artists)
    if track.albums[0].genre:
        audiofile.tag.genre = track.albums[0].genre
    if track.albums[0].year:
        audiofile.tag.recording_date = str(track.albums[0].year)
    if track.albums[0].track_position.index and track.albums[0].track_count:
        audiofile.tag.track_num = (
            track.albums[0].track_position.index,
            track.albums[0].track_count,
        )
        audiofile.tag.duration = track.duration_ms / 1000

    image_data = await download_data(cover_url, callback.from_user.username, 'cover')
    if image_data:
        audiofile.tag.images.set(3, image_data, 'image/jpeg', 'Album Cover')

    audiofile.tag.save()

    await callback.bot.send_audio(
        callback.message.chat.id,
        audio=types.FSInputFile(audio_path, f'{track.title}.mp3'),
        performer=', '.join(artist.name for artist in track.artists),
        caption=_('Album 📀:  {}').format(track.albums[0].title),
        thumbnail=types.BufferedInputFile(image_data, filename=f'{track.title}.jpeg'),
        reply_markup=await keyboard.get_track_extras(track),
    )

    if audio_path:
        os.remove(audio_path)


async def process_choice(callback: types.CallbackQuery, client: ClientAsync, search_result: Search, search_type: str) -> types.CallbackQuery:
    track = search_result.tracks
    album = search_result.albums
    artist = search_result.artists
    if track is not None:
        track = track.results[0]
    if album is not None:
        album = album.results[0]
    if artist is not None:
        artist = artist.results[0]

    if search_type == 'track':
        if track:
            return await app_track.process_track(callback, track)
        return await callback.message.answer(_('Match not found!'))

    if search_type == 'album':
        if album:
            return await app_album.process_album(callback, album)
        return await callback.message.answer(_('Match not found!'))
    if search_type == 'artist':
        if artist:
            return await app_artist.process_artist(callback, client, artist)
        return await callback.message.answer(_('Match not found!'))


async def get_suggestions(callback, suggestions):
    if len(suggestions) > 0:
        return await callback.message.answer(
            text='\n\n'.join(suggestion for suggestion in suggestions)
        )
    return await callback.message.answer(text=_('No suggestions!'))

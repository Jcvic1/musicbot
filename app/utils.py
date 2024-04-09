import os
from datetime import datetime
import aiohttp
import eyed3
from aiogram import types
from aiogram.utils.i18n import gettext as _

from app import keyboard, track as app_track, album as app_album, artist as app_artist


async def seconds_to_minutes_seconds(seconds):
    minutes, remainder = divmod(seconds, 60)
    return f"{int(minutes)}:{int(remainder):02d}"


async def calculate_age_and_birthday(birthdate):
    birthdate = datetime.strptime(birthdate, "%Y-%m-%d")

    today = datetime.now()

    age = str(
        today.year
        - birthdate.year
        - ((today.month, today.day) < (birthdate.month, birthdate.day))
    )

    is_birthday_today = today.month == birthdate.month and today.day == birthdate.day

    return age, is_birthday_today


async def download_data(url, username, type):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if type == "audio":
                audio_data = await response.read()
                audio_path = f"{username.replace('/', '')}.mp3"
                with open(audio_path, "wb") as audio_file:
                    audio_file.write(audio_data)

                return audio_path
            elif type == "cover":
                cover_data = None
                cover_path = None
                if response.status == 200:
                    cover_data = await response.read()
                    return cover_data
                else:
                    return cover_data


async def download_audio(callback, track, audio_url, cover_url):
    audio_path = await download_data(audio_url, callback.from_user.username, "audio")

    audiofile = eyed3.load(audio_path)

    if audiofile.tag is None:
        audiofile.tag = eyed3.id3.Tag()

    if track.title:
        audiofile.tag.title = track.title
    if track.artists:
        audiofile.tag.artist = ", ".join(artist.name for artist in track.artists)
    if track.albums:
        audiofile.tag.album = track.albums[0].title
    if track.artists:
        audiofile.tag.album_artist = ", ".join(artist.name for artist in track.artists)
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

    image_data = await download_data(cover_url, callback.from_user.username, "cover")
    if image_data:
        audiofile.tag.images.set(3, image_data, "image/jpeg", "Album Cover")

    audiofile.tag.save()

    await callback.bot.send_audio(
        callback.message.chat.id,
        audio=types.FSInputFile(audio_path, f"{track.title}.mp3"),
        performer=", ".join(artist.name for artist in track.artists),
        caption=_("Album 📀:  {}").format(track.albums[0].title),
        thumbnail=types.BufferedInputFile(image_data, filename=f"{track.title}.jpeg"),
        reply_markup=await keyboard.get_track_extras(track),
    )

    if audio_path:
        os.remove(audio_path)


async def process_choice(callback, client, search_result, search_type):
    track = search_result.tracks
    album = search_result.albums
    artist = search_result.artists
    if track is not None:
        track = track.results[0]
    if album is not None:
        album = album.results[0]
    if artist is not None:
        artist = artist.results[0]

    if search_type == "track":
        if track:
            return await app_track.process_track(callback, track)
        return await callback.message.answer(_("Match not found!"))

    if search_type == "album":
        if album:
            return await app_album.process_album(callback, album)
        return await callback.message.answer(_("Match not found!"))
    if search_type == "artist":
        if artist:
            return await app_artist.process_artist(callback, client, artist)
        return await callback.message.answer(_("Match not found!"))


async def get_suggestions(callback, suggestions):
    if len(suggestions) > 0:
        return await callback.message.answer(
            text="\n\n".join(suggestion for suggestion in suggestions)
        )
    return await callback.message.answer(text=_("No suggestions!"))

from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import gettext as _
from yandex_music import ClientAsync

from app import album as app_album
from app import callbacks as app_callbacks
from app import config, keyboard, lyrics
from app import state as app_state
from app import track as app_track
from app import utils

music_router = Router()


@music_router.message(app_state.SearchSuggestions.search_input)
async def process_search_input_handler(
    message: types.Message, state: FSMContext
) -> None:
    """
    This handler receives search text
    """
    await state.update_data(search_input=message.text)
    await state.set_state(app_state.SearchSuggestions.search_type)
    await message.answer(
        _('Choose search type.'), reply_markup=await keyboard.get_search_type_keyboard()
    )


@music_router.callback_query(app_state.SearchSuggestions.search_type)
async def process_search_type_handler(
    callback: types.CallbackQuery, state: FSMContext
) -> None:
    """
    This handler receives search type
    """
    client = await ClientAsync(
        token=config.MUSIC_TOKEN, language=config.AppLangConfig.locale
    ).init()

    await state.update_data(search_type=callback.data)
    data = await state.get_data()
    await state.clear()
    search_text = data['search_input']
    search_type = data['search_type']
    if callback.data == 'similar':
        suggestions = (await client.search_suggest(search_text)).suggestions
        await callback.answer()
        await utils.get_suggestions(callback, suggestions)
        await callback.message.answer(
            _('Type Next Search Name.'),
        )
        await state.set_state(app_state.SearchSuggestions.search_input)
    else:
        search_result = await client.search(search_text)
        await callback.answer()
        await utils.process_choice(callback, client, search_result, search_type)


@music_router.callback_query(app_callbacks.Lyrics.filter(F.title == 'lyrics'))
async def lyrics_handler(
    callback: types.CallbackQuery,
    callback_data: app_callbacks.Lyrics,
    state: FSMContext,
) -> None:
    """
    This handler download lyrics
    """

    client = await ClientAsync(
        token=config.MUSIC_TOKEN, language=config.AppLangConfig.locale
    ).init()
    track = (await client.tracks(callback_data.track_id))[0]
    await lyrics.get_lyrics(callback, callback_data.track_id, track)
    await callback.message.answer(
        _('Type Next Search Name.'),
    )
    await state.set_state(app_state.SearchSuggestions.search_input)


@music_router.callback_query(
    app_callbacks.ArtistAlbum.filter(F.title == 'artist_album')
)
async def artist_album_handler(
    callback: types.CallbackQuery, callback_data: app_callbacks.ArtistAlbum
) -> None:
    """
    This handler shows artist album
    """
    client = await ClientAsync(
        token=config.MUSIC_TOKEN, language=config.AppLangConfig.locale
    ).init()
    artist_brief = await client.artists_brief_info(callback_data.artist_id)
    albums = artist_brief.albums
    await callback.answer()
    await callback.message.answer(
        _('Albums by {}').format(artist_brief.artist.name),
        reply_markup=await keyboard.get_artist_albums_keyboard(albums),
    )


@music_router.callback_query(app_callbacks.Album.filter(F.title == 'album'))
async def album_handler(
    callback: types.CallbackQuery, callback_data: app_callbacks.Album
) -> None:
    """
    This handler processes album
    """
    client = await ClientAsync(
        token=config.MUSIC_TOKEN, language=config.AppLangConfig.locale
    ).init()
    album = await client.albums_with_tracks(callback_data.album_id)
    await callback.answer()
    await app_album.process_album(callback, album)


@music_router.callback_query(app_callbacks.GetAlbum.filter(F.title == 'get_album'))
async def get_album_handler(
    callback: types.CallbackQuery,
    callback_data: app_callbacks.GetAlbum,
    state: FSMContext,
) -> None:
    """
    This handler retrievs album
    """
    client = await ClientAsync(
        token=config.MUSIC_TOKEN, language=config.AppLangConfig.locale
    ).init()
    album = await client.albums_with_tracks(callback_data.album_id)
    await callback.answer()
    await app_album.get_album(callback, client, album)
    await state.set_state(app_state.SearchSuggestions.search_input)
    await callback.message.answer(
        _('Type Next Search Name.'),
    )


@music_router.callback_query(
    app_callbacks.GetAlbumTrackList.filter(F.title == 'get_album_track_list')
)
async def get_album_track_list_handler(
    callback: types.CallbackQuery,
    callback_data: app_callbacks.GetAlbumTrackList,
    state: FSMContext,
) -> None:
    """
    This handler retrievs album track list
    """
    client = await ClientAsync(
        token=config.MUSIC_TOKEN, language=config.AppLangConfig.locale
    ).init()
    album = await client.albums_with_tracks(callback_data.album_id)
    await callback.answer()
    await app_album.get_album_track_list(callback, client, album)
    await state.set_state(app_state.SearchSuggestions.search_input)
    await callback.message.answer(
        _('Type Next Search Name.'),
    )


@music_router.callback_query(app_callbacks.Track.filter(F.title == 'track'))
async def track_handler(
    callback: types.CallbackQuery, callback_data: app_callbacks.Track
) -> None:
    """
    This handler processes track
    """
    client = await ClientAsync(
        token=config.MUSIC_TOKEN, language=config.AppLangConfig.locale
    ).init()
    track = (await client.tracks(callback_data.track_id))[0]
    await app_track.process_track(callback, track)


@music_router.callback_query(app_callbacks.GetTrack.filter(F.title == 'get_track'))
async def get_track_handler(
    callback: types.CallbackQuery,
    callback_data: app_callbacks.GetTrack,
    state: FSMContext,
) -> None:
    """
    This handler retrieves track
    """
    client = await ClientAsync(
        token=config.MUSIC_TOKEN, language=config.AppLangConfig.locale
    ).init()
    track = (await client.tracks(callback_data.track_id))[0]
    await callback.answer()
    await app_track.get_track(callback, track)
    await state.set_state(app_state.SearchSuggestions.search_input)
    await callback.message.answer(
        _('Type Next Search Name.'),
    )


@music_router.callback_query(app_callbacks.ArtistClip.filter(F.title == 'artist_clip'))
async def artist_clip_handler(
    callback: types.CallbackQuery, callback_data: app_callbacks.ArtistClip
) -> None:
    """
    This handler shows artist clip
    """
    client = await ClientAsync(
        token=config.MUSIC_TOKEN, language=config.AppLangConfig.locale
    ).init()
    artist_brief = await client.artists_brief_info(callback_data.artist_id)
    clips = artist_brief.videos
    await callback.answer()
    await callback.message.answer(
        _('Clips by {}').format(artist_brief.artist.name),
        reply_markup=await keyboard.get_artist_clips_keyboard(clips),
    )


@music_router.callback_query(app_callbacks.Clip.filter(F.title == 'clip'))
async def clips_handler(
    callback: types.CallbackQuery, callback_data: app_callbacks.Clip
) -> None:
    """
    This handler processes clips
    """
    await callback.answer()
    await callback.message.answer(
        callback_data.clip_title,
        reply_markup=await keyboard.get_clip_link(
            callback_data.clip_title, callback_data.clip_id
        ),
    )

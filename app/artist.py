from aiogram import types
from aiogram.utils.i18n import gettext as _
from app import keyboard, template, utils


async def get_cover(artist_brief):
    cover = None

    if artist_brief.artist.cover:
        artist_cover_url = (
            f"https://{artist_brief.artist.cover.uri.replace('%%', '400x400')}"
        )
        cover = types.URLInputFile(
            url=artist_cover_url, filename=f"{artist_brief.artist.name}.jpeg"
        )
    else:
        cover = types.FSInputFile(
            path="app/images/backup.jpg", filename=f"{artist_brief.artist.name}.jpeg"
        )

    return cover


async def process_artist(callback, client, artist):
    artist_brief = await client.artists_brief_info(artist.id)

    name = "N.A"
    fullname = "N.A"
    birth = "N.A"
    age = "N.A"
    genres = "N.A"
    description = "N.A"
    countries = "N.A"
    is_birthday_today = False
    artist_caption = await template.get_artist_caption_text()

    # with open("debug.txt", "w") as hh:
    #     hh.write(str(artist_brief))


    if artist_brief.artist.name:
        name = artist_brief.artist.name
    if artist_brief.artist.full_names:
        fullname = ", ".join(name for name in artist_brief.artist.full_names)
    if artist_brief.artist.init_date:
        birth = artist_brief.artist.init_date
        age, is_birthday_today = await utils.calculate_age_and_birthday(birth)
    if artist_brief.artist.genres:
        genres = ", ".join(genre for genre in artist_brief.artist.genres)
    if artist_brief.artist.description:
        description = artist_brief.artist.description.text
    if artist_brief.artist.countries:
        countries = ", ".join(genre for genre in artist_brief.artist.countries)
    await callback.bot.send_photo(
        callback.message.chat.id,
        photo=await get_cover(artist_brief),
        caption=artist_caption.format(
            name, fullname, birth, age, description, countries, genres
        ),
        reply_markup=await keyboard.get_artist_keyboard(artist_brief),
    )

    if is_birthday_today:
        await callback.message.answer(_("🎉🎂  <b>{}</b>  is  <b>{}</b>  today! ").format(name, age))

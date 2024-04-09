from app.config import AppLangConfig

# Command

HELP_EN = (
    "\n\n<b>COMMANDS</b>\n\n"

    "<b>Start</b> -  Starts bot.\n"
    "<b>Refresh</b> - Resets bot for new search if reply is delayed from server or for new search.\n"
    "<b>Cancel</b> - Cancel current state of bot.\n\n"

    "<b>BUTTONS</b>\n\n"

    "<b>Track</b> - Retrieves track details of current search text.\n"
    "<b>Get Track</b> - Retrieves track file.\n"
    "<b>Get Lyrics</b> - Retrieves lyrics of current track if exist.\n\n"

    "<b>Album</b> - Retrieves album details of current search text.\n"
    "<b>Get Track List</b> - Retrieves button for each track in album.\n"
    "<b>Get Album Track</b> - Retrieves all track files in album.\n\n"

    "<b>Artist</b> - Retrieves artist details of current search text.\n"
    "<b>Social Buttons</b> - Redirects to repective links.\n"
    "<b>Get Albums by *Artist name*</b> - Retrieves all albums of current artist.\n\n"

    "<b>Similar Suggestions</b> - Retrieves list of possible similar search text. It is useful when current search result isnt accurate. Retry search with closest from suggestion text.\n\n"

    "<b>HINT</b>\n\n"

    "For more accurate search, add artist name and track title in search text.\n\n"
)


HELP_RU = (
    "\n\n"
    "<b>КОМАНДЫ</b>\n\n"
    "<b>Start</b> -  Запускает бота.\n"
    "<b>Refresh</b> - Сбрасывает бота для нового поиска, если ответ от сервера задерживается или для нового поиска.\n"
    "<b>Cancel</b> -  Отменяет текущее состояние бота.\n\n"

    "<b>КНОПКИ</b>\n\n"

    "<b>Трек</b> - Получает детали трека текущего поискового текста.\n"
    "<b>Получить Трек</b> - Получает файл трека.\n"
    "<b>Получить Текст Песни</b> - Получает текст песни текущего трека, если есть.\n\n"

    "<b>Альбом</b> - Получает детали альбома текущего поискового текста.\n"
    "<b>Получить список треки Альбома</b> - Получает кнопку для каждого трека в альбоме.\n"
    "<b>Получить Треки Альбома</b> - Получает все файлы треков в альбоме.\n\n"

    "<b>Артист</b> - Получает детали артиста текущего поискового текста.\n"
    "<b>Социальные Кинопки</b> - Перенаправляет на соответствующие ссылки.\n"
    "<b>Получить Альбомы от *Имя артиста*</b> - Получает все альбомы текущего артиста.\n\n"

    "<b>Подобные предложения</b> - Получает список возможных похожих текстов поиска. Это полезно, когда текущий результат поиска не точен. Повторите поиск с ближайшим из текста предложения.\n\n"
    
    "<b>ПОДСКАЗКА</b>\n\n"

    "Для более точного поиска добавьте имя артиста и заголовок трека в текст поиска.\n\n"
)
# Track

TRACK_CAPTION_EN = (
    "\n\n<b>Title</b>: {}\n\n"
    "<b>Artist</b>: {}\n\n"
    "<b>Album</b>: {}\n\n"
    "<b>Genre</b>: {}\n\n"
    "<b>Explicit</b>: {}\n\n"
    "<b>Duration</b>: {}\n\n"
    "<b>Year</b>: {}\n\n"
    "<b>Track Position</b>: {}\n\n"
)

TRACK_CAPTION_RU = (
    "\n\n<b>Название</b>: {}\n\n"
    "<b>Артист</b>: {}\n\n"
    "<b>Альбом</b>: {}\n\n"
    "<b>Жанр</b>: {}\n\n"
    "<b>Эксплицит</b>: {}\n\n"
    "<b>Продолжительность</b>: {}\n\n"
    "<b>Год</b>: {}\n\n"
    "<b>Позиция трека</b>: {}\n\n"
)

# Album

ALBUM_CAPTION_EN = (
    "\n\n<b>Title</b>: {}\n\n"
    "<b>Artist</b>: {}\n\n"
    "<b>Genre</b>: {}\n\n"
    "<b>Explicit</b>: {}\n\n"
    "<b>Year</b>: {}\n\n"
    "<b>Track Count</b>: {}\n\n"
)


ALBUM_CAPTION_RU = (
    "\n\n<b>Название</b>: {}\n\n"
    "<b>Артист</b>: {}\n\n"
    "<b>Жанр</b>: {}\n\n"
    "<b>Эксплицит</b>: {}\n\n"
    "<b>Год</b>: {}\n\n"
    "<b>Количество треков</b>: {}\n\n"
)

# Artist

ARTIST_CAPTION_EN = (
    "\n\n<b>Name</b>: {}\n\n"
    "<b>Fullname</b>: {}\n\n"
    "<b>Birth</b>: {}       ""<b>Age</b>: {}\n\n"
    "<b>Description</b>: {}\n\n"
    "<b>Countries</b>: {}\n\n"
    "<b>Genres</b>: {}\n\n"
)

ARTIST_CAPTION_RU = (
    "\n\n<b>Имя</b>: {}\n\n"
    "<b>Полное имя</b>: {}\n\n"
    "<b>Дата pождения</b>: {}\n\n"
    "<b>Возраст</b>: {}\n\n"
    "<b>Описание</b>: {}\n\n"
    "<b>Страны</b>: {}\n\n"
    "<b>Жанры</b>: {}\n\n"
)


async def get_help_text():
    if AppLangConfig.locale == "en":
        return HELP_EN
    return HELP_RU


async def get_track_caption_text():
    if AppLangConfig.locale == "en":
        return TRACK_CAPTION_EN
    return TRACK_CAPTION_RU


async def get_album_caption_text():
    if AppLangConfig.locale == "en":
        return ALBUM_CAPTION_EN
    return ALBUM_CAPTION_RU


async def get_artist_caption_text():
    if AppLangConfig.locale == "en":
        return ARTIST_CAPTION_EN
    return ARTIST_CAPTION_RU

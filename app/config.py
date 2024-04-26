import os

from dotenv import load_dotenv
from yandex_music import ClientAsync

load_dotenv()


BOT_TOKEN = os.environ.get('BOT_TOKEN')
MUSIC_TOKEN = os.environ.get('MUSIC_TOKEN')


class AppLangConfig:
    locale = 'en'


class ClientConfig:
    @staticmethod
    async def init_client():
        return await ClientAsync(
            token=MUSIC_TOKEN, language=AppLangConfig.locale
        ).init()

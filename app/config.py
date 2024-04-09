import os
from dotenv import load_dotenv


load_dotenv()


BOT_TOKEN = os.environ.get("BOT_TOKEN")
MUSIC_TOKEN = os.environ.get("MUSIC_TOKEN")


class AppLangConfig:
    locale = 'en'
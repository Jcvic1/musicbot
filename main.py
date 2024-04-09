import asyncio
import logging

from app.music import music_router
from app.commands import commands_router

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.utils.i18n import I18n, SimpleI18nMiddleware

from app import config, middleware


TOKEN = config.BOT_TOKEN


async def main() -> None:
    # Dispatcher is a root router
    dp = Dispatcher()

    dp.include_routers(
        commands_router,
        music_router,
    )
    i18n = I18n(path="app/locales", default_locale="en", domain="messages")
    SimpleI18nMiddleware(i18n).setup(dp)
    middleware.LocaleMiddleware().setup(dp)

    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())

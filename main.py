import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.utils.i18n import I18n, SimpleI18nMiddleware
from aiohttp import web

from app import config, middleware
from app.commands import commands_router
from app.music import music_router

TOKEN = config.BOT_TOKEN


async def handle_health(request):
    return web.Response(text='OK', status=200)


async def main() -> None:
    # Dispatcher is a root router
    dp = Dispatcher()

    dp.include_routers(
        commands_router,
        music_router,
    )
    i18n = I18n(path='app/locales', default_locale='en', domain='messages')
    SimpleI18nMiddleware(i18n).setup(dp)
    middleware.LocaleMiddleware().setup(dp)

    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)

    app = web.Application()
    app.router.add_get('/', handle_health)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', 8080)
    await site.start()

    logging.info('Health check server started on port 8080')

    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())

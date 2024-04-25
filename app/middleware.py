# middleware.py
from typing import Any, Awaitable, Callable

from aiogram import Router
from aiogram.dispatcher.middlewares.base import BaseMiddleware
from aiogram.types import TelegramObject, User

from app.config import AppLangConfig


class LocaleMiddleware(BaseMiddleware):

    def setup(
        self: BaseMiddleware, router: Router, exclude: set[str] | None = None
    ) -> BaseMiddleware:
        """
        Register middleware for all events in the Router

        :param router:
        :param exclude:
        :return:
        """
        if exclude is None:
            exclude = set()
        exclude_events = {'update', *exclude}
        for event_name, observer in router.observers.items():
            if event_name in exclude_events:
                continue
            observer.outer_middleware(self)
        return self

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        event_from_user: User | None = data.get('event_from_user', None)
        if event_from_user is None or event_from_user.language_code is None:
            AppLangConfig.locale = 'en'
        else:
            AppLangConfig.locale = event_from_user.language_code

        return await handler(event, data)

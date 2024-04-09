# middleware.py
from typing import Any, Awaitable, Callable, Dict, Optional, Set
from aiogram import Router, types
from aiogram.types import TelegramObject, User
from aiogram.dispatcher.middlewares.base import BaseMiddleware
from app.config import AppLangConfig


class LocaleMiddleware(BaseMiddleware):

    def setup(
        self: BaseMiddleware, router: Router, exclude: Optional[Set[str]] = None
    ) -> BaseMiddleware:
        """
        Register middleware for all events in the Router

        :param router:
        :param exclude:
        :return:
        """
        if exclude is None:
            exclude = set()
        exclude_events = {"update", *exclude}
        for event_name, observer in router.observers.items():
            if event_name in exclude_events:
                continue
            observer.outer_middleware(self)
        return self

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        event_from_user: Optional[User] = data.get("event_from_user", None)
        if event_from_user is None or event_from_user.language_code is None:
            AppLangConfig.locale = "en"
        else:
            AppLangConfig.locale = event_from_user.language_code

        return await handler(event, data)
    

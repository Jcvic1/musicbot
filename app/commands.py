import logging
from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.markdown import hbold
from aiogram.utils.i18n import gettext as _

from app import state as app_state, template

commands_router = Router()


@commands_router.message(Command("start"))
async def command_start_handler(message: Message, state: FSMContext) -> None:
    """
    This handler receives messages with `/start` command
    """
    await message.answer(_("Hello, {}!").format(hbold(message.from_user.full_name)))
    await message.answer(
        _("Type Search Name."),
    )
    await state.set_state(app_state.SearchSuggestions.search_input)
    await message.delete()


@commands_router.message(Command("refresh"))
async def command_refresh_handler(message: Message, state: FSMContext) -> None:
    """
    This handler receives messages with `/refresh` command
    """
    await message.answer(
        _("Refreshed."),
    )
    await message.answer(
        _("Type Search Name."),
    )
    await state.set_state(app_state.SearchSuggestions.search_input)
    await message.delete()


@commands_router.message(Command("help"))
async def command_help_handler(message: Message, state: FSMContext) -> None:
    """
    This handler receives messages with `/help` command
    """

    await message.answer(await template.get_help_text())
    await message.answer(
        _("Type Search Name."),
    )
    await state.set_state(app_state.SearchSuggestions.search_input)
    await message.delete()


@commands_router.message(Command("cancel"))
@commands_router.message(F.text.casefold() == "cancel")
async def command_cancel_handler(message: Message, state: FSMContext) -> None:
    """
    Allow user to cancel any action
    """
    current_state = await state.get_state()
    if current_state is None:
        await message.delete()
        return

    logging.info("Cancelling state %r", current_state)
    await state.clear()
    await message.answer(
        _("Cancelled."),
    )
    await message.delete()

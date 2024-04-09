from aiogram.fsm.state import State, StatesGroup


class SearchSuggestions(StatesGroup):
    search_input = State()
    search_type = State()

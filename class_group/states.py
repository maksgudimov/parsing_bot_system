from aiogram.dispatcher.filters.state import StatesGroup, State


class FeedBackState(StatesGroup):
    message = State()

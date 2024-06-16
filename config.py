import os

from aiogram import Bot, types, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

# from starlette.config import Config

# config = Config('.env')
#
# bot = Bot(config("TOKEN"))
# dp = Dispatcher(bot,storage=MemoryStorage())

bot = Bot("7084871412:AAGFKhv7xee9j38gpvEaU0_1O0xgsIkGafA")
dp = Dispatcher(bot=bot, storage=MemoryStorage())
AUTH_TOKEN = "59e37de2edb07ec32618f509c656aea05a6a953a"
CHAT_DISCOUNT_ID = "-1002214932198"
CHAT_FEEDBACK_ID = "-1002230431861"

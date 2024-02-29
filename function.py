import aiogram.utils.markdown as md
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode, WebAppInfo
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.executor import start_webhook
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from config import *


#Рендеринг клавиатуры из списка
def render_reply_kb(list_buttons, user_id):
    kb = ReplyKeyboardMarkup(resize_keyboard=True)

    for key, value in list_buttons.items():
        if key == 'buy':
            kb.add(KeyboardButton(value))
        else:
            kb.add(value)
        
    return kb

def extract_unique_code(text):
    # Extracts the unique_code from the sent /start command.
    return text.split()[1] if len(text.split()) > 1 else None


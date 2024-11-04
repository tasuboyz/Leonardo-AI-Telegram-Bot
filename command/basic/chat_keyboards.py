from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.types.web_app_info import WebAppInfo
from . import config

class Keyboard_Manager:
    def __init__(self):
        self.example_url = 'https://tasuboyz.github.io/Leonardo-AI-interface/'

    def start_keyboard(self):
        keyboard_buttons = []
        keyboard_buttons.append([KeyboardButton(text="Open App", web_app=WebAppInfo(url=f'{self.example_url}?token={config.leonardo_token}'))])
        keyboard = ReplyKeyboardMarkup(keyboard=keyboard_buttons)
        return keyboard
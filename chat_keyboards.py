from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.types.web_app_info import WebAppInfo
import os
from user import UserInfo
from aiogram import types

class Keyboard_Manager:
    def __init__(self):
        self.example_url = 'https://github.com/tasuboyz/aiogram-bot-example'

    def start_keyboard(self):
        keyboard_buttons = []
        keyboard_buttons.append([types.InlineKeyboardButton(text="Model 🤖", switch_inline_query_current_chat=" model")])
        keyboard = types.InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)
        return keyboard
    
    def custom_keyboard(self, alchemy=None, photoreal=None):
        on_alchemy = 'Alchemy V2 🧪✅'
        off_alchemy = 'Alchemy V2 🧪🚫'
        on_photoreal = 'PhotoReal V2 📸✅'
        off_photoreal = 'PhotoReal V2 📸🚫'
        on_off_alchemy = on_alchemy if alchemy else off_alchemy
        on_off_photoreal = on_photoreal if photoreal else off_photoreal
        keyboard_buttons = []
        keyboard_buttons.append([types.InlineKeyboardButton(text=on_off_alchemy, callback_data="alchemy"),
                                 types.InlineKeyboardButton(text=on_off_photoreal, callback_data="photoreal")])
        keyboard_buttons.append([types.InlineKeyboardButton(text="Element ⚡️", switch_inline_query_current_chat='')])
        keyboard_buttons.append([types.InlineKeyboardButton(text="Confirm ✅", callback_data="confirm")])
        keyboard_buttons.append([types.InlineKeyboardButton(text="Cancel ❌", callback_data="cancel")])
        keyboard = types.InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)
        return keyboard
    
    def custom_elements(self):
        keyboard_buttons = []
        keyboard_buttons.append([types.InlineKeyboardButton(text="0.1", callback_data="0.1"),
                                 types.InlineKeyboardButton(text="0.2", callback_data="0.2"),
                                 types.InlineKeyboardButton(text="0.3", callback_data="0.3"),
                                 types.InlineKeyboardButton(text="0.4", callback_data="0.4"),
                                 types.InlineKeyboardButton(text="0.5", callback_data="0.5")])
        keyboard_buttons.append([types.InlineKeyboardButton(text="0.6", callback_data="0.6"),
                                 types.InlineKeyboardButton(text="0.7", callback_data="0.7"),
                                 types.InlineKeyboardButton(text="0.8", callback_data="0.8"),
                                 types.InlineKeyboardButton(text="0.9", callback_data="0.8"),
                                 types.InlineKeyboardButton(text="1", callback_data="0.8")])
        keyboard_buttons.append([types.InlineKeyboardButton(text="-0.1", callback_data="-0.1"),
                                 types.InlineKeyboardButton(text="-0.2", callback_data="-0.2"),
                                 types.InlineKeyboardButton(text="-0.3", callback_data="-0.3"),
                                 types.InlineKeyboardButton(text="-0.4", callback_data="-0.4"),
                                 types.InlineKeyboardButton(text="-0.5", callback_data="-0.5")])
        keyboard_buttons.append([types.InlineKeyboardButton(text="-0.6", callback_data="-0.6"),
                                 types.InlineKeyboardButton(text="-0.7", callback_data="-0.7"),
                                 types.InlineKeyboardButton(text="-0.8", callback_data="-0.8"),
                                 types.InlineKeyboardButton(text="-0.9", callback_data="-0.9"),
                                 types.InlineKeyboardButton(text="-1", callback_data="-1")])
        keyboard_buttons.append([types.InlineKeyboardButton(text="Cancel ❌", callback_data="cancel")])
        keyboard = types.InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)
        return keyboard

    # def inline_image(self):
    #     keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    #     navigation_buttons = [
    #         types.InlineKeyboardButton("<< Previous", callback_data="previous"),
    #         types.InlineKeyboardButton("Next >>", callback_data="next")
    #     ]
    #     keyboard.add(*navigation_buttons)
    #     return keyboard

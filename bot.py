import config

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.types.web_app_info import WebAppInfo

from aiogram import F, Bot, Dispatcher, Router, types
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from user import UserInfo
import instance
import uuid
import shutil
import os
import re
import time
from logger_config import logger
from chat_keyboards import Keyboard_Manager
from state import Form
from leonardo import LeonardoAI
from db import Database
from config import admin_id
from aiogram.enums import ParseMode
from aiogram.utils.markdown import hbold
import json
import asyncio

class BOT():
    def __init__(self):
        self.dp = Dispatcher()
        self.bot = instance.bot
        self.keyboards = Keyboard_Manager()
        self.leonardo = LeonardoAI()
        
        #command
        self.dp.message(CommandStart())(self.command_start_handler) 
        self.dp.message(F.web_app_data)(self.generate_image) 

    async def cancel_operation(self, callback_query: types.CallbackQuery):
        info = UserInfo(callback_query)
        chat_id = info.chat_id
        message_id = info.message_id
        user_id = info.user_id
        await self.bot.edit_message_text(chat_id=chat_id, message_id=message_id, text="Operation delated")

        #self.dp.message(Form.set_text)(self.handle_set_threshold)
    async def copy_bot_name(self, callback_query: types.CallbackQuery):
        await self.bot.edit_chat_invite_link(callback_query.from_user.id, "@TasuAdmin_Bot")

    async def command_start_handler(self, message: Message):
        info = UserInfo(message)
        chat_id = info.chat_id
        try:
            keyboard = self.keyboards.start_keyboard()
            await message.answer("Hallo", reply_markup=keyboard)
        except Exception as ex:
            logger.error(ex)

    async def generate_image(self, message: Message):
        info = UserInfo(message)
        chat_id = info.chat_id
        user_id = info.user_id
        user_name = info.username
        data = json.loads(message.web_app_data.data)
        prompt = data.get('prompt')
        elements = data.get('elements')
        modelId = data.get('modelId')
        preset = data.get('preset').upper()
        size = data.get('size')
        alchemy = data.get('alchemy')
        photoReal = data.get('photoReal')
        result = self.leonardo.generation(prompt, modelId, alchemy=alchemy, highContrast=False, highResolution=True, photoReal=photoReal, elements=elements, presetStyle=preset, size=size)

        generationId = result['sdGenerationJob']['generationId']
        apiCreditCost = result['sdGenerationJob']['apiCreditCost']

        image_url = await self.send_upload_action(generationId, prompt, chat_id)
        if image_url:
            if apiCreditCost < 20:
                await self.bot.send_photo(chat_id, photo=f"{image_url}", caption=f'"`{prompt}`"\n(0)', parse_mode=ParseMode.MARKDOWN)
            else:
                await self.bot.send_photo(chat_id, photo=f"{image_url}", caption=f'"`{prompt}`"\n(0)', parse_mode=ParseMode.MARKDOWN)

    async def send_upload_action(self, generationId, prompt, chat_id):
        await self.bot.send_chat_action(chat_id=chat_id, action="upload_photo")
        await asyncio.sleep(5)  # Attendi 5 secondi prima di inviare di nuovo l'azione
        image_url = self.leonardo.get_image(generationId, prompt)
        if image_url is None:
            return await self.send_upload_action(generationId, prompt, chat_id)  # Richiama la funzione ricorsivamente finché l'immagine non è pronta
        else:
            return image_url

    
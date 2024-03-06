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

class BOT():
    def __init__(self):
        self.dp = Dispatcher()
        self.bot = instance.bot
        self.keyboards = Keyboard_Manager()
        self.leonardo = LeonardoAI()
        
        #command
        self.dp.message(CommandStart())(self.command_start_handler)  
        self.dp.inline_query()(self.inline_query_handler)  
        self.dp.callback_query(F.data == 'alchemy')(self.set_alchemy_photoreal)
        self.dp.callback_query(F.data == 'photoreal')(self.set_alchemy_photoreal)
        self.dp.callback_query(F.data == 'confirm')(self.confirm_prompt)
        self.dp.callback_query(F.data.in_({' '}))(self.copy_bot_name)
        self.dp.callback_query(F.data == '0.1')(self.set_element_point)
        self.dp.callback_query(F.data == '0.2')(self.set_element_point)
        self.dp.callback_query(F.data == '0.3')(self.set_element_point)
        self.dp.callback_query(F.data == '0.4')(self.set_element_point)
        self.dp.callback_query(F.data == '0.5')(self.set_element_point)
        self.dp.callback_query(F.data == '0.6')(self.set_element_point)
        self.dp.callback_query(F.data == '0.7')(self.set_element_point)
        self.dp.callback_query(F.data == '0.8')(self.set_element_point)
        self.dp.callback_query(F.data == '0.9')(self.set_element_point)
        self.dp.callback_query(F.data == '-0.1')(self.set_element_point)
        self.dp.callback_query(F.data == '-0.2')(self.set_element_point)
        self.dp.callback_query(F.data == '-0.3')(self.set_element_point)
        self.dp.callback_query(F.data == '-0.4')(self.set_element_point)
        self.dp.callback_query(F.data == '-0.5')(self.set_element_point)
        self.dp.callback_query(F.data == '-0.6')(self.set_element_point)
        self.dp.callback_query(F.data == '-0.7')(self.set_element_point)
        self.dp.callback_query(F.data == '-0.8')(self.set_element_point)
        self.dp.callback_query(F.data == '-0.9')(self.set_element_point)
        self.dp.callback_query(F.data == 'cancel')(self.cancel_operation)
        self.dp.message(Form.set_selement)(self.set_element)
        self.dp.callback_query(Form.set_selement)
        self.dp.message(F.text)(self.recive_prompt)

    async def cancel_operation(self, callback_query: types.CallbackQuery):
        info = UserInfo(callback_query)
        chat_id = info.chat_id
        message_id = info.message_id
        user_id = info.user_id
        db = Database()
        db.delate_elements(user_id)
        db.delate_option(user_id)
        db.delate_elements(user_id)
        await self.bot.edit_message_text(chat_id=chat_id, message_id=message_id, text="Operation delated")

        #self.dp.message(Form.set_text)(self.handle_set_threshold)
    async def copy_bot_name(self, callback_query: types.CallbackQuery):
        await self.bot.edit_chat_invite_link(callback_query.from_user.id, "@TasuAdmin_Bot")

    async def command_start_handler(self, message: Message):
        info = UserInfo(message)
        chat_id = info.chat_id
        try:
            keyboard = self.keyboards.start_keyboard()
            await message.answer("Hallo!, Choose Model:", reply_markup=keyboard)
        except Exception as ex:
            logger.error(ex)

    async def model_query_handler(self, query: types.InlineQuery):
        results = self.leonardo.get_model()      
        inline_results = []
        try:
            for result in results['custom_models']:
                creatorName = result['creatorName']
                if creatorName == "Leonardo":
                    element_id = result['id']
                    if result['generated_image']:
                        thumbnail_url = result['generated_image']
                        thumbnail_url = thumbnail_url['url']
                    else:
                        thumbnail_url = ''
                    Title = result['name']
                    desciption = result['description']

                    inline_result = types.InlineQueryResultArticle(
                        id=element_id,
                        title=Title,
                        thumbnail_url=thumbnail_url,                   
                        description=desciption,
                        input_message_content=types.InputTextMessageContent(
                            message_text=element_id
                        )
                    )
                    inline_results.append(inline_result)
                    await query.answer(inline_results)
        except Exception as ex:
            logger.error(f"Errore durante l'esecuzione di handle_set_state: {ex}", exc_info=True) 

    async def inline_query_handler(self, query: types.InlineQuery):
        results = self.leonardo.get_element()      
        inline_results = []
        user_id = query.from_user.id
        try:
            for result in results['loras']:
                creatorName = result['creatorName']
                if creatorName == "Leonardo":
                    element_id = result['akUUID']
                    thumbnail_url = result['urlImage']
                    Title = result['name']
                    desciption = result['description']
                    Database().insert_elements_id(element_id, Title)

                    inline_result = types.InlineQueryResultArticle(
                        id=element_id,
                        title=Title,
                        thumbnail_url=thumbnail_url,                   
                        description=desciption,
                        input_message_content=types.InputTextMessageContent(
                            message_text = f"{Title}: 1"
                        ),
                    )
                    inline_results.append(inline_result)

            await query.answer(inline_results)
        except Exception as ex:
            logger.error(f"Errore durante l'esecuzione di handle_set_state: {ex}", exc_info=True)    

    async def set_alchemy_photoreal(self, callback_query: types.CallbackQuery, state: FSMContext):
        info = UserInfo(callback_query)
        db = Database()
        user_id = info.user_id
        message_id = info.message_id
        caption = callback_query.message.text
        data = info.user_data
        option = db.get_option(user_id)
        result = Result(user_id)

        photoreal_current = result.photoreal_current 
        alchemy_current = result.alchemy_current
        prompt = result.prompt
        elements = db.get_element_name(user_id)  # recupera tutti gli element_id per l'utente
        elements_string = "\n".join(elements)
        if option is None:
            if data.startswith('alchemy'):
                db.insert_option(user_id=user_id, alchemy=True, photoreal=False)
                alchemy_current = not alchemy_current
                keyboard = self.keyboards.custom_keyboard(alchemy=alchemy_current, photoreal=photoreal_current)
                if alchemy_current:
                    Alchemy_V2 = "Alchemy V2 🧪"
                else:
                    Alchemy_V2 = ""
                if photoreal_current:
                    PhotoReal_V2 = "PhotoReal V2 📸"
                else:
                    PhotoReal_V2 = ""
            if data.startswith('photoreal'):
                db.insert_option(user_id=user_id, alchemy=False, photoreal=True)
                photoreal_current = not photoreal_current
                keyboard = self.keyboards.custom_keyboard(alchemy=alchemy_current, photoreal=photoreal_current)
                if photoreal_current:
                    PhotoReal_V2 = "PhotoReal V2 📸"
                else:
                    PhotoReal_V2 = ""
                if alchemy_current:
                    Alchemy_V2 = "Alchemy V2 🧪"
                else:
                    Alchemy_V2 = ""

            #db.insert_option(user_id=user_id, alchemy=not alchemy_current, photoreal=photoreal_current)
            
            await self.bot.edit_message_text(chat_id=user_id, message_id=message_id, text = f'"`{prompt}`"\nElements ⚡️:\n{elements_string} \n{Alchemy_V2}\n{PhotoReal_V2}', reply_markup=keyboard, parse_mode=ParseMode.MARKDOWN)
        else:         
            if data.startswith('alchemy'):
                alchemy_current = not alchemy_current
                db.insert_option(user_id=user_id, alchemy=alchemy_current, photoreal=photoreal_current)
                keyboard = self.keyboards.custom_keyboard(alchemy=alchemy_current, photoreal=photoreal_current)
                if photoreal_current:
                    PhotoReal_V2 = "PhotoReal V2 📸"
                else:
                    PhotoReal_V2 = ""
                if alchemy_current:
                    Alchemy_V2 = "Alchemy V2 🧪"
                else:
                    Alchemy_V2 = ""
            if data.startswith('photoreal'):
                photoreal_current = not photoreal_current
                db.insert_option(user_id=user_id, alchemy=alchemy_current, photoreal=photoreal_current)
                keyboard = self.keyboards.custom_keyboard(alchemy=alchemy_current, photoreal=photoreal_current)
                if photoreal_current:
                    PhotoReal_V2 = "PhotoReal V2 📸"
                else:
                    PhotoReal_V2 = ""
                if alchemy_current:
                    Alchemy_V2 = "Alchemy V2 🧪"
                else:
                    Alchemy_V2 = ""
            
            await self.bot.edit_message_text(chat_id=user_id, message_id=message_id, text = f'"`{prompt}`"\nElements ⚡️:\n{elements_string} \n{Alchemy_V2}\n{PhotoReal_V2}', reply_markup=keyboard, parse_mode=ParseMode.MARKDOWN)

    async def recive_prompt(self, message: types.Message, state: FSMContext):
        info = UserInfo(message)
        db = Database()
        user_id = info.user_id
        text = message.text
        try:
            keyboard = self.keyboards.custom_keyboard()
            prompt = await message.answer(text=f'"`{text}`"', reply_markup=keyboard, parse_mode=ParseMode.MARKDOWN)
            await state.set_state(Form.set_selement)  
            post_id = prompt.message_id
            db.insert_prompt(user_id, post_id, text)
        except Exception as ex:
            await self.bot.send_message(admin_id, f"{ex}")
            logger.error(ex)

    async def confirm_prompt(self, Callback: types.CallbackQuery, state: FSMContext):
        info = UserInfo(Callback)
        db = Database()
        user_id = info.user_id
        message_id = info.message_id
        text = Callback.message.text
        try:
            waiting_message = await self.bot.edit_message_text(chat_id=user_id, message_id=message_id,text="waiting...")
            prompt = text.split('\n')[0].strip('"')
            element_pattern = r'([\w\s]+):(-?[\d.]+)'
            #elements = dict(re.findall(element_pattern, text))
            elements = dict((key.strip(), value) for key, value in re.findall(element_pattern, text))
            keys = elements.keys()
            chiavi_stringhe = [str(chiave) for chiave in keys]
            ids = []
            for key in chiavi_stringhe:
                element_id = db.get_element_id(key)
                ids.append(element_id[0])
            corrispondenze = {chiave: id for chiave, id in zip(elements.keys(), ids)}

            elementi_con_id = {corrispondenze[chiave]: valore for chiave, valore in elements.items()}

            alchemy = 'Alchemy V2' in text
            photo_real = 'PhotoReal V2' in text
            await self.handle_set_threshold(Callback, prompt, elementi_con_id, alchemy, photo_real, waiting_message)
            db.delate_elements(user_id)
            db.delate_option(user_id)
            db.delate_elements(user_id)
        except Exception as ex:
            await self.bot.send_message(admin_id, f"{ex}")
            logger.error(ex, exc_info=True)
        finally:
            await state.clear()

    async def set_element(self, message: types.Message):
        info = UserInfo(message)
        user_id = info.user_id
        message_id = info.message_id
        element = message.text
        try:
            keyboard = self.keyboards.custom_elements()
            await message.send_copy(user_id, reply_markup=keyboard)

            db = Database()
            selected_element = element.split(':')[0].strip()
            element_id = db.get_element_id(selected_element)
            element_id = element_id[0]
            db.insert_element(user_id, element_id)  # aspetta che l'operazione di inserimento sia completata
            elements_id = db.get_elements(user_id)  # recupera tutti gli element_id per l'utente
            elements = db.get_element_name(user_id)

            result = Result(user_id)
            prompt = result.prompt
            post_id = result.post_id
            alchemy_current = result.alchemy_current
            photoreal_current = result.photoreal_current

            elements_string = "\n".join(elements)

            if photoreal_current:
                PhotoReal_V2 = "PhotoReal V2 📸"
            else:
                PhotoReal_V2 = ""
            if alchemy_current:
                Alchemy_V2 = "Alchemy V2 🧪"
            else:
                Alchemy_V2 = ""
            db.insert_prompt(user_id, post_id, prompt)
            keyboard = self.keyboards.custom_keyboard(alchemy=alchemy_current, photoreal=photoreal_current)
            await self.bot.edit_message_text(chat_id=user_id, message_id=post_id, text = f'"`{prompt}`"\nElements ⚡️: \n{elements_string} \n{Alchemy_V2}\n{PhotoReal_V2}', reply_markup=keyboard, parse_mode=ParseMode.MARKDOWN)
        except Exception as ex:
            logger.error(f"Errore durante l'esecuzione di handle_set_state: {ex}", exc_info=True)
            await self.bot.send_message(admin_id, f"{ex}")   
        finally:
            await self.bot.delete_message(chat_id=user_id, message_id=message_id)

    async def handle_set_threshold(self, Callback, prompt, elements, alchemy, photo_real, waiting_message):
        info = UserInfo(Callback)
        chat_id = info.chat_id
        user_id = info.user_id
        db = Database()
        #await state.finish()
        try:            
            result = self.leonardo.generation(prompt=prompt, alchemy=alchemy, photoReal=photo_real, elements=elements)
            generationId = result['sdGenerationJob']['generationId']
            apiCreditCost = result['sdGenerationJob']['apiCreditCost']
            db.image_id(user_id, generationId)
            image_id =db.get_image_ids(user_id)
            time.sleep(25)
            image_url = await self.leonardo.get_image(generationId, prompt, photo_real)
            await self.bot.delete_message(chat_id, waiting_message.message_id)
            await self.bot.send_photo(chat_id, photo=f"{image_url}", caption=f"api cost:{apiCreditCost}")
        except Exception as ex:
            logger.error(f"Errore durante l'esecuzione di handle_set_state: {ex}", exc_info=True)
            await self.bot.send_message(admin_id, f"{ex}")   

    async def set_element_point(self, callback: types.CallbackQuery):
        info = UserInfo(callback)
        db = Database()
        chat_id = info.chat_id
        user_id = info.user_id
        message_id = info.message_id
        data = callback.data
        a = callback.message.md_text
        selected_element = a.split(':')[0].strip()
        result = Result(user_id)
        prompt = result.prompt
        post_id = result.post_id
        alchemy_current = result.alchemy_current
        photoreal_current = result.photoreal_current
        if photoreal_current:
            PhotoReal_V2 = "PhotoReal V2 📸"
        else:
            PhotoReal_V2 = ""
        if alchemy_current:
            Alchemy_V2 = "Alchemy V2 🧪"
        else:
            Alchemy_V2 = ""
        elements = db.get_element_name(user_id)

        new_value = f"{selected_element}:{data}"
        elements_id = db.get_element_id(selected_element)
        db.update_gradation(gradation=float(data), element_id=elements_id[0])
        db.insert_element(user_id, f"{selected_element}:{data}")
        new_elements_list = [new_value if s.startswith(selected_element) else s for s in elements]
        new_elements_string = '\n'.join(new_elements_list)

        db.insert_prompt(user_id, post_id, prompt)
        keyboard = self.keyboards.custom_keyboard(alchemy=alchemy_current, photoreal=photoreal_current)
        keyboard_elements = self.keyboards.custom_elements()
        await self.bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=f"{selected_element}:{data}", reply_markup=keyboard_elements)
        await self.bot.edit_message_text(chat_id=user_id, message_id=post_id, text = f'"`{prompt}`"\nElements ⚡️: \n{new_elements_string} \n{Alchemy_V2}\n{PhotoReal_V2}', reply_markup=keyboard, parse_mode=ParseMode.MARKDOWN)
        return
    
class Result():
    def __init__(self, user_id):
        self.db = Database()
        result_prompt = self.db.get_prompt(user_id)  # ora dovresti ottenere il prompt aggiornato
        result_option = self.db.get_option(user_id)
        if result_option:
            self.photoreal_current = result_option[1]
            self.alchemy_current = result_option[0]
        else:
            self.photoreal_current = None
            self.alchemy_current = None
        if result_prompt:
            self.prompt = result_prompt[0]
            self.post_id = result_prompt[1]
        else: 
            self.prompt = None
            self.post_id = None


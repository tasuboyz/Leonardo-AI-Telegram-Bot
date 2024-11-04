from . import config
from aiogram.client.telegram import TelegramAPIServer
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram import Bot
import logging
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

bot_token=config.TOKEN
admin_id = config.admin_id

if config.use_local_api:
    session = AiohttpSession(
            api=TelegramAPIServer.from_base(config.api_base_url)
    )
    bot = Bot(token=bot_token, session=session, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
else:
    bot = Bot(token=bot_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

file_path_map = {}
from aiogram import F, Bot, Dispatcher, Router
from aiogram.filters import CommandStart, Command
from command.basic import instance
from command.user_commands import UserCommands

class BotCommand():
    def __init__(self):
        self.dp = Dispatcher()
        self.bot = instance.bot
        self.user_commands = UserCommands()
        
        #command
        self.dp.message(CommandStart())(self.user_commands.command_start_handler) 
        self.dp.message(F.web_app_data)(self.user_commands.generate_image) 
    
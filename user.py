from aiogram import types

class UserInfo:
    def __init__(self, data):
        if isinstance(data, types.Message):
            user = data.from_user
            self.chat_id = data.chat.id
            self.message_id = data.message_id
            self.text= data.text
        elif isinstance(data, types.CallbackQuery):
            user = data.from_user
            self.chat_id = data.message.chat.id
            self.message_id = data.message.message_id
            self.user_data = data.data
            self.text= data.message.text
        else:
            return None

        self.user_id = user.id
        self.first_name = user.first_name
        self.last_name = user.last_name
        self.username = user.username
        self.language = user.language_code
        
    async def get_user_member(self, user_id, bot):
        chat_id= "YOUR_CHANNEL"
        user_count = await bot.get_chat_member(chat_id, user_id)
        return user_count.status

from aiogram.filters import BaseFilter
from aiogram.types import Message

from app.config_loader import settings

class Admin(BaseFilter): 
    
    async def __call__(self, message: Message) -> bool:  
        if message.from_user.id in settings.bot.admin_ids:
            return True
        await message.answer('Вы не являетесь администратором')
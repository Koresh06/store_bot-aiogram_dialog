from aiogram.filters import BaseFilter
from aiogram.types import Message


class Admin(BaseFilter): 
    
    async def __call__(self, message: Message) -> bool:  
        if int(message.from_user.id ) == 1020781796:
            return True
        await message.answer('Вы не являетесь администратором')
import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram_dialog import setup_dialogs
from fastapi import FastAPI
from app.adminpanel.views import UserAdmin
from app.core.session import create_engine_db, create_sessionmaker
from app.tgbot.middlewares.db_session import DbSessionMiddleware

from app.tgbot.dialogs import dialogs_list
from app.tgbot.handlers import router_list

from app.tgbot.filters.filter import Admin

from .config_loader import settings


logger = logging.getLogger(__name__)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s'
    )
    logger.info('Staring bot')
    
    engine = create_engine_db(settings.db)
    sessionmaker = create_sessionmaker(engine)
    

    bot: Bot = Bot(
        token=settings.bot.token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp: Dispatcher = Dispatcher()
    dp.update.middleware(DbSessionMiddleware(sessionmaker=sessionmaker))
    dp.update.filter(Admin())
    dp.include_routers(*router_list)
    dp.include_routers(*dialogs_list)

    setup_dialogs(dp)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
    

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt as exxit:
        logger.info(f'Бот закрыт: {exxit}')
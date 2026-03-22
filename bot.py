import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.base import BaseStorage
from config import BOT_TOKEN

from handlers import start, expense, income, stats, edit, reset, goals, fun
from database.db import init_db
from database.fsm_storage import DatabaseFSMStorage
from utils.scheduler import start_scheduler

# Включите логирование
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = Bot(token=BOT_TOKEN)
storage = DatabaseFSMStorage()
dp = Dispatcher(storage=storage)

async def main():
    init_db()
    logger.info("✅ База данных инициализирована")

    # Важный порядок: более специфичные фильтры в начале
    start.register(dp)
    goals.register(dp)
    fun.register(dp)
    stats.register(dp)
    edit.register(dp)
    reset.register(dp)
    income.register(dp)
    expense.register(dp)

    logger.info("✅ Хендлеры зарегистрированы")

    start_scheduler(bot)

    logger.info("🤖 Бот запущен и слушает сообщения...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

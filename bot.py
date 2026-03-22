import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.base import BaseStorage
from config import BOT_TOKEN

from handlers import start, expense, income, stats, edit, reset, goals
from database.db import init_db
from database.fsm_storage import DatabaseFSMStorage
from utils.scheduler import start_scheduler

# Включите логирование
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = Bot(token=BOT_TOKEN)
storage = DatabaseFSMStorage()  # 🆕 FSM Storage в БД вместо MemoryStorage
dp = Dispatcher(storage=storage)


async def main():

    init_db()
    logger.info("✅ База данных инициализирована")

    # Важный порядок: более специфичные фильтры в начале
    start.register(dp)      # Команды /start
    goals.register(dp)      # 🆕 Цели (новый обработчик)
    stats.register(dp)      # Статистика
    edit.register(dp)       # Редактирование
    reset.register(dp)      # Сброс
    income.register(dp)     # Доходы (зарплата, доход, фриланс)
    expense.register(dp)    # Расходы (последний, самый общий)

    logger.info("✅ Хендлеры зарегистрированы")

    start_scheduler(bot)

    logger.info("🤖 Бот запущен и слушает сообщения...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

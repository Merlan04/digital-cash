import asyncio
from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from database.db import get_all, get_all_users
import logging

logger = logging.getLogger(__name__)

scheduler = None


def start_scheduler(bot):
    """Инициализирует планировщик"""
    global scheduler

    if scheduler is None:
        scheduler = AsyncIOScheduler()

        # Напоминание каждый день в 20:00 (8 вечера)
        scheduler.add_job(
            send_daily_reminder,
            'cron',
            hour=20,
            minute=0,
            args=[bot]
        )

        scheduler.start()
        logger.info("✅ Планировщик запущен")

    return scheduler


async def send_daily_reminder(bot):
    """Отправляет напоминание всем пользователям"""
    try:
        users = get_all_users()
        today = datetime.now().strftime("%Y-%m-%d")

        for user_id in users:
            try:
                data = get_all(user_id)
                today_transactions = [t for t in data if t[4] == today]

                if not today_transactions:
                    await bot.send_message(
                        user_id,
                        "📝 Напоминание: Вы еще не записали расходы за сегодня!\n"
                        "Пожалуйста, запишите ваши расходы."
                    )
            except Exception as e:
                logger.warning(f"Не удалось отправить напоминание пользователю {user_id}: {e}")
    except Exception as e:
        logger.error(f"Ошибка в send_daily_reminder: {e}")
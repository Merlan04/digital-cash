import asyncio
from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from database.db import get_all, get_all_users, get_goal_stats, get_today_goals, delete_old_goals
import logging

logger = logging.getLogger(__name__)

scheduler = None


def start_scheduler(bot):
    """Инициализирует планировщик"""
    global scheduler

    if scheduler is None:
        scheduler = AsyncIOScheduler()

        # ⏰ УТРЕННЕЕ НАПОМИНАНИЕ В 05:00
        scheduler.add_job(
            send_morning_goals_reminder,
            'cron',
            hour=5,
            minute=0,
            args=[bot],
            id='morning_reminder'
        )

        # 🔔 НАПОМИНАНИЯ КАЖДЫЕ 2 ЧАСА (5:00, 7:00, 9:00, 11:00, 13:00, 15:00, 17:00, 19:00, 21:00)
        scheduler.add_job(
            send_goal_reminder,
            'cron',
            hour='5,7,9,11,13,15,17,19,21',
            minute=0,
            args=[bot],
            id='goal_reminder'
        )

        # 📋 ВЕЧЕРНИЙ ОТЧЕТ В 23:00
        scheduler.add_job(
            send_evening_report,
            'cron',
            hour=23,
            minute=0,
            args=[bot],
            id='evening_report'
        )

        scheduler.start()
        logger.info("✅ Планировщик запущен")
        logger.info("⏰ Расписание:")
        logger.info("  • 05:00 - Утреннее напоминание целей")
        logger.info("  • Каждые 2 часа - Напоминание о целях")
        logger.info("  • 23:00 - Вечерний отчет")

    return scheduler


async def send_morning_goals_reminder(bot):
    """Отправляет утреннее напоминание с целями на день"""
    try:
        users = get_all_users()

        for user_id in users:
            try:
                goals = get_today_goals(user_id)
                
                if goals:
                    text = "🌅 <b>ДОБРОЕ УТРО!</b>\n\n"
                    text += "🎯 <b>ВАШИ ЦЕЛИ НА СЕГОДНЯ:</b>\n\n"
                    
                    for i, (goal_id, goal_text, priority, status) in enumerate(goals, 1):
                        emoji_priority = "🔴" if priority == "high" else "🟡" if priority == "medium" else "🟢"
                        text += f"{i}. {emoji_priority} {goal_text}\n"
                    
                    text += "\n💪 Вы можете это сделать! Начните прямо сейчас!"
                    
                    await bot.send_message(user_id, text, parse_mode="HTML")
                else:
                    await bot.send_message(
                        user_id,
                        "🌅 Доброе утро!\n\n"
                        "🎯 У вас еще нет целей на сегодня.\n"
                        "Используйте /add_goal чтобы добавить цели!"
                    )
                    
            except Exception as e:
                logger.warning(f"Не удалось отправить утреннее напоминание пользователю {user_id}: {e}")
                
    except Exception as e:
        logger.error(f"Ошибка в send_morning_goals_reminder: {e}")


async def send_goal_reminder(bot):
    """Отправляет напоминание о целях каждые 2 часа"""
    try:
        users = get_all_users()
        current_time = datetime.now().strftime("%H:%M")

        for user_id in users:
            try:
                goals = get_today_goals(user_id)
                
                if goals:
                    incomplete_count = sum(1 for g in goals if g[3] != 'completed')
                    
                    if incomplete_count > 0:
                        text = f"⏰ <b>НАПОМИНАНИЕ {current_time}</b>\n\n"
                        text += f"📋 У вас осталось {incomplete_count} невыполненных целей на сегодня:\n\n"
                        
                        for goal_id, goal_text, priority, status in goals:
                            if status != 'completed':
                                emoji_priority = "🔴" if priority == "high" else "🟡" if priority == "medium" else "🟢"
                                text += f"  {emoji_priority} {goal_text}\n"
                        
                        text += "\n⚡ Не забывайте про свои цели!"
                        
                        await bot.send_message(user_id, text, parse_mode="HTML")
                        
            except Exception as e:
                logger.warning(f"Не удалось отправить напоминание пользователю {user_id}: {e}")
                
    except Exception as e:
        logger.error(f"Ошибка в send_goal_reminder: {e}")


async def send_evening_report(bot):
    """Отправляет вечерний отчет о выполнении целей"""
    try:
        users = get_all_users()

        for user_id in users:
            try:
                stats = get_goal_stats(user_id)
                
                text = "📊 <b>ВЕЧЕРНИЙ ОТЧЕТ</b>\n\n"
                text += f"📋 Целей на сегодня: {stats['total']}\n"
                text += f"✅ Выполнено: {stats['completed']}\n"
                text += f"⏳ Не выполнено: {stats['incomplete']}\n"
                text += f"📈 Процент выполнения: {stats['percentage']}%\n\n"
                
                if stats['percentage'] == 100:
                    text += "🎉 <b>СУПЕР! ВЫ ВЫПОЛНИЛИ ВСЕ ЦЕЛИ!</b>"
                elif stats['percentage'] >= 75:
                    text += "👏 <b>Отличный результат! Продолжайте в том же духе!</b>"
                elif stats['percentage'] >= 50:
                    text += "💪 <b>Хороший прогресс! Завтра у вас получится лучше!</b>"
                else:
                    text += "🔄 <b>Не расстраивайтесь! Завтра день новый. Вы справитесь!</b>"
                
                if stats['incomplete_list'] and stats['percentage'] < 100:
                    text += "\n\n❌ <b>Невыполненные цели на завтра:</b>\n"
                    for goal in stats['incomplete_list']:
                        text += f"  • {goal}\n"
                
                # Удаляем старые цели (старше 7 дней)
                delete_old_goals(user_id, days=7)
                
                await bot.send_message(user_id, text, parse_mode="HTML")
                
            except Exception as e:
                logger.warning(f"Не удалось отправить вечерний отчет пользователю {user_id}: {e}")
                
    except Exception as e:
        logger.error(f"Ошибка в send_evening_report: {e}")

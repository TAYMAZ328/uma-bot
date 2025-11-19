from apscheduler.schedulers.asyncio import AsyncIOScheduler
from bot.reminder import broadcast_res, remind_update
import asyncio


async def setup_scheduler():
    scheduler = AsyncIOScheduler()
    
    scheduler.add_job(
        broadcast_res,
        trigger='cron',
        day_of_week='thu',
        hour=22,
        minute=0,
        timezone='Asia/Tehran'
    )

    scheduler.add_job(
        remind_update,
        trigger='cron',
        day_of_week='sat',
        hour=13,
        minute=0,
        timezone='Asia/Tehran'
    )

    scheduler.start()

asyncio.get_event_loop().run_until_complete(setup_scheduler())
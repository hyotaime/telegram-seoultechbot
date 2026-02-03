import sys
import asyncio

sys.path.append('/telegram-seoultechbot')
import telegram as tel
from telegram.ext import CommandHandler, ApplicationBuilder, MessageHandler, filters
import os
from dotenv import load_dotenv
import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from src import database, log, schedule_notification
from src.commands import start, help, notice, food, weather, ping
from src.crawlers import food_crawler, notice_crawler
from src.departments import cse

# 토큰 읽기
load_dotenv()
BOT_TOKEN = os.environ.get('BOT_TOKEN')
NOTICE_CHANNEL_ID = os.environ.get('NOTICE_CHANNEL_ID')
WEATHER_API_TOKEN = os.environ.get('WEATHER_API_TOKEN')
CSE_CHANNEL_ID = os.environ.get('CSE_CHANNEL_ID')

bot = tel.Bot(token=BOT_TOKEN)


async def scheduler_hour(application):
    if datetime.datetime.now().hour == 0 and datetime.datetime.now().minute == 0:
        await schedule_notification.schedule_notification(application, NOTICE_CHANNEL_ID)
    if datetime.datetime.now().weekday() < 5 and datetime.datetime.now().hour == 7 and datetime.datetime.now().minute == 0:
        await schedule_notification.weather(application, NOTICE_CHANNEL_ID, WEATHER_API_TOKEN)
    if datetime.datetime.now().weekday() == 0 and datetime.datetime.now().hour == 9 and datetime.datetime.now().minute == 0:
        await schedule_notification.process_tepark_notification(application, NOTICE_CHANNEL_ID)
    await notice_crawler.process_notice_crawling(application, NOTICE_CHANNEL_ID)
    await cse.cse_notice_crawling(application, CSE_CHANNEL_ID)


if __name__ == '__main__':
    log.logger.addHandler(log.stream_handler)
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    database.db_test()
    scheduler = AsyncIOScheduler(event_loop=loop)
    scheduler.start()
    scheduler.add_job(scheduler_hour, 'cron', minute='*/10', args=(application,), id='scheduler_10min')
    # scheduler.add_job(scheduler_hour, 'cron', minute='*/1', args=(application,), id='scheduler_hour')
    a, b = 'notice', 'university'
    notice_crawler.get_notice(a, b)
    a, b = 'matters', 'affairs'
    notice_crawler.get_notice(a, b)
    a, b = 'janghak', 'scholarship'
    notice_crawler.get_notice(a, b)
    notice_crawler.get_domi_notice()
    food_crawler.set_tepark()

    start_handler = CommandHandler('start', start.start)
    application.add_handler(start_handler)

    help_handler = CommandHandler('help', help.help)
    application.add_handler(help_handler)

    tepark_handler = CommandHandler('tepark', food.tepark)
    application.add_handler(tepark_handler)

    weather_handler = CommandHandler('weather', weather.weather)
    application.add_handler(weather_handler)

    notice_handler = CommandHandler('notice', notice.notice)
    application.add_handler(notice_handler)

    ping_handler = CommandHandler('ping', ping.ping)
    application.add_handler(ping_handler)

    application.run_polling()

import sys

sys.path.append('/telegram-seoultechbot')
import telegram as tel
from telegram.ext import CommandHandler, ApplicationBuilder, CallbackQueryHandler
import os
from dotenv import load_dotenv
import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from commands import start, help, food, weather, dorm, ping, callback
from crawlers import foodcrawler, noticecrawler
from src import database, log, schedule_notification

# 토큰 읽기
load_dotenv()
BOT_TOKEN = os.environ.get('BOT_TOKEN')

bot = tel.Bot(token=BOT_TOKEN)


async def scheduler_hour(application):
    if datetime.datetime.now().hour == 0:
        await schedule_notification.schedule_notification(application)
    await foodcrawler.food_crawling()
    await food.process_food_notification(application)
    await noticecrawler.process_notice_crawling(application)


async def scheduler_notice(application):
    await noticecrawler.process_notice_crawling(application)


# 메인 함수
if __name__ == '__main__':
    log.logger.addHandler(log.stream_handler)
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    database.db_test()
    scheduler = AsyncIOScheduler()
    scheduler.start()
    scheduler.add_job(scheduler_hour, 'cron', minute=0, args=(application,), id='scheduler_hour')
    a, b = 'notice', 'university'
    noticecrawler.get_notice(a, b)
    a, b = 'matters', 'affairs'
    noticecrawler.get_notice(a, b)
    a, b = 'janghak', 'scholarship'
    noticecrawler.get_notice(a, b)
    noticecrawler.get_domi_notice()
    scheduler.add_job(scheduler_notice, 'cron', minute=30, args=(application,), id='scheduler_notice')

    start_handler = CommandHandler('start', start.start)
    application.add_handler(start_handler)

    help_handler = CommandHandler('help', help.help)
    application.add_handler(help_handler)

    food_handler = CommandHandler('food', food.food)
    application.add_handler(food_handler)

    cafe2_handler = CommandHandler('cafe2', food.cafe2)
    application.add_handler(cafe2_handler)

    tepark_handler = CommandHandler('tepark', food.tepark)
    application.add_handler(tepark_handler)

    weather_handler = CommandHandler('weather', weather.weather)
    application.add_handler(weather_handler)

    dorm_handler = CommandHandler('dorm', dorm.dorm)
    application.add_handler(dorm_handler)

    ping_handler = CommandHandler('ping', ping.ping)
    application.add_handler(ping_handler)

    callback_handler = CallbackQueryHandler(callback.callback)
    application.add_handler(callback_handler)

    application.run_polling()

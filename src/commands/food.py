import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from src import database
from src.crawlers import food_crawler

# 테크노파크
async def tepark(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    await process_tepark_notification(context, chat_id, datetime.datetime.now())

async def process_tepark_notification(context: ContextTypes.DEFAULT_TYPE, chat_id, today):
    food_crawler.set_tepark()
    food_data = database.get_tepark_menu(int(today.strftime('%y%W')))
    if food_data:
        await context.bot.send_photo(
            chat_id=chat_id,
            photo=food_data['img_link'],
            caption=food_data['title']
        )
    else:
        await context.bot.send_message(
            chat_id=chat_id,
            text="테크노파크 이번 주에 등록된 식단표가 없습니다."
        )

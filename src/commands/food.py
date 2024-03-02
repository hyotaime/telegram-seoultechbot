import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from src import database
from src.log import logger
from src.crawlers import foodcrawler


async def food(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    logger.info(f"ChatID: {chat_id} - food")
    button_off = InlineKeyboardButton(text="받지 않음", callback_data="food_off")
    button_9 = InlineKeyboardButton(text="9시", callback_data="food_09")
    button_10 = InlineKeyboardButton(text="10시", callback_data="food_10")
    button_11 = InlineKeyboardButton(text="11시", callback_data="food_11")
    button_12 = InlineKeyboardButton(text="12시", callback_data="food_12")
    await context.bot.send_message(
        chat_id=chat_id,
        text="학식 메뉴 알림을 설정해주세요.\n",
        reply_markup=InlineKeyboardMarkup([[button_9, button_10, button_11, button_12], [button_off]])
    )


async def food_callback(context: ContextTypes.DEFAULT_TYPE, chat_id, callback_data: str):
    if callback_data == "food_off":
        database.del_food_noti_time(chat_id)
        await context.bot.send_message(
            chat_id=chat_id,
            text="학식 메뉴 알림을 받지 않습니다."
        )
    else:
        callback_data = callback_data.split("_")[1]
        database.set_food_noti_time(chat_id, callback_data)
        await context.bot.send_message(
            chat_id=chat_id,
            text=f"학식 메뉴 알림이 {callback_data}시로 설정되었습니다."
        )


async def cafe2(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    logger.info(f"ChatID: {chat_id} - cafe2")
    button_today = InlineKeyboardButton(text="오늘", callback_data="cafe2_today")
    button_tomorrow = InlineKeyboardButton(text="내일", callback_data="cafe2_tomorrow")
    await context.bot.send_message(
        chat_id=chat_id,
        text="제2학생회관\n",
        reply_markup=InlineKeyboardMarkup([[button_today, button_tomorrow]])
    )
    day = datetime.datetime.now()
    await process_cafe2_notification(context, chat_id, day, '오늘')


async def cafe2_callback(context: ContextTypes.DEFAULT_TYPE, chat_id, callback_data: str):
    day = datetime.datetime.now()
    if callback_data == "cafe2_tomorrow":
        day += datetime.timedelta(days=1)
        try:
            database.get_cafe2_menu(int(day.strftime('%y%m%d')))
        except IndexError:
            foodcrawler.cafeteria_2(tomorrow=True)
        await process_cafe2_notification(context, chat_id, day, '내일')
    else:
        try:
            database.get_cafe2_menu(int(day.strftime('%y%m%d')))
        except IndexError:
            foodcrawler.cafeteria_2()
        await process_cafe2_notification(context, chat_id, day, '오늘')


async def process_cafe2_notification(context: ContextTypes.DEFAULT_TYPE, chat_id, day, day_str):
    food_data = database.get_cafe2_menu(int(day.strftime('%y%m%d')))
    if food_data:
        message = '{today.month}월 {today.day}일 식단\n'.format(today=day)
        message += (f"점심: {food_data['menu1_name']} `{food_data['menu1_price']}`\n"
                    f"{food_data['menu1_side']}\n")
        if food_data[3] != '간단 snack':
            message += (f"점심: {food_data['menu2_name']} `{food_data['menu2_price']}`\n"
                        f"{food_data['menu2_side']}\n")
        message += (f"저녁: {food_data['dinner_name']} `{food_data['dinner_price']}`\n"
                    f"{food_data['dinner_side']}\n")
        await context.bot.send_message(
            chat_id=chat_id,
            text=message
        )
    else:
        await context.bot.send_message(
            chat_id=chat_id,
            text=f"제2학생회관 {day_str} 등록된 식단이 없습니다."
        )


# 테크노파크
async def tepark(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    await process_tepark_notification(context, chat_id, datetime.datetime.now())


async def process_tepark_notification(context: ContextTypes.DEFAULT_TYPE, chat_id, today):
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


async def process_food_notification(context: ContextTypes.DEFAULT_TYPE):
    time_now = datetime.datetime.now().strftime('%H')
    chat_ids = database.get_food_noti_id(time_now)
    for chat_id in chat_ids:
        await process_cafe2_notification(context, chat_id['id'], datetime.datetime.now(), '오늘')
        await process_tepark_notification(context, chat_id['id'], datetime.datetime.now())

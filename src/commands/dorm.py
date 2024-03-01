from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from src import database
from src.log import logger


async def dorm(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    logger.info(f"ChatID: {chat_id} - dorm")
    button_off = InlineKeyboardButton(text="받지 않음", callback_data="dorm_off")
    button_on = InlineKeyboardButton(text="받음", callback_data="dorm_on")
    await context.bot.send_message(
        chat_id=chat_id,
        text="생활관 알림을 설정해주세요.\n",
        reply_markup=InlineKeyboardMarkup([[button_off, button_on]])
    )


async def dorm_callback(context: ContextTypes.DEFAULT_TYPE, chat_id, callback_data: str):
    if callback_data == "dorm_off":
        database.del_dorm_noti(chat_id)
        await context.bot.send_message(
            chat_id=chat_id,
            text="생활관 알림을 받지 않습니다."
        )
    else:
        database.set_dorm_noti(chat_id)
        await context.bot.send_message(
            chat_id=chat_id,
            text=f"생활관 알림이 설정되었습니다."
        )

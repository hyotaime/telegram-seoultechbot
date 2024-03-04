from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from src import database
from src.log import logger


async def notice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    logger.info(f"ChatID: {chat_id} - notice")
    button_off = InlineKeyboardButton(text="받지 않음", callback_data="notice_off")
    button_on = InlineKeyboardButton(text="받음", callback_data="notice_on")
    await context.bot.send_message(
        chat_id=chat_id,
        text="공지사항 알림을 설정해주세요.\n",
        reply_markup=InlineKeyboardMarkup([[button_off, button_on]])
    )


async def notice_callback(context: ContextTypes.DEFAULT_TYPE, chat_id, callback_data: str):
    if callback_data == "notice_off":
        database.del_user_notice(chat_id)
        await context.bot.send_message(
            chat_id=chat_id,
            text="공지사항 알림을 받지 않습니다."
        )
    else:
        database.set_user_notice(chat_id)
        await context.bot.send_message(
            chat_id=chat_id,
            text=f"공지사항 알림이 설정되었습니다."
        )

from telegram import Update
from telegram.ext import ContextTypes
import datetime
from src.log import logger


async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    logger.info(f"ChatID: {chat_id} - ping")
    start = datetime.datetime.now().microsecond
    await context.bot.send_message(
        chat_id=chat_id,
        text=f'pong!\n'
             f'지연시간: {round(datetime.datetime.now().microsecond - start)} ms'
    )

from telegram import Update
from telegram.ext import ContextTypes
from src.log import logger


async def notice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    logger.info(f"ChatID: {chat_id} - notice")
    await context.bot.send_message(
        chat_id=chat_id,
        text="Now sending notification to individual accounts is deprecated.\n"
             "Please use the @seoultech_notice to get notification.",
    )

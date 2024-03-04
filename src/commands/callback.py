from telegram import Update
from telegram.ext import ContextTypes
from src.log import logger
from src.commands import food, dorm, notice


async def callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    callback_data = update.callback_query.data
    logger.info(f"{chat_id} - callback - {callback_data}")
    match callback_data.split("_")[0]:
        case "food":
            await food.food_callback(context, chat_id, callback_data)
        case "cafe2":
            await food.cafe2_callback(context, chat_id, callback_data)
        case "dorm":
            await dorm.dorm_callback(context, chat_id, callback_data)
        case "notice":
            await notice.notice_callback(context, chat_id, callback_data)

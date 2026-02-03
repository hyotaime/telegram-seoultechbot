from telegram import Update
from telegram.ext import ContextTypes
from src.log import logger
from src import database


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    logger.info(f"ChatID: {chat_id} - start")
    database.start_chat(chat_id)
    await context.bot.send_message(
        chat_id=chat_id,
        text="👋 안녕하세요!\n"
             "서울과학기술대학교 비공식 봇, 테크봇을 이용해주셔서 감사합니다.\n"
             "/help 명령어로 명령어의 목록을 확인하실 수 있습니다.\n"
    )
    await context.bot.send_message(
        chat_id=chat_id,
        text="⚠️주의사항⚠️\n"
             "`/notice` 명령어를 사용해야 학교 공지사항과 학사일정 알림을 받을 수 있습니다.\n"
             "학교 공지사항은 학교 홈페이지의 대학공지사항, 학사공지, 장학공지를 알려드립니다.\n"
             "이외의 공지사항은 학교 홈페이지를 참고하시기 바랍니다.\n"
    )

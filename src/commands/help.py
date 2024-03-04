from telegram import Update
from telegram.ext import ContextTypes
from src.log import logger


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    logger.info(f"ChatID: {chat_id} - help")
    await context.bot.send_message(
        chat_id=chat_id,
        text="명령어 목록\n"
             "/help - 테크봇의 명령어 목록과 설명을 보여줍니다.\n"
             "/cafe2 - 제2학생회관의 식단표를 보여줍니다.\n"
             "/tepark - 테크노파크의 이번 주 식단표를 보여줍니다.\n"
             "/weather - 현재 캠퍼스의 날씨와 1 ~ 6시간 뒤 날씨 예보를 보여줍니다.\n"
             "/notice - 학교 공지사항과 학사일정 알림을 설정합니다.\n"
             "/food - 학식 메뉴 알림을 설정합니다.\n"
             "/dorm - 생활관 알림을 설정합니다.\n"
             "/ping - 명령어 입력 시점부터 메세지 전송까지 총 지연시간을 보여줍니다.\n"
    )

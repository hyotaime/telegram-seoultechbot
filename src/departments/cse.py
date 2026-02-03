import requests
from telegram.ext import ContextTypes
from src.log import logger
from src.crawlers import notice_crawler

async def cse_notice_crawling(context: ContextTypes.DEFAULT_TYPE, CSE_CHANNEL_ID):
    logger.info('Trying to crawl CSE notice...')
    try:
        new_com_notice = notice_crawler.get_cse_notice()
    except requests.ConnectTimeout:
        logger.error("ERROR: Connection timed out")
        return

    com_notice_msg = "새 컴퓨터공학과 공지사항\n"

    for row in new_com_notice:
        com_notice_msg += (f'{row[1]}\n'
                           f'[{row[0]}]({row[2]})\n')

    logger.info(f'Sending new notification')
    if len(new_com_notice) > 0:
        try:
            if len(new_com_notice) > 0:
                await context.bot.send_message(
                    chat_id=CSE_CHANNEL_ID,
                    text=com_notice_msg,
                    parse_mode='MarkdownV2'
                )
        except Exception as e:
            logger.error(f'Cannot send CSE notification to {CSE_CHANNEL_ID}. Error: {e}')

import datetime
from src import database
from src.log import logger
from src.crawlers import noticecrawler


async def schedule_notification(application):
    logger.info('schedule_notification')
    now = datetime.datetime.now()
    schedule = noticecrawler.get_univ_schedule()
    msg = (f'오늘의 일정\n'
           f'오늘 시작하거나 끝나는 학사일정입니다.\n')
    chat_ids = database.get_all_users()
    if len(schedule) > 0:
        for row in schedule:
            if '\n\n' in row:
                task = row.split('\n\n')[0]
                date = row.split('\n\n')[1]
                msg += (f'{task}\n'
                        f'{date}\n')
            else:
                task = row.split('\n\n')[0]
                date = now.strftime('%Y.%m.%d')
                msg += (f'{task}\n'
                        f'{date}\n')

        if len(chat_ids) > 0:
            print(f'{now}: 알림 설정한 서버들을 대상으로 오늘의 학사일정 알림을 전송합니다.')
            for chat_id in chat_ids:
                chat_id = chat_id['id']
                try:
                    await application.context.bot.send_message(
                        chat_id=chat_id,
                        text=msg
                    )
                except Exception as e:
                    logger.info(f'{chat_id} 채널에 알림을 보낼 수 없습니다. 예외명: {e}')
                    continue

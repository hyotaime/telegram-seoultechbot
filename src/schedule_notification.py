import datetime
from telegram.ext import ContextTypes
from src import database
from src.log import logger
from src.crawlers import notice_crawler, weather_crawler, food_crawler


async def schedule_notification(context: ContextTypes.DEFAULT_TYPE, NOTICE_CHANNEL_ID):
    logger.info('schedule_notification')
    now = datetime.datetime.now()
    schedule = notice_crawler.get_univ_schedule()
    msg = (f'오늘의 일정\n'
           f'오늘 시작하거나 끝나는 학사일정입니다.\n')
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

        print(f'{now}: Sending today\' schedule notification')
        try:
            await context.bot.send_message(
                chat_id=NOTICE_CHANNEL_ID,
                text=msg
            )
        except Exception as e:
            logger.info(f'{NOTICE_CHANNEL_ID} 채널에 알림을 보낼 수 없습니다. 예외명: {e}')

async def process_tepark_notification(context: ContextTypes.DEFAULT_TYPE, NOTICE_CHANNEL_ID):
    logger.info('process_tepark_notification')
    food_crawler.set_tepark()
    food_data = database.get_tepark_menu(int(datetime.datetime.now().strftime('%y%W')))
    if food_data:
        await context.bot.send_photo(
            chat_id=NOTICE_CHANNEL_ID,
            photo=food_data['img_link'],
            caption=food_data['title']
        )
    else:
        await context.bot.send_message(
            chat_id=NOTICE_CHANNEL_ID,
            text="테크노파크 이번 주에 등록된 식단표가 없습니다."
        )

async def weather(context: ContextTypes.DEFAULT_TYPE, NOTICE_CHANNEL_ID, WEATHER_API_TOKEN):
    logger.info(f"ChatID: {NOTICE_CHANNEL_ID} - weather")
    try:
        today, weather_datas = weather_crawler.get_weather(WEATHER_API_TOKEN)
        message = "이 시간 캠퍼스 날씨\n"
        now_weather = weather_datas[0]
        if now_weather[3] == '0':
            message += (f"{today.month}월 {today.day}일 {today.hour}시 {today.minute}분 공릉동의 날씨입니다.\n"
                        f"{now_weather[1]}{now_weather[2]}\n"
                        f"🌡기온: {now_weather[0]}°C\n"
                        f"💧습도: {now_weather[5]}%\n"
                        f"💨바람: {now_weather[7]}방향으로 {now_weather[8]}m/s\n"
                        f"날씨예보\n")
        else:
            message += (f"{today.month}월 {today.day}일 {today.hour}시 {today.minute}분 날씨입니다.\n"
                        f"{now_weather[3].split()[0]}{now_weather[3].split()[1]}\n"
                        f"🌧강수량: {now_weather[4]}\n"
                        f"🌡기온: {now_weather[0]}°C\n"
                        f"💧습도: {now_weather[5]}%\n"
                        f"💨바람: {now_weather[7]}방향으로 {now_weather[8]}m/s\n"
                        f"날씨예보\n")
        for weather_data in weather_datas[1:]:
            if weather_data[3][0] == '0':
                message += f"{weather_data[9]}시: {weather_data[1]}{weather_data[0]}°C, 💧{weather_data[5]}%\n"
            else:
                message += f"{weather_data[9]}시: {weather_data[3].split()[0]}{weather_data[0]}°C, 💧{weather_data[5]}%\n"
        message += "기상청 초단기예보 조회 서비스 오픈 API를 이용한 것으로, 실제 기상상황과 차이가 있을 수 있습니다."

        await context.bot.send_message(
            chat_id=NOTICE_CHANNEL_ID,
            text=message
        )
    except Exception:
        await context.bot.send_message(
            chat_id=NOTICE_CHANNEL_ID,
            text="날씨를 불러오는 중 문제가 발생했습니다."
        )

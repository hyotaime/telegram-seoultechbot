from telegram import Update
from telegram.ext import ContextTypes
from src.log import logger
import datetime
import requests
import os
from dotenv import load_dotenv


async def weather(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    logger.info(f"ChatID: {chat_id} - weather")
    try:
        today, weather_datas = get_weather()
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
            chat_id=chat_id,
            text=message
        )
    except Exception:
        await context.bot.send_message(
            chat_id=chat_id,
            text="날씨를 불러오는 중 문제가 발생했습니다."
        )


def get_weather():
    load_dotenv()
    token = os.environ.get('WEATHER_API_TOKEN')

    today = datetime.datetime.now()
    url = 'http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtFcst'
    direction = ['북', '북북동', '북동', '동북동', '동', '동남동', '남동', '남남동', '남',
                 '남남서', '남서', '서남서', '서', '서북서', '북서', '북북서', '북']

    basetime = today
    if int(basetime.strftime('%H%M')[2:4]) < 45:
        basetime = today - datetime.timedelta(hours=1)

    params = {'serviceKey': token, 'dataType': 'JSON', 'numOfRows': '1000', 'base_date': basetime.strftime('%Y%m%d'),
              'base_time': basetime.strftime('%H') + '30', 'nx': '61', 'ny': '128'}

    response = requests.get(url, params=params, timeout=20)
    items = response.json().get('response').get('body').get('items')

    data = [[], [], [], [], [], []]

    for i, item in enumerate(items['item']):
        if i < 6:
            # Kor. to Eng.
            data[i] = ['temperature', 'status_num', 'status', 'rain_type', 'precipitation', 'humidity', 'wind_vane',
                       'wind_direction', 'wind_speed', 'time']
            if int(item['fcstTime'][0:2]) < 10:
                data[i % 6][9] = item['fcstTime'][1]
            else:
                data[i % 6][9] = item['fcstTime'][0:2]

        # 강수 형태 (PTY)
        # Add few more options
        elif 6 <= i < 12:
            if item['fcstValue'] == '0':
                data[i % 6][3] = item['fcstValue']
            elif item['fcstValue'] == '1':
                data[i % 6][3] = '☔️ 비'
            elif item['fcstValue'] == '2':
                data[i % 6][3] = '🌧 비/눈'
            elif item['fcstValue'] == '3':
                data[i % 6][3] = '❄️ 눈'
            elif item['fcstValue'] == '5':
                data[i % 6][3] = '💦 빗방울'
            elif item['fcstValue'] == '6':
                data[i % 6][3] = '💦 빗방울눈날림'
            elif item['fcstValue'] == '7':
                data[i % 6][3] = '❄️ 눈날림'
            else:
                data[i % 6][3] = '⚠️ API 에러'

        # 강수량 (RN1)
        elif 12 <= i < 18:
            data[i % 6][4] = item['fcstValue']

        # 하늘 상태 (SKY)
        # Add few more options
        elif 18 <= i < 24:
            if item['fcstValue'] == '1':
                data[i % 6][1] = '☀️'
                data[i % 6][2] = '맑음'
            elif item['fcstValue'] == '3':
                data[i % 6][1] = '🌥'
                data[i % 6][2] = '구름많음'
            elif item['fcstValue'] == '4':
                data[i % 6][1] = '☁️'
                data[i % 6][2] = '흐림'
            else:
                data[i % 6][1] = '⚠️'
                data[i % 6][2] = 'API 에러'

        # 기온 (TH1)
        elif 24 <= i < 30:
            data[i % 6][0] = item['fcstValue']

        # 습도 (REH)
        elif 30 <= i < 36:
            data[i % 6][5] = item['fcstValue']

        # 풍향 (VEC)
        elif 48 <= i < 54:
            data[i % 6][6] = item['fcstValue']
            direction_num = int((int(item['fcstValue']) + 22.5 * 0.5) / 22.5)
            data[i % 6][7] = direction[direction_num]

        # 풍속 (WSD)
        elif 54 <= i < 60:
            data[i % 6][8] = item['fcstValue']
    return today, data

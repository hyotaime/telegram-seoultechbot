import datetime
import requests
from src import database
from bs4 import BeautifulSoup
from src.log import logger


async def food_crawling():
    today = datetime.datetime.now()
    if today.weekday() < 5:
        if not database.get_cafe2_menu(int(today.strftime('%y%m%d'))):
            print(f'{today}: 제2학생회관 식단 크롤링 시도...')
            cafeteria_2()
        if not database.get_tepark_menu(int(today.strftime('%y%W'))):
            print(f'{today}: 서울테크노파크 식단 크롤링 시도...')
            tepark()


def cafeteria_2(tomorrow=False):
    basedate = datetime.date.today()
    if tomorrow:
        basedate += datetime.timedelta(days=1)
    try:
        response = requests.get(headers={'User-Agent': 'Mozilla/5.0'},
                                url=f"https://www.seoultech.ac.kr/life/student/food2/?location_code=20&food_date={basedate.strftime('%Y-%m-%d')}")
        parser = BeautifulSoup(response.text, "html.parser")
        rows = parser.select('.dts_design > div:nth-child(5) > div:nth-child(2) > table:nth-child(1) > tr')
        menu1 = [rows[1].select('td:nth-child(1)')[0].text.strip(),
                 rows[1].select('td:nth-child(2)')[0].text.strip(),
                 rows[1].select('td:nth-child(3)')[0].text.strip().replace('\t', '').replace('\r', '')]
        menu2 = [rows[2].select('td:nth-child(1)')[0].text.strip(),
                 rows[2].select('td:nth-child(2)')[0].text.strip(),
                 rows[2].select('td:nth-child(3)')[0].text.strip().replace('\t', '').replace('\r', '')]
        rows = parser.select('.dts_design > div:nth-child(5) > div:nth-child(4) > table:nth-child(1) > tr')
        dinner_menu = [rows[1].select('td:nth-child(1)')[0].text.strip(),
                       rows[1].select('td:nth-child(2)')[0].text.strip(),
                       rows[1].select('td:nth-child(3)')[0].text.strip().replace('\t', '').replace('\r', '')]

        database.set_cafe2_menu(int(basedate.strftime('%y%m%d')), menu1[0], menu1[1], menu1[2], menu2[0], menu2[1],
                                menu2[2], dinner_menu[0], dinner_menu[1], dinner_menu[2])
    except IndexError:
        if tomorrow:
            logger.error('크롤링 실패. (내일의 식단 등록 안 됨)')
        else:
            logger.error('크롤링 실패. 다음 주기에 다시 시도합니다. (오늘의 식단 등록 안 됨)')
    except requests.ConnectTimeout:
        logger.error('크롤링 실패. 다음 주기에 다시 시도합니다. (학교 홈페이지 응답 없음)')


def tepark():
    try:
        response = requests.get('https://www.seoultp.or.kr/user/nd70791.do')
        parser = BeautifulSoup(response.text, "html.parser")
        bnum = str(
            parser.select('.board-list > tbody:nth-child(4) > tr:nth-child(1) > td:nth-child(2) > a:nth-child(1)')[
                0]).split("'")[5]
        title = parser.select('.board-list > tbody:nth-child(4) > tr:nth-child(1) > td:nth-child(2) > a:nth-child(1)')[
            0].text.strip()
        uploaded_date = parser.select('.board-list > tbody:nth-child(4) > tr:nth-child(1) > td:nth-child(4)')[
            0].text.strip().replace('.', '')
        response = requests.get('https://www.seoultp.or.kr/user/nd70791.do?View&boardNo=' + bnum)
        parser = BeautifulSoup(response.text, "html.parser")
        board_area = parser.select('.board-write > tbody:nth-child(3) > tr:nth-child(4)')[0]
        picture_link = 'https://www.seoultp.or.kr' + board_area.find_all(name='img')[0].get('src')

        database.set_tepark_menu(int(datetime.date.today().strftime('%y%W')), title, int(uploaded_date), picture_link)
    except requests.ConnectTimeout:
        logger.error('크롤링 실패. 다음 주기에 다시 시도합니다. (테크노파크 홈페이지 응답 없음)')

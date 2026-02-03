import datetime
import requests
from src import database
from bs4 import BeautifulSoup
from src.log import logger


def set_tepark():
    today = datetime.datetime.now()
    if today.weekday() < 5:
        if database.get_tepark_menu(int(today.strftime('%y%W'))):
            return
        print(f'{today}: 서울테크노파크 식단 크롤링 시도...')
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

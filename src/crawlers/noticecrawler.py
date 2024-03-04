import requests
import datetime
import pymysql
from functools import wraps
import os
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from telegram.ext import ContextTypes
from src import database
from src.log import logger


def db_connection(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        load_dotenv()
        DB_HOST = os.environ.get('DB_HOST')
        DB_USERNAME = os.environ.get('DB_USERNAME')
        DB_PASSWORD = os.environ.get('DB_PASSWORD')
        DB_PORT = os.environ.get('DB_PORT')
        DB_NAME = os.environ.get('DB_NAME')
        try:
            with pymysql.connect(host=DB_HOST, user=DB_USERNAME, password=DB_PASSWORD, port=int(DB_PORT),
                                 db=DB_NAME, charset="utf8", cursorclass=pymysql.cursors.DictCursor) as conn:
                with conn.cursor() as cur:
                    return func(cur, *args, **kwargs)
        except Exception as e:
            logger.error(e)
            return None

    return wrapper


@db_connection
def get_notice(cur, board_name, table_name):
    response = requests.get(headers={'User-Agent': 'Mozilla/5.0'},
                            url='https://www.seoultech.ac.kr/service/info/' + board_name + '/')
    parser = BeautifulSoup(response.text, "html.parser")
    rows = parser.select('.tbl_list > tbody:nth-child(4) > tr')
    new_notice = []
    for row in rows:
        try:
            title = (row.select('td:nth-child(2) > a')[0].text.strip()
                     .replace("[", "\\[").replace("]", "\\]").replace("`", "\\`")
                     .replace("(", '\\(').replace(")", "\\)").replace("-", "\\-")
                     .replace("~", "\\~").replace(".", "\\.").replace("!", "\\!")
                     .replace(">", "\\>").replace("#", "\\#").replace("+", "\\+")
                     .replace("=", "\\=").replace("|", "\\|").replace("{", "\\{")
                     .replace("}", "\\}").replace("_", "\\_").replace("*", "\\*")
                     )
            author = row.select('td:nth-child(4)')[0].text.strip()
            url = row.select('td:nth-child(2) > a')[0].get('href')
            bidx = int(url.split('&')[5].strip('bidx='))
            try:
                sql = f'''
                INSERT INTO {table_name}
                VALUES(%s)
                '''
                cur.execute(sql, (bidx,))
                new_notice.append([title, author, 'https://www.seoultech.ac.kr/service/info/' + board_name + url])
            except pymysql.IntegrityError:
                continue
        except IndexError:
            continue
    sql = f'''
        SELECT COUNT(board_index)
        FROM {table_name}
    '''
    cur.execute(sql)
    count = cur.fetchall()[0]['COUNT(board_index)']
    while count > 2000:
        sql = f'''
            DELETE FROM {table_name}
            WHERE board_index = (SELECT min(board_index) FROM {table_name})
        '''
        cur.execute(sql)
        count -= 1
    cur.connection.commit()
    return new_notice


@db_connection
def get_domi_notice(cur):
    response = requests.get('https://domi.seoultech.ac.kr/do/notice/')
    parser = BeautifulSoup(response.text, "html.parser")
    rows = parser.select('.list_3 > li')
    new_notice = []
    for row in rows:
        title = (row.select('a:nth-child(1)')[0].text.strip()
                 .replace("[", "\\[").replace("]", "\\]").replace("`", "\\`")
                 .replace("(", '\\(').replace(")", "\\)").replace("-", "\\-")
                 .replace("~", "\\~").replace(".", "\\.").replace("!", "\\!")
                 .replace(">", "\\>").replace("#", "\\#").replace("+", "\\+")
                 .replace("=", "\\=").replace("|", "\\|").replace("{", "\\{")
                 .replace("}", "\\}").replace("_", "\\_").replace("*", "\\*")
                 )
        url = row.select('a:nth-child(1)')[0].get('href')
        bidx = int(url.split('&')[2].strip('bidx='))
        try:
            sql = '''
                INSERT INTO dormitory
                VALUES(%s)
            '''
            cur.execute(sql, (bidx,))
            response = requests.get('https://domi.seoultech.ac.kr/do/notice/' + url)
            parser = BeautifulSoup(response.text, "html.parser")
            try:
                author = parser.select('.date > span:nth-child(2) > font:nth-child(1)')[0].text
            except IndexError:
                author = parser.select('.date > span:nth-child(3) > font:nth-child(1)')[0].text
            new_notice.append([title, author, 'https://domi.seoultech.ac.kr/do/notice/' + url])
        except pymysql.IntegrityError:
            continue
    sql = '''
        SELECT COUNT(board_index)
        FROM dormitory
    '''
    cur.execute(sql)
    count = cur.fetchall()[0]['COUNT(board_index)']
    while count > 1000:
        sql = '''
            DELETE FROM dormitory
            WHERE board_index = (SELECT min(board_index) FROM dormitory)
        '''
        cur.execute(sql)
        count -= 1
    cur.connection.commit()
    return new_notice


def get_univ_schedule():
    logger.info('get univ schedule')
    response = requests.get(
        'https://eclass.seoultech.ac.kr/ilos/main/main_schedule_view.acl?viewDt=' + datetime.date.today().strftime(
            '%Y%m%d'))
    parser = BeautifulSoup(response.text, "html.parser")
    rows = parser.find_all(class_='changeDetile schedule-Detail-Box')
    schedule = []
    for row in rows:
        schedule.append(row.text.strip())
    return schedule


async def process_notice_crawling(context: ContextTypes.DEFAULT_TYPE):
    logger.info('공지사항 크롤링 시도...')
    try:
        a, b = 'notice', 'university'
        new_univ_notice = get_notice(a, b)
        a, b = 'matters', 'affairs'
        new_affairs_notice = get_notice(a, b)
        a, b = 'janghak', 'scholarship'
        new_scholarship_notice = get_notice(a, b)
        new_dormitory_notice = get_domi_notice()
    except requests.ConnectTimeout:
        new_univ_notice = []
        new_affairs_notice = []
        new_scholarship_notice = []
        new_dormitory_notice = []
        logger.error('학교 홈페이지 연결 실패. 다음 주기에 다시 시도합니다.')

    univ_notice_msg = "새 대학공지사항\n"
    scholarship_msg = "새 장학공지\n"
    affairs_msg = "새 학사공지\n"

    for row in new_univ_notice:
        univ_notice_msg += (f'{row[1]}\n'
                            f'[{row[0]}]({row[2]})\n')
    for row in new_affairs_notice:
        affairs_msg += (f'{row[1]}\n'
                        f'[{row[0]}]({row[2]})\n')
    for row in new_scholarship_notice:
        scholarship_msg += (f'{row[1]}\n'
                            f'[{row[0]}]({row[2]})\n')

    chat_ids = database.get_all_users()
    if len(new_univ_notice) > 0 or len(new_affairs_notice) > 0 or len(new_scholarship_notice) > 0:
        logger.info('알림 설정한 서버들을 대상으로 새 공지사항 알림을 전송합니다.')
        for chat_id in chat_ids:
            chat_id = chat_id['id']
            try:
                if len(new_univ_notice) > 0:
                    await context.bot.send_message(
                        chat_id=chat_id,
                        text=univ_notice_msg,
                        parse_mode='MarkdownV2'
                    )
                if len(new_affairs_notice) > 0:
                    await context.bot.send_message(
                        chat_id=chat_id,
                        text=affairs_msg,
                        parse_mode='MarkdownV2'
                    )
                if len(new_scholarship_notice) > 0:
                    await context.bot.send_message(
                        chat_id=chat_id,
                        text=scholarship_msg,
                        parse_mode='MarkdownV2'
                    )
            except Exception as e:
                logger.error(f'{chat_id} 채널에 알림을 보낼 수 없습니다. 예외명: {e}')
                continue

    if len(new_dormitory_notice) > 0:
        msg = "새 생활관공지\n"
        chat_ids_domi = database.get_user_dorm_noti()
        for row in new_dormitory_notice:
            msg += (f'{row[1]}\n'
                    f'[{row[0]}]({row[2]})\n')

        logger.info('알림 설정한 서버들을 대상으로 새 생활관공지 알림을 전송합니다.')
        for chat_id_domi in chat_ids_domi:
            chat_id_domi = chat_id_domi['id']
            try:
                await context.bot.send_message(
                    chat_id=chat_id_domi,
                    text=msg,
                    parse_mode='MarkdownV2'
                )
            except Exception as e:
                logger.error(f'{chat_id_domi} 채널에 알림을 보낼 수 없습니다. 예외명: {e}')
                continue

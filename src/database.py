import pymysql
from functools import wraps
from log import logger
from dotenv import load_dotenv
import os


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
def db_test(cur):
    logger.info(f"DB connection test")
    sql = '''
        SELECT * 
        FROM user
        '''
    cur.execute(sql)
    logger.info("DB connection success")


@db_connection
def start_chat(cur, chat_id):
    logger.info("start chat")
    sql = '''
        SELECT id
        FROM user
        WHERE id=%s
        '''
    cur.execute(sql, chat_id)
    results = cur.fetchall()
    if len(results) == 0:
        sql = '''
            INSERT INTO user(id)
            VALUES (%s)
            '''
        cur.execute(sql, chat_id)
        cur.connection.commit()
        logger.info(f"{chat_id} INSERT success")
    else:
        logger.info(f"{chat_id} Already exist")


@db_connection
def get_all_users(cur):
    logger.info("get all users")
    sql = '''
        SELECT id
        FROM user
    '''
    cur.execute(sql)
    return cur.fetchall()

@db_connection
def get_user_notice(cur):
    logger.info("get user notice")
    sql = '''
        SELECT id
        FROM notice
    '''
    cur.execute(sql)
    return cur.fetchall()


@db_connection
def set_user_notice(cur, chat_id):
    logger.info("set user notice")
    try:
        sql = '''
            INSERT INTO notice
            VALUES(%s)
        '''
        cur.execute(sql, chat_id)
        logger.info(f"{chat_id} INSERT success")
    except pymysql.IntegrityError:
        logger.info(f"{chat_id} Already exist")
    cur.connection.commit()
    logger.info("commit success")


@db_connection
def del_user_notice(cur, chat_id):
    logger.info("del user notice")
    sql = '''
        DELETE FROM notice
        WHERE id=%s
    '''
    cur.execute(sql, chat_id)
    cur.connection.commit()
    logger.info("commit success")


@db_connection
def get_user_dorm_noti(cur):
    logger.info("get user dorm noti")
    sql = '''
        SELECT id
        FROM dorm
    '''
    cur.execute(sql)
    return cur.fetchall()


@db_connection
def set_dorm_noti(cur, chat_id):
    logger.info("set dorm noti")
    try:
        sql = '''
            INSERT INTO dorm
            VALUES(%s)
        '''
        cur.execute(sql, chat_id)
        logger.info(f"{chat_id} INSERT success")
    except pymysql.IntegrityError:
        logger.info(f"{chat_id} Already exist")
    cur.connection.commit()
    logger.info("commit success")


@db_connection
def del_dorm_noti(cur, chat_id):
    logger.info("del dorm noti")
    sql = '''
        DELETE FROM dorm
        WHERE id=%s
    '''
    cur.execute(sql, chat_id)
    cur.connection.commit()
    logger.info("commit success")


@db_connection
def set_food_noti_time(cur, chat_id, noti_time):
    try:
        sql = '''
            INSERT INTO food
            VALUES(%s, %s)
        '''
        cur.execute(sql, (chat_id, noti_time))
        logger.info(f"{chat_id} INSERT success")
    except pymysql.IntegrityError:
        sql = '''
            UPDATE food
            SET noti_time=%s
            WHERE id=%s
        '''
        cur.execute(sql, (noti_time, chat_id))
        logger.info(f"{chat_id} UPDATE success")
    cur.connection.commit()
    logger.info("commit success")


@db_connection
def get_food_noti_id(cur, noti_time):
    sql = '''
        SELECT id
        FROM food
        WHERE noti_time=%s
    '''
    cur.execute(sql, noti_time)
    return cur.fetchall()


@db_connection
def del_food_noti_time(cur, chat_id):
    sql = '''
        DELETE FROM food
        WHERE id=%s
    '''
    cur.execute(sql, chat_id)
    cur.connection.commit()
    logger.info("commit success")


@db_connection
def set_cafe2_menu(cur, basedate, menu1_name, menu1_price, menu1_side, menu2_name, menu2_price, menu2_side, dinner_name,
                   dinner_price, dinner_side):
    try:
        sql = '''
            INSERT INTO cafeteria_2
            VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        '''
        cur.execute(sql, (
            basedate, menu1_name, menu1_price, menu1_side, menu2_name, menu2_price, menu2_side, dinner_name,
            dinner_price,
            dinner_side))
    except pymysql.IntegrityError:
        sql = '''
            UPDATE cafeteria_2
            SET menu1_name=%s, menu1_price=%s, menu1_side=%s, menu2_name=%s, menu2_price=%s, menu2_side=%s, dinner_name=%s, dinner_price=%s, dinner_side=%s
            WHERE year_month_date=%s
        '''
        cur.execute(sql, (
            menu1_name, menu1_price, menu1_side, menu2_name, menu2_price, menu2_side, dinner_name, dinner_price,
            dinner_side, basedate,))
    sql = '''
        SELECT COUNT(year_month_date)
        FROM cafeteria_2
    '''
    cur.execute(sql)
    count = cur.fetchall()[0]['COUNT(year_month_date)']
    while count > 5:
        sql = '''
            DELETE FROM cafeteria_2
            WHERE year_month_date = (SELECT min(year_month_date) FROM cafeteria_2)
        '''
        cur.execute(sql)
        count -= 1

    cur.connection.commit()
    logger.info("commit success")


@db_connection
def get_cafe2_menu(cur, date):
    logger.info("get cafe2 menu")
    try:
        sql = '''
            SELECT menu1_name, menu1_price, menu1_side, menu2_name, menu2_price, menu2_side, dinner_name, dinner_price, dinner_side
            FROM cafeteria_2
            WHERE year_month_date=%s
        '''
        cur.execute(sql, date)
        return cur.fetchall()[0]
    except IndexError:
        logger.error('제2학생회관 인덱스 에러')
        return None


@db_connection
def set_tepark_menu(cur, today, title, uploaded_date, picture_link):
    logger.info("set tepark menu")
    try:
        sql = '''
        INSERT INTO tepark 
        VALUES(%s, %s, %s, %s)
        '''
        cur.execute(sql, (today, title, uploaded_date, picture_link))
        logger.info("서울테크노파크 식단 INSERT 성공!")
    except pymysql.IntegrityError:
        logger.error("크롤링 실패. 다음 주기에 다시 시도합니다. (지난주 게시글 크롤링 시도)")
    sql = '''
        SELECT COUNT(year_week)
        FROM tepark
    '''
    cur.execute(sql)
    count = cur.fetchall()[0]['COUNT(year_week)']
    while count > 4:
        sql = '''
            DELETE FROM tepark 
            WHERE year_week = (SELECT min(year_week) FROM tepark)
        '''
        cur.execute(sql)
        count -= 1
    cur.connection.commit()
    logger.info("commit success")


@db_connection
def get_tepark_menu(cur, week):
    try:
        sql = '''
            SELECT title, img_link
            FROM tepark
            WHERE year_week=%s
        '''
        cur.execute(sql, week)
        return cur.fetchall()[0]
    except IndexError:
        logger.error('테크노파크 인덱스 에러')
        return None

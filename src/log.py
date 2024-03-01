import logging

logger = logging.getLogger()
# 로그의 출력 기준 설정
logger.setLevel(logging.INFO)
# log 출력 형식
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# log 출력
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

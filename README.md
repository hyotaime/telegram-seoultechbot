# TechBot Project - Telegram Bot for SEOULTECH
## Introduction
[기존 Discord 기반의 봇 서비스를 제공하였던 테크봇](https://github.com/hgsanguk/discord-seoultechbot)
을 Telegram으로 마이그레이션 한 프로젝트입니다.

## Release
[텔레그램 테크봇](https://t.me/seoultech_bot)  
위 링크를 눌러 이 프로젝트의 안정적인 버전을 사용한 '테크봇'을 사용할 수 있습니다.

## Features and Commands
* 공지사항과 학식 자동 알림
  * 매일 자정 `/notice`를 켠 사용자에게 오늘의 학사일정을 보냅니다.
  * 30분 간격으로 학교 홈페이지의 학교공지사항, 학사공지, 장학공지, *생활관공지(선택)* 를 체크하여, 새 공지사항이 올라왔다면 `/notice`를 켠 사용자에게 알림을 보냅니다.

* 봇 조작 명령어
  * `/help`: 테크봇의 명령어 목록과 설명을 볼 수 있습니다.
  * `/notice`: 학교 공지사항과 학사일정 알림을 설정하는 명령어입니다.
    * **봇 초대 후 이 명령어를 입력하지 않으면 공지사항 알림, 학사일정 알림을 받을 수 없습니다.**
  * `/food`: 학식 메뉴 알림 시간을 설정하는 명령어입니다.
  * `/dorm`: 생활관 알림을 설정하는 명령어입니다.
  * `/ping`: 명령어 입력 시점부터 메세지 전송까지 총 지연시간을 보여줍니다.

* 학교 생활 명령어
  * `/cafe2`: 제2학생회관의 오늘 식단(점심, 저녁)을 보여줍니다. 2023년 1월 28일 기준으로 점심의 간단 snack 메뉴는 항상 같으므로 생략합니다.
    * `내일` 옵션으로 내일의 제2학생회관 식단을 확인 가능합니다.
  * `/tepark`: 테크노파크의 이번 주 식단표를 이미지로 보여줍니다.
  * `/weather`: 캠퍼스가 있는 공릉동의 날씨와 1 ~ 6시간 뒤 날씨 예보를 보여줍니다.

### Working Screenshots
- 첫 시작 화면<br><img width="488" alt="start" src="https://github.com/hgsanguk/discord-seoultechbot/assets/109580929/6ccada22-45b5-4fa0-bedd-43ee768c622c">
- 오늘의 학사일정<br><img width="488" alt="schedule" src="https://github.com/hgsanguk/discord-seoultechbot/assets/109580929/7aa12f1a-7cb7-46e7-bdef-8e4984553a88">
- 학교 공지사항<br><img width="488" alt="notice_example" src="https://github.com/hgsanguk/discord-seoultechbot/assets/109580929/4927f325-3bcc-4666-b481-6943008dffae">
- 생활관 공지사항<br><img width="488" alt="dorm_example" src="https://github.com/hgsanguk/discord-seoultechbot/assets/109580929/b81f0abf-af17-441b-be7e-ef3dec0cead9">
- `/help`<br><img width="488" alt="help" src="https://github.com/hgsanguk/discord-seoultechbot/assets/109580929/b2e50789-c5b0-41e5-b5ae-2753b6cef5fb">
- `/cafe2`<br><img width="488" alt="cafe2" src="https://github.com/hgsanguk/discord-seoultechbot/assets/109580929/bdd996ef-7bdc-46aa-8467-e6d8af40fccc">
- `/tepark`<br><img width="488" alt="tepark" src="https://github.com/hgsanguk/discord-seoultechbot/assets/109580929/8209f73c-cdd4-4ace-8a18-9f652ec4e665">
- `/weather`<br><img width="488" alt="weather" src="https://github.com/hgsanguk/discord-seoultechbot/assets/109580929/ffe1ce2a-2930-47e0-9ea8-6ebffc3e864a">
- `/notice`<br><img width="488" alt="notice" src="https://github.com/hgsanguk/discord-seoultechbot/assets/109580929/161b6792-5beb-4615-97d4-7b95cbe7bcb0">
- `/food`<br><img width="488" alt="food" src="https://github.com/hgsanguk/discord-seoultechbot/assets/109580929/bd352d72-6eed-45fc-bce2-35e154dd4eec">
- `/dorm`<br><img width="488" alt="dorm" src="https://github.com/hgsanguk/discord-seoultechbot/assets/109580929/92c245e3-65cf-4bf8-9218-95df6c77cf70">
- `/ping`<br><img width="488" alt="ping" src="https://github.com/hgsanguk/discord-seoultechbot/assets/109580929/54e3ab2b-8084-4ea7-9b06-e2e37afc9d76">
___
## Bug Report
문제 발생 시 반드시 **해당 오류 발생 시각과 오류 발생 명령어를 포함한** issue를 작성해 문제를 알려주시기 바랍니다.
___
## About Files
* [`main.py`](src/main.py): 테크봇의 메인 코드입니다. 이 코드를 실행하여 테크봇을 구동할 수 있습니다.
* [`log.py`](src/log.py): 로깅 모듈
* [`database.py`](src/database.py): 데이터베이스 관리
* [`schedule_notification.py`](src/schedule_notification.py): 학사일정 알림을 위한 코드입니다.
* [`crawlers`](src/crawlers) directory
  * [`foodcrawler.py`](src/crawlers/foodcrawler.py): 학교 홈페이지에서 식단을 크롤링하는 코드입니다.
  * [`noticecrawler.py`](src/crawlers/noticecrawler.py): 학교 공지사항과 일정을 크롤링하는 코드입니다.
* [`commands`](src/commands) directory
  * [`callback.py`](src/commands/callback.py): Callback을 처리하는 모듈
  * [`dorm.py`](src/commands/dorm.py): Dormitory 명령어 모듈
  * [`food.py`](src/commands/food.py): Food 명령어 모듈
  * [`help.py`](src/commands/help.py): Help 명령어 모듈
  * [`notice.py`](src/commands/notice.py): Notice 명령어 모듈
  * [`ping.py`](src/commands/ping.py): Ping 명령어 모듈
  * [`start.py`](src/commands/start.py): Start 명령어 모듈
  * [`weather.py`](src/commands/weather.py): Weather 명령어 모듈
* [`requirements.txt`](requirements.txt): 테크봇을 실행하는 데 필요한 패키지 목록
* [`example.env`](example.env): 환경변수 설정을 위한 예시 파일입니다.
___
## License
* 이 프로젝트의 라이센스는 GNU GPL 3.0이며, 자세한 내용은 [`LICENSE`](LICENSE)를 참고하시기 바랍니다.

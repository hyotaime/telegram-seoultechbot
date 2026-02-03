# TechBot Project - Telegram Bot for SEOULTECH

## Introduction
This project is a migration of [the previous Discord-based bot service](https://github.com/hgsanguk/discord-seoultechbot) to Telegram. It provides campus-related notifications and utilities for SeoulTech students and staff.

## Delivery / Channel
This service is delivered exclusively via public channels; interactive 1:1 command-based bots are no longer developed or supported.

## Release
Use the stable released channel via the following link:  
[SeoulTech Notice Channel](https://t.me/seoultech_notice)

## Features and Commands
* Automatic notifications for announcements and technopark cafeteria menus
  * Daily at 00:00, academic calendar updates are sent, highlighting events starting or ending today.
  * On weekdays at 07:00, Weather updates are sent.
  * Every Monday at 09:00, Technopark cafeteria weekly menu notifications are sent.
  * Every 10 minutes the bot checks the school website for new announcements (school notices, academic notices, scholarship notices) and notifies to the channel.
* ~~Bot control commands (Deprecated, supported but no longer developed or maintained)~~  
  * ~~`/help` \- View the list of commands and descriptions.~~
  * ~~`/tepark` \- Shows the Technopark cafeteria weekly menu as an image.~~
  * ~~`/weather` \- Shows the current weather in Gongneung-dong (campus area) and forecasts for the next 1 to 6 hours.~~
  * ~~`/ping` \- Shows the round-trip latency from command input to message delivery.~~

## Working Screenshots
- Start screen  
  ![start](https://github.com/user-attachments/assets/358c78d7-be55-4d30-8970-d24ce56c4692)
- Today's academic calendar  
  ![schedule](https://github.com/user-attachments/assets/da48172e-1733-46c3-a5bc-222afc36959c)
- School announcements  
  ![notice_example](https://github.com/user-attachments/assets/6e1e9ee1-ef6b-4f19-8ba0-8616140a8469)
- `/tepark`  
  ![tepark](https://github.com/user-attachments/assets/9f816474-8fc8-4702-80fb-de50f9bda79b)
- `/weather`  
  ![weather](https://github.com/user-attachments/assets/f4465d26-078d-4a67-a3e3-eea7c14601a9)
- `/ping`  
  ![ping](https://github.com/user-attachments/assets/fd02c766-925c-4ee4-9df5-146f67790789)

---

## Bug Report
When reporting an issue, please include the exact time the error occurred and the command that triggered the error.

## License
This project is licensed under GNU GPL 3.0. See the `LICENSE` file for details.

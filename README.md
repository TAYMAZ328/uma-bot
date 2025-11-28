# UMA Info Bot
A Telegram bot that automatically scrapes data from university websites, processes and categorizes the information, and provides it to students

## Corrent Features
### Data Scraping & Processing
- Real-time University Data: Automatic scraping of official university website
- Data Cleaning: Processes and structures raw website data
- Intelligent Classification: Categorizes information for easy access

### User-Friendly Interface
- Instant Responses: Quick delivery of requested information
- Organized Menus: Logical categorization of university data
- Simple Commands: Easy-to-use interaction system

### Information Categories
- Academic schedules and calendars
- University announcements and news

## Planned Features
- Teacher review system
- Study resources and references
- University service feedback
- Advanced data analytics
- Multi-university support

## Tech Stack
- Python
- Selenium
- Regex
- BeautifulSoup4
- Pyrogram
- MySQL

## Project Structure
```bash
uma-bot
├── bot/
│   ├── __init__.py
│   ├── admin_pannel/
│       ├── __init__.py
│       ├── admin.py
│       ├── user.py
│       ├── ban.py
│       ├── messaging.py
│       └── exportlogs.py
│
│   ├── handlers/
│       ├── __init__.py
│       ├── bot.py
│       ├── handler.py
│       ├── updater.py
│       ├── self_menu.py
│       └── unknown_msg.py
│   ├── app.py
│   ├── clock.py
│   ├── config.py
│   ├── menu.py
│   ├── keyboards.py
│   ├── scheduler.py
│   ├── reminder.py
│   └── util.py
│
├── scraper/
│   ├── __init__.py
│   ├── login.py
│   ├── scrap.py
│   └── extract.py
│
├── database/
│   ├── __init__.py
│   └── database.py
│
├── files/
│   ├── users.csv
│   ├── admins.csv
│   └── banned_users.csv
│
├── menu_data/
│   ├── pre.txt
│   ├── current.txt
│   └── next.txt
│
├── logs/
│   ├── commands.log
│   ├── cmds.log
│   └── errors.log
│
├── main.py
├── .env
├── requirements.txt
└── README.md
```

## License
MIT License
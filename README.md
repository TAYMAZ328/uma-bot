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
├── bot.py
├── database.py
├── login.py
├── scrap.py
├── extract.py
├── data/
│   ├── pre.txt
│   ├── current.txt
│   └── next.txt
├── files/
│   ├── users.csv
│   ├── admins.csv
│   ├── banned_users.csv
│   ├── commands.log
│   ├── errors.log
│   └── token.csv
├── requirements.txt
└── README.md
```

## License
MIT License
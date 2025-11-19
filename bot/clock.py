from datetime import datetime
from zoneinfo import ZoneInfo
import jdatetime


class IranClock:
    def __init__(self):
        self.zone = ZoneInfo("Asia/Tehran")

    def get_datetime(self):
        now = datetime.now(self.zone)
        time = now.strftime("%H:%M:%S")
        date = jdatetime.datetime.fromgregorian(datetime=now).strftime("%Y/%m/%d")

        return f"**📅 {date} | 🕛 {time}**"

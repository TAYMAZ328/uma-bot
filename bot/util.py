import os, logging
from datetime import datetime

from bot.config import db



def auth(message, role='admin'):
    user_id = int(message.from_user.id)
    if role == "user":
        banned = db.ban_list()
        if user_id in banned:
            return False
    elif role == "admin":
        admins = db.admins_list()
        if user_id not in admins:
            return False
    return True

def log_command(message):
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    user = message.from_user
    text = message.text
    with open(os.path.join("logs", "commands.log"), "a", encoding="utf-8") as f:
        f.write(f"[{date}]\nUser: {user.first_name + (user.last_name or ' ')}, {user.id}\n{text}\n\n")
    logging.info(text)

def log_error(error):
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(os.path.join("logs", "errors.log"), "a", encoding="utf-8") as f:
        f.write(f"[{date}]\n{error}\n")
    logging.error(error)

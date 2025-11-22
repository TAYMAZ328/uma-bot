from pyrogram.errors import UserIsBlocked

import asyncio

from bot.config import db, OWNER
from bot.util import log_error
from bot.app import app


async def broadcast_res():
    users_id = db.users_list()
    for user in users_id:
        try:
            await app.send_message(chat_id=user, text="سلف یادت نره!")
            await asyncio.sleep(0.2)

        except UserIsBlocked:
            await app.send_message(chat_id=OWNER, text=f"User: `{user}` has blocked the bot.")
        except Exception as e:
            await app.send_message(chat_id=OWNER, text=f"Failed sending message to user {user}: {e}")
            log_error(f"Failed sending to {user}: {e}")


async def remind_update():
    admins = db.admins_list()
    for adm in admins:
        try:
            await app.send_message(chat_id=adm, text="UPDATE TIME!")
            await asyncio.sleep(0.2)
        except Exception as e:
            log_error(f"Failed sending to Admin {adm}: {e}")



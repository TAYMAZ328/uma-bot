from pyrogram import filters
from pyrogram.types import Message

from datetime import datetime

from bot.util import log_command, log_error, auth
from bot.config import OWNER
from bot.app import app



@app.on_message(filters.private & ~filters.regex(r"^/") & ~filters.regex(r"^مشاهده منوی سلف$|^اطلاعات استاد ها$|^ثبت نظر$|^جزوات و منابع درسی$|^راهنما$|^بازگشت$|^پنل ادمین$|^⬅️ Back$|^🔄️ update$|^🧾 logs$|^👤 admins$|^🚫 bans$|^⭐ users$"))
async def none_cmd_msg(client, message: Message):
    log_command(message)
    if not auth(message, "user"): return

    try:
        user_id = message.from_user.id
        if int(user_id) == OWNER: return
        user = await client.get_users(user_id)
        await message.forward(chat_id=OWNER)
        await client.send_message(chat_id=OWNER, text=f"User: `{user.first_name} {user.last_name or ' '}`\nID: `{user.id}`\nUsername: {f'@{user.username}' if user.username else f'[{user.first_name}](tg://user?id={user.id})'}\n{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    except Exception as e:
        await client.send_message(chat_id=OWNER, text=f"Failed sending message from user {user_id}: {e}")
        log_error(f"Failed sending message from user {user_id}: {e}")

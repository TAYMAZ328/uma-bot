from pyrogram.types import Message
from pyrogram import filters

import os

from bot.util import log_command, log_error, auth
from bot.config import db
from bot.app import app



@app.on_message(filters.command("user") & filters.private)
async def user_info(client, message: Message):
    if not auth(message): return
    log_command(message)

    if len(message.command) < 2:
        await message.reply_text("Invalid user")
        return

    user_id = message.command[1]
    try:
        user = await client.get_users(user_id)
        peer = await client.resolve_peer(user_id)
        access_hash = peer.access_hash
        date = db.select_user(user.id)
        await message.reply_text(
            f"""**👤 User Information**

**🧾 Name:** `{user.first_name or ''} {user.last_name or ''}`
**🆔 ID:** `{user.id}`
**🔑 Access Hash:** `{access_hash}`

**🏷 Username:** {
    f"@{user.username}"
    if user.username
    else f"[{user.first_name}](tg://user?id={user.id})"
    }

**⭐ Premium:** `{user.is_premium}`
**🙋‍♂️ Self:** `{user.is_self}`
**📅 Registered:** `{date}`
""",
            disable_web_page_preview=True,
        )

    except Exception as e:
        await message.reply_text("User has never started the bot")
        log_error(f"User info Error: {e}")


@app.on_message(filters.command("users") | filters.regex("^/users ⭐$"))
async def all_user_info(_, message: Message):
    if not auth(message): return
    log_command(message)

    users_num = db.select_users()
    await message.reply_document(os.path.join("files", "users.csv"), caption=f"[ {users_num} ] Users have been registered so far")

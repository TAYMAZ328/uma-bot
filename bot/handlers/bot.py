from pyrogram.types import Message
from pyrogram import filters

from bot.util import log_command, log_error, auth
from bot.handlers.handler import show_keyboard
from bot.keyboards import KEYBOARDS
from bot.config import db
from bot.app import app


@app.on_message(filters.command('start') & filters.private)
async def start(client, message: Message):
    if not auth(message, "user"): return
    log_command(message)
    
    try:
        if auth(message):
            await show_keyboard(client, message, role="admin")
        else:
            user = message.from_user
            peer = await client.resolve_peer(user.id)
            access_hash = peer.access_hash
            db.insert_user(user, access_hash)
            await show_keyboard(client, message)

    except Exception as e:
        log_error(f"Failed starting bot: user {message.from_user.id}: {message.text}\n{e}")


@app.on_message(filters.command("help") | filters.regex("^پنل ادمین$") & filters.private)
async def help(_, message: Message):
    if not auth(message): return

    keyboard = KEYBOARDS["admin_pannel"]

    await message.reply_text("""
**🤖 Available Bot Commands**

**🧩 General**
`/code [captcha_code]` — Verify captcha  
`/help` — Show this help message  
`/update` — Update the main menu  

**👤 User Management**
`/user [ID | Username]` — Get user info  
`/users` — Show list of all users  
`/admins` — Show list of all admins  
`/bans` — Show list of banned users  

**⚙️ Admin Controls**
`/admin [0 | 1] [user_ID]` — Promote or dismiss admin (1 → promote, 0 → dismiss)  
`/ban [user_ID]` — Ban a user  
`/unban [user_ID]` — Unban a user  

**📢 Messaging**
`/broadcast` — Send message to all users  
`/direct` — Send direct message to a specific user  

**🧾 Logs**
`/logs [number]` — Export logs (default: all)
"""
, reply_markup=keyboard, quote=True)


@app.on_message(filters.regex("^⬅️ Back$") & filters.private)
async def back_to_start(client, message: Message):
    if auth(message):
        await show_keyboard(client, message, role="admin")

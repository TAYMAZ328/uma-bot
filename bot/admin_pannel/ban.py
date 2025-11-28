from pyrogram.types import Message
from pyrogram import filters

import os

from bot.util import log_command, log_error, auth
from bot.config import db, OWNER
from bot.app import app



@app.on_message(filters.command("unban"))
async def unban_user(_, message: Message):
    if not auth(message): return
    log_command(message)
    
    try:
        if len(message.command) < 2:
            await message.reply_text("Invalid command")
            return

        user_id = int(message.command[1])
        state = db.unban_user(user_id)

        if state:
            await message.reply_text("The User Unbanned")
        else:
            await message.reply_text("User was never banned")

    except Exception as e:
        log_error(f"Failed unaban user: {message.text}\n{e}")


@app.on_message(filters.command("ban"))
async def ban_user(_, message: Message):
    if not auth(message): return
    log_command(message)
    try:
        if len(message.command) < 2:
            await message.reply_text("Invalid command")
            return

        user_id = int(message.command[1])
        if user_id in db.admins_list() or user_id == OWNER:
            await message.reply_text("The User is Admin")
            return

        state = db.ban_user(user_id)
        if state:
            await message.reply_text("The User Banned")
        else:
            await message.reply_text("User has never started the bot")
    
    except Exception as e:
        log_error(f"Failed ban user: {message.text}\n{e}")


@app.on_message(filters.command("bans") | filters.regex("^🚫 bans$"))
async def banned_users(_, message: Message):
    if not auth(message): return
    log_command(message)

    bans_num = db.select_bans()
    await message.reply_document(os.path.join("files", "banned_users.csv"), caption=f"[ {bans_num} ] Users have been Banned")

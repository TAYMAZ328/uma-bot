from pyrogram.types import Message
from pyrogram import filters

import os

from bot.util import log_command, log_error, auth
from bot.config import db, OWNER
from bot.app import app


@app.on_message(filters.command("admin") & filters.private)
async def add_admin(_, message: Message):
    if not auth(message): return
    log_command(message)
    
    try:
        if len(message.command) < 3:
            await message.reply_text("Invalid command")
            return

        admin_id = int(message.command[2])
        if message.command[1] == '1':
            if admin_id in db.admins_list():
                await message.reply_text("User is already an Admin")

            else:
                state = db.insert_admin(admin_id)
                if state:
                    await message.reply_text("User added to Admins")
                else:
                    await message.reply_text("User has never started the bot")

        elif message.command[1] == '0':
            if admin_id == OWNER:
                await message.reply_text("Permission Denied")
                return

            if admin_id in db.admins_list():
                state = db.del_admin(admin_id)
                if state:
                    await message.reply_text("Admin dismissed successfully")
                else:
                    await message.reply_text("No admin dismissed — ID not found")
            else:
                await message.reply_text("User not in Admin list")

    except Exception as e:
        log_error(f"Failed promote/dismiss admin: {message.text}\n{e}")


@app.on_message(filters.command("admins") | filters.regex("^/admins 👤$") & filters.private)
async def admins(_, message: Message):
    if not auth(message): return
    log_command(message)

    admins_num = db.select_admins()
    await message.reply_document(os.path.join("files", "admins.csv"), caption=f"[ {admins_num} ] Admins have been promoted so far")

from pyrogram.types import Message
from pyrogram import filters

import os

from bot.util import log_command, log_error, auth
from bot.app import app


@app.on_message(filters.command("logs") | filters.regex("^/logs 🧾$") & filters.private)
async def user_info(_, message: Message):
    if not auth(message): return
    log_command(message)
    try:
        if len(message.command) == 1:
            await message.reply_document(os.path.join("logs", "commands.log"), caption=f"All logs")

        elif len(message.command) == 2:
            num = int(message.command[1]) * 4

            with open(os.path.join("logs", "commands.log"), 'r', encoding="utf-8") as f:
                c = f.readlines()[-num:]

            with open(os.path.join("logs", "cmds.txt"), 'w', encoding="utf-8") as f:
                f.writelines(c)
        
            await message.reply_document(os.path.join("logs", "cmds.txt"), caption=f"[ {num} ] lines of log")

    except Exception as e:
        log_error(f"Failed exporting logs: {message.text}\n{e}")
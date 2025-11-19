from pyrogram.types import Message
from pyrogram import filters

import asyncio

from bot.util import log_command, log_error, auth
from bot.app import app
from bot.config import db



@app.on_message(filters.command("direct"))
async def direct(_, message: Message):
    if not auth(message): return
    log_command(message)

    msg = message.reply_to_message
    if not msg:
        await message.reply_text("No message selected")
        return

    if len(message.command) != 2:
        await message.reply_text("Invalid command")
        return
    
    user_id = int(message.command[1])
    if user_id not in db.users_list():
        await message.reply_text("User has never started the bot")
        return
    try:
        await msg.copy(chat_id=user_id)
        await message.reply_text("Sent")
    except Exception as e:
        await message.reply_text(f"Failed sending message to user {user_id}: {e}")
        log_error(f"Failed sending message to user {user_id}: {e}")


@app.on_message(filters.command("broadcast"))
async def broadcast(_, message: Message):
    if not auth(message): return
    log_command(message)

    msg = message.reply_to_message
    if not msg:
        await message.reply_text("No message selected")
        return

    users_id = db.users_list()
    await message.reply_text("Broadcasting...")
    for user in users_id:
        try:
            await msg.copy(chat_id=user)
            await asyncio.sleep(0.5)
        except Exception as e:
            await message.reply_text(f"Failed sending message to user {user}: {e}")
            log_error(f"Failed sending message to user {user}: {e}")
    await message.edit_text("Broadcast complete")
from pyrogram import filters
from pyrogram.types import Message


from bot.util import log_command, auth
from .handler import show_keyboard
from bot.menu import show_cnt
from bot.app import app


@app.on_message(filters.command("menu") | filters.regex("^مشاهده منوی سلف$") & filters.private)
async def menu(client, message: Message):
    log_command(message)
    if not auth(message, "user"): return

    await show_cnt(client, message)
    await show_keyboard(client, message, role='menu')


@app.on_message(filters.command("menu") | filters.regex("^بازگشت$") & filters.private)
async def back(client, message: Message):
    log_command(message)
    if not auth(message, "user"): return

    if auth(message): return await show_keyboard(client, message, role='back_admin')
    await show_keyboard(client, message, role='back')
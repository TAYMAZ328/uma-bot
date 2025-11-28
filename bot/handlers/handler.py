from pyrogram.types import Message
from pyrogram import filters


from bot.util import log_command, auth
from bot.keyboards import KEYBOARDS
from bot.app import app


@app.on_message(filters.regex("^ثبت نظر$") & filters.private)
async def vote(_, message: Message):
    log_command(message)
    if not auth(message, "user"): return

    await message.reply_text("درحال توسعه...")


@app.on_message(filters.regex("^اطلاعات استاد ها$") & filters.private)
async def teachers_info(_, message: Message):
    log_command(message)
    if not auth(message, "user"): return

    await message.reply_text("درحال توسعه...")


@app.on_message(filters.regex("^جزوات و منابع درسی$") & filters.private)
async def refrences(_, message: Message):
    log_command(message)
    if not auth(message, "user"): return

    await message.reply_text("درحال توسعه...")


@app.on_message(filters.regex("^راهنما$") & filters.private)
async def guide(_, message: Message):
    log_command(message)
    if not auth(message, "user"): return

    await message.reply_text("درحال توسعه...")


async def show_keyboard(_, message: Message, role='new'):
    keyboard = KEYBOARDS["user_pannel"]
    admin_keyboard = KEYBOARDS["admin_keyboard"]
    back_keyboard = KEYBOARDS["back"]

    if role == 'new':
        await message.reply_text(
            text="🤖 به ربات خوش آمدید!\n\n"
            "لطفا یکی از گزینه های زیر را انتخاب کنید:",
            reply_markup=keyboard, quote=True)

    elif role == 'back':
        await message.reply_text(text="🏛", reply_markup=keyboard)

    elif role == 'back_admin':
        await message.reply_text(text="🏛", reply_markup=admin_keyboard)

    elif role == 'menu':
        await message.reply_text(text="🍽", reply_markup=back_keyboard)

    elif role == "admin":
        await message.reply_text(
            text="🤖 به ربات خوش آمدید!\n\n"
            "لطفا یکی از گزینه های زیر را انتخاب کنید:",
            reply_markup=admin_keyboard, quote=True)


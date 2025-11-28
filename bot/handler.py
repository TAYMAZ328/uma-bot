from pyrogram.types import Message, ReplyKeyboardMarkup
from pyrogram import filters

from datetime import datetime

from bot.util import log_command, log_error, auth
from bot.menu import show_cnt
from bot.config import OWNER
from bot.app import app


@app.on_message(filters.private & ~filters.regex(r"^/"))
async def res(client, message: Message):
    log_command(message)
    if not auth(message, "user"): return

    if message.text:
        if message.text == "مشاهده منوی سلف":
            await show_cnt(client, message)
            await show_keyboard(client, message, role='menu')

        elif message.text == "ثبت نظر":
            await message.reply_text("درحال توسعه...")

        elif message.text == "اطلاعات استاد ها":
            await message.reply_text("درحال توسعه...")

        elif message.text == "جزوات و منابع درسی":
            await message.reply_text("درحال توسعه...")

        elif message.text == "راهنما":
            await message.reply_text("درحال توسعه...")

        elif message.text == "بازگشت":
            await show_keyboard(client, message, role='back')

        else:
            await none_cmd_msg(client, message)

    else:
        await none_cmd_msg(client, message)


async def show_keyboard(_, message: Message, role='new'):
    keyboard = ReplyKeyboardMarkup([
        ["مشاهده منوی سلف"],
        ["ثبت نظر", "اطلاعات استاد ها"],
        ["راهنما", "جزوات و منابع درسی"]
    ],
        resize_keyboard=True
    )

    admin_keyboard = ReplyKeyboardMarkup([
        ["مشاهده منوی سلف"],
        ["ثبت نظر", "اطلاعات استاد ها"],
        ["راهنما", "جزوات و منابع درسی"],
        ["/Admin"],
    ],
        resize_keyboard=True
    )

    back_keyboard = ReplyKeyboardMarkup([['بازگشت']], resize_keyboard=True)

    if role == 'new':
        await message.reply_text(
            text="🤖 به ربات خوش آمدید!\n\n"
            "لطفا یکی از گزینه های زیر را انتخاب کنید:",
            reply_markup=keyboard, quote=True)

    elif role == 'back':
        await message.reply_text(text="🏛", reply_markup=keyboard)

    elif role == 'menu':
        await message.reply_text(text="🍽", reply_markup=back_keyboard)

    elif role == "admin":
        await message.reply_text(
            text="🤖 به ربات خوش آمدید!\n\n"
            "لطفا یکی از گزینه های زیر را انتخاب کنید:",
            reply_markup=admin_keyboard, quote=True)

async def none_cmd_msg(client, message):
    try:
        user_id = message.from_user.id
        if int(user_id) == OWNER: return
        user = await client.get_users(user_id)
        await message.forward(chat_id=OWNER)
        await client.send_message(chat_id=OWNER, text=f"User: `{user.first_name} {user.last_name or ' '}`\nID: `{user.id}`\nUsername: {f'@{user.username}' if user.username else f'[{user.first_name}](tg://user?id={user.id})'}\n{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    except Exception as e:
        await client.send_message(chat_id=OWNER, text=f"Failed sending message from user {user_id}: {e}")
        log_error(f"Failed sending message from user {user_id}: {e}")

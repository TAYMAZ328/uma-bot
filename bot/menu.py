from pyrogram.types import Message, CallbackQuery
from pyrogram.errors import MessageNotModified

from bot.keyboards import KEYBOARDS
from bot.clock import IranClock
from scraper import extract
from bot.util import auth
from bot.app import app

menu = extract.Menu()
menu.update()

ic = IranClock()



async def show_menu(_, message: Message, week="current"):
    key_menu = KEYBOARDS["menu_btn"]
    cnt = KEYBOARDS["current_btn"]

    try:
        match week:
            case 'pre':
                await message.edit_text(f"{ic.get_datetime()}\n{menu.pre}", reply_markup=cnt)
            case 'current':
                await message.edit_text(f"{ic.get_datetime()}\n{menu.current}", reply_markup=key_menu)
            case 'next':
                await message.edit_text(f"{ic.get_datetime()}\n{menu.next}", reply_markup=cnt)
    except MessageNotModified:
        pass

async def show_cnt(_, message: Message):
    key_menu = KEYBOARDS["menu_btn"]

    await message.reply_text(f"{ic.get_datetime()}{menu.current}", reply_markup=key_menu)


@app.on_callback_query()
async def handle_callback(client, callback_query: CallbackQuery):
    if not auth(callback_query.message, "user"): return
    key = callback_query.data
    if key == "pre":
        await callback_query.answer("⏪ هفته قبل انتخاب شد.")
        await show_menu(client, callback_query.message, week='pre')

    elif key == "current":
        await callback_query.answer("📅 هفته جاری انتخاب شد.")
        await show_menu(client, callback_query.message, week='current')

    elif key == "next":
        await callback_query.answer("⏩ هفته بعدی انتخاب شد.")
        await show_menu(client, callback_query.message, week='next')

    elif key == "close":
        await callback_query.answer("❌ منو بسته شد.")
        await callback_query.message.delete()

    else:
        await callback_query.answer("⚠️ گزینه نامعتبر است.")
from pyrogram.types import Message
from pyrogram import filters

from scraper import scrap, login, extract

from bot.util import log_command, log_error, auth
from bot.menu import menu
from bot.app import app



@app.on_message(filters.command("update"))
async def updater(_, message: Message):
    if not auth(message): return
    log_command(message)

    await message.reply_text("Updating started")
    path = login.get_cap()
    await message.reply_document(path, caption="CAPTCHA")


@app.on_message(filters.command("code"))
async def get_captcha(_, message: Message):
    if not auth(message): return
    log_command(message)
    try:
        cap = message.command[1]

        await message.reply_text("Logging in...")
        driver = login.login(cap)
        await message.reply_text("Updating...")

        for week in ('pre', 'current', 'next'):
            driver = scrap.update_week(driver, week)
            src = scrap.scrap(driver)
            string = extract.extract(src)
            extract.write(string, week)
        driver.quit()
        menu.update()
        await message.reply_text("Weeks are updated.")
    
    except Exception as e:
        await message.reply_text(f"Error while updating: {e}")
        log_error(f"Error updating: {e}")

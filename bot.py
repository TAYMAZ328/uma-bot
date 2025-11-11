from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, ReplyKeyboardMarkup
from pyrogram.errors import MessageNotModified
from pyrogram import Client, filters

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime
import csv, logging, asyncio, os

import extract, login, scrap, database


def get_token():
    with open(os.path.join("files", "tokens.csv"), "r") as f:
        c = csv.reader(f)
        c = list(c)[0]
        return c[0].strip(), c[1].strip(), int(c[2]), int(c[3])

def get_db():
    with open(os.path.join("files", "tokens.csv"), "r") as f:
        c = csv.reader(f)
        c = list(c)[2]
        return c[0].strip(), c[1].strip(), c[2].strip(), c[3].strip()

def auth(message, role='admin'):
    user_id = int(message.from_user.id)
    if role == "user":
        banned = db.ban_list()
        if user_id in banned:
            return False
    elif role == "admin":
        admins = db.admins_list()
        if user_id not in admins:
            return False
    return True


HOST, USERNAME, PASSWORD, DB_NAME = get_db()
db = database.DB(host=HOST, username=USERNAME, password=PASSWORD, db_name=DB_NAME)
db.connect_db()

menu = extract.Menu()
menu.update()


TOKEN, HASH, ID, OWNER = get_token()
app = Client('uma_bot', bot_token=TOKEN, api_id=ID, api_hash=HASH)


@app.on_message(filters.command('start'))
async def start(client, message: Message):
    if not auth(message, "user"): return
    log_command(message)

    user = message.from_user
    peer = await client.resolve_peer(user.id)
    access_hash = peer.access_hash

    db.insert_user(user, access_hash)

    await show_keyboard(client, message)


@app.on_message(filters.command("code"))
async def get_captcha(client, message: Message):
    if not auth(message): return
    log_command(message)
    cap = message.command[1]

    await message.reply_text("Logging in...")
    driver = login.login(cap)
    await message.reply_text("Updating...")

    for week in ('pre', 'corrent', 'next'):
        driver = scrap.update_week(driver, week)
        src = scrap.scrap(driver)
        string = extract.extract(src)
        extract.write(string, week)
    driver.quit()

    menu.update()

    await message.reply_text("Weeks are updated.")


@app.on_message(filters.command("help"))
async def help(client, message: Message):
    if not auth(message): return

    await message.reply_text("""
/code [captcha code]
/admin [0: dismiss | 1: promote] [user ID] promote and dismiss admin
/user [ID | Username] User info
/users All users list
/admins All admins list
/bans All banned users list
/ban [user ID] ban User
/unban [user ID] Unban User
/update  Update menu
/broadcast send message to all users
/direct send direct message to a user
/logs [Null/ number of logs] Export logs
/help""")


@app.on_message(filters.command("direct"))
async def direct(client, message: Message):
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


@app.on_message(filters.command("kill"))
async def shutdown(client, message: Message):
    if not auth(message): return
    log_command(message)
    await message.reply_text("Force shutdown...")
    os._exit(0)


@app.on_message(filters.command("broadcast"))
async def broadcast(client, message: Message):
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
            log_error(f"Failed sending message to user {user}: {e}")
    await message.edit_text("Broadcast complete")


async def broadcast_res():
    users_id = db.users_list()
    for user in users_id:
        try:
            await app.send_message(chat_id=user, text="سلف یادت نره!")
            await asyncio.sleep(0.2)
        except Exception as e:
            log_error(f"Failed sending to {user}: {e}")


async def remind_update():
    admins = db.admins_list()
    for adm in admins:
        try:
            await app.send_message(chat_id=adm, text="UPDATE TIME!")
            await asyncio.sleep(0.2)
        except Exception as e:
            log_error(f"Failed sending to Admin {adm}: {e}")


@app.on_message(filters.command("update"))
async def updater(client, message: Message):
    if not auth(message): return
    log_command(message)

    await message.reply_text("Updating started")
    path = login.get_cap()
    await message.reply_document(path, caption="CAPTCHA")


@app.on_message(filters.command("unban"))
async def unban_user(client, message: Message):
    if not auth(message): return
    log_command(message)

    if len(message.command) < 2:
        await message.reply_text("Invalid command")
        return

    user_id = int(message.command[1])
    state = db.unban_user(user_id)

    if state:
        await message.reply_text("The User Unbanned")
    else:
        await message.reply_text("User was never banned")


@app.on_message(filters.command("ban"))
async def ban_user(client, message: Message):
    if not auth(message): return
    log_command(message)

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


@app.on_message(filters.command("bans"))
async def banned_users(client, message: Message):
    if not auth(message): return
    log_command(message)

    bans_num = db.select_bans()
    await message.reply_document(os.path.join("files", "banned_users.csv"), caption=f"[ {bans_num} ] Users have been Banned")

@app.on_message(filters.command("users"))
async def all_user_info(client, message: Message):
    if not auth(message): return
    log_command(message)

    users_num = db.select_users()
    await message.reply_document(os.path.join("files", "users.csv"), caption=f"[ {users_num} ] Users have been registered so far")

@app.on_message(filters.command("admins"))
async def admins(client, message: Message):
    if not auth(message): return
    log_command(message)

    admins_num = db.select_admins()
    await message.reply_document(os.path.join("files", "admins.csv"), caption=f"[ {admins_num} ] Admins have been promoted so far")


@app.on_message(filters.command("logs"))
async def user_info(client, message: Message):
    if not auth(message): return
    log_command(message)

    if len(message.command) == 1:
        await message.reply_document(os.path.join("files", "commands.log"), caption=f"All logs")

    elif len(message.command) == 2:
        num = int(message.command[1]) * 4

        with open(os.path.join("files", "commands.log"), 'r', encoding="utf-8") as f:
            c = f.readlines()[-num:]

        with open(os.path.join("files", "cmds.txt"), 'w', encoding="utf-8") as f:
            f.writelines(c)
    
        await message.reply_document(os.path.join("files", "cmds.txt"), caption=f"[ {num} ] lones of log")


@app.on_message(filters.command("user"))
async def user_info(client, message: Message):
    if not auth(message): return
    log_command(message)

    if len(message.command) < 2:
        await message.reply_text("Invalid user")
        return

    user_id = message.command[1]
    try:
        user = await client.get_users(user_id)
        peer = await client.resolve_peer(user_id)
        access_hash = peer.access_hash
        date = db.select_user(user.id)
        await message.reply_text(f"User: `{user.first_name} {user.last_name or ' '}`\nID: `{user.id}`\nAccess Hash: {access_hash}\nUsername: {f"@{user.username}" if user.username else f"[{user.first_name}](tg://user?id={user.id})"}\n"
            f"Phone Number: {getattr(user, 'phone', 'Hidden')}\nSelf: {user.is_self}\nPremium: {user.is_premium}\nRegisteration Date: {date}")
    except Exception as e:
        await message.reply_text("User has never started the bot")
        log_error(f"User info Error: {e}")


@app.on_message(filters.command("admin"))
async def add_admin(client, message: Message):
    if not auth(message): return
    log_command(message)

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


async def none_cmd_msg(client, message):
    try:
        user_id = message.from_user.id
        if int(user_id) == OWNER: return
        user = await client.get_users(user_id)
        await message.forward(chat_id=OWNER)
        await client.send_message(chat_id=OWNER, text=f"User: `{user.first_name} {user.last_name or ' '}`\nID: `{user.id}`\nUsername: {f"@{user.username}" if user.username else f"[{user.first_name}](tg://user?id={user.id})"}\n{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}")
    except Exception as e:
        await client.send_message(chat_id=OWNER, text=f"Failed sending message from user {user_id}: {e}")
        log_error(f"Failed sending message from user {user_id}: {e}")


async def show_menu(client, message: Message, week="corrent"):

    key_menu = InlineKeyboardMarkup([
        [
        InlineKeyboardButton("هفته قبل", callback_data="pre"),
        InlineKeyboardButton("هفته جاری", callback_data="corrent"),
        InlineKeyboardButton("هفته بعد", callback_data="next")],
    [InlineKeyboardButton("بستن منو", callback_data="close")]])    

    cnt = InlineKeyboardMarkup([
        [InlineKeyboardButton("هفته جاری", callback_data="corrent")],
    [InlineKeyboardButton("بستن منو", callback_data="close")]])

    try:
        match week:
            case 'pre':
                await message.edit_text(menu.pre, reply_markup=cnt)
            case 'corrent':
                await message.edit_text(menu.corrent, reply_markup=key_menu)
            case 'next':
                await message.edit_text(menu.next, reply_markup=cnt)
    except MessageNotModified:
        pass


@app.on_message(filters.private)
async def res(client, message: Message):
    log_command(message)
    if not auth(message, "user"): return

    if message.text:
        match message.text:
            case "مشاهده منوی سلف":
                await show_cnt(client, message)
                await show_keyboard(client, message, role='menu')
            case "ثبت نظر":
                await message.reply_text("درحال توسعه...")
            case "اطلاعات استاد ها":
                await message.reply_text("درحال توسعه...")
            case "جزوات و منابع درسی":
                await message.reply_text("درحال توسعه...")
            case "راهنما":
                await message.reply_text("درحال توسعه...")
            case 'بازگشت':
                await show_keyboard(client, message, role='back')
            case _:
                await none_cmd_msg(client, message)
    else:
        await none_cmd_msg(client, message)


@app.on_callback_query()
async def handle_callback(client, callback_query: CallbackQuery):
    if not auth(callback_query.message, "user"): return
    key = callback_query.data
    match key:
        case "pre":
            await callback_query.answer("هفته قبل انتخاب شد.")
            await show_menu(client, callback_query.message, week='pre')
        case "corrent":
            await callback_query.answer("هفته جاری انتخاب شد.")
            await show_menu(client, callback_query.message, week='corrent')
        case "next":
            await callback_query.answer("هفته بعدی انتخاب شد.")
            await show_menu(client, callback_query.message, week='next')

        case "close":
            await callback_query.answer("منو بسته شد.")
            await callback_query.message.delete()


async def show_cnt(cliet, message: Message):
    key_menu = InlineKeyboardMarkup([
        [
        InlineKeyboardButton("هفته قبل", callback_data="pre"),
        InlineKeyboardButton("هفته جاری", callback_data="corrent"),
        InlineKeyboardButton("هفته بعد", callback_data="next")],
    [InlineKeyboardButton("بستن منو", callback_data="close")]]
    ) 
    await message.reply_text(extract.read("corrent"), reply_markup=key_menu)

async def show_keyboard(client, message: Message, role='new'):

    keyboard = ReplyKeyboardMarkup([
        ["مشاهده منوی سلف"],
        ["ثبت نظر", "اطلاعات استاد ها"],
        ["راهنما", "جزوات و منابع درسی"]], resize_keyboard=True)

    if role == 'new':
        await message.reply_text(
            "🤖 به ربات خوش آمدید!\n\n"
            "لطفا یکی از گزینه های زیر را انتخاب کنید:",
            reply_markup=keyboard)

    elif role == 'back':
        await message.reply_text("🏛", reply_markup=keyboard)

    elif role == 'menu':
        back = ReplyKeyboardMarkup([
            ['بازگشت']], resize_keyboard=True)
    
        await message.reply_text("🍽", reply_markup=back)


def log_command(message):
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    user = message.from_user
    text = message.text
    with open(os.path.join("files", "commands.log"), "a", encoding="utf-8") as f:
        f.write(f"[{date}]\nUser: {user.first_name + (user.last_name or ' ')}, {user.id}\n{text}\n\n")
    logging.info(text)

def log_error(error):
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(os.path.join("files", "errors.log"), "a", encoding="utf-8") as f:
        f.write(f"[{date}]\n{error}\n")
    logging.error(error)


async def setup_scheduler():
    scheduler = AsyncIOScheduler()
    
    scheduler.add_job(
        broadcast_res,
        trigger='cron',
        day_of_week='thu',
        hour=22,
        minute=0,
        timezone='Asia/Tehran'
    )

    scheduler.add_job(
        remind_update,
        trigger='cron',
        day_of_week='sat',
        hour=13,
        minute=0,
        timezone='Asia/Tehran'
    )

    scheduler.start()


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(setup_scheduler())
    app.run()

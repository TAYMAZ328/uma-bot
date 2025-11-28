from pyrogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton

KEYBOARDS = {
    "admin_pannel": ReplyKeyboardMarkup(
        [
        ["🔄️ update", "🧾 logs"],
        ["⭐ users", "👤 admins", "🚫 bans"],
        ["⬅️ Back"]
        ],
        resize_keyboard=True),

    "user_pannel": ReplyKeyboardMarkup(
        [
        ["مشاهده منوی سلف"],
        ["ثبت نظر", "اطلاعات استاد ها"],
        ["راهنما", "جزوات و منابع درسی"]
        ],
        resize_keyboard=True),

    "admin_keyboard": ReplyKeyboardMarkup(
        [
        ["مشاهده منوی سلف"],
        ["ثبت نظر", "اطلاعات استاد ها"],
        ["راهنما", "جزوات و منابع درسی"],
        ["پنل ادمین"],
        ],
        resize_keyboard=True),

    "back": ReplyKeyboardMarkup([['بازگشت']], resize_keyboard=True),

    "menu_btn": InlineKeyboardMarkup([
        [
            InlineKeyboardButton("⏪ هفته قبل", callback_data="pre"),
            InlineKeyboardButton("📅 هفته جاری", callback_data="current"),
            InlineKeyboardButton("⏩ هفته بعد", callback_data="next"),
        ],
        [
            InlineKeyboardButton("❌ بستن منو", callback_data="close"),
        ]
    ]),

    "current_btn": InlineKeyboardMarkup([
        [
            InlineKeyboardButton("📅 هفته جاری", callback_data="current"),
        ],
        [
            InlineKeyboardButton("❌ بستن منو", callback_data="close"),
        ]
    ]),



}
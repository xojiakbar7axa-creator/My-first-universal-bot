import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import (
    Message, CallbackQuery,
    InlineKeyboardMarkup, InlineKeyboardButton,
    ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
)

# =====================
# TOKEN
# =====================
TOKEN = "8581731147:AAF4F9JRYYaCmmNeBjRtCQOjC8_hDLfk7Kg"

bot = Bot(token=TOKEN)
dp = Dispatcher()

# =====================
# CONTACTS
# =====================
INSTAGRAM_URL = "https://instagram.com/xojiakbarr_7"
TELEGRAM_USERNAME = "@rio_pantera"
PHONE_NUMBER = "+998507776998"

# user_id -> lang
user_lang = {}  # "uz"/"ru"/"en"

# =====================
# TEXTS
# =====================
def t(lang: str, key: str) -> str:
    texts = {
        "menu": {"uz": "Menyu", "ru": "Меню", "en": "Menu"},
        "choose_lang": {"uz": "Tilni tanlang / Choose language:", "ru": "Выберите язык / Choose language:", "en": "Choose language:"},

        "btn_contact": {"uz": "📩 Bog‘lanish", "ru": "📩 Связаться", "en": "📩 Contact"},
        "btn_instagram": {"uz": "📸 Instagram", "ru": "📸 Instagram", "en": "📸 Instagram"},
        "btn_services": {"uz": "🤖 Xizmatlar", "ru": "🤖 Услуги", "en": "🤖 Services"},
        "btn_change_lang": {"uz": "🌐 Tilni o‘zgartirish", "ru": "🌐 Сменить язык", "en": "🌐 Change language"},
        "btn_back": {"uz": "⬅️ Ortga", "ru": "⬅️ Назад", "en": "⬅️ Back"},

        "contact_title": {"uz": "Biz bilan aloqa 👇", "ru": "Связь 👇", "en": "Contact 👇"},
        "services_title": {"uz": "Xizmatlar 👇", "ru": "Услуги 👇", "en": "Services 👇"},

        "phone": {"uz": f"📞 Telefon: {PHONE_NUMBER}", "ru": f"📞 Телефон: {PHONE_NUMBER}", "en": f"📞 Phone: {PHONE_NUMBER}"},
        "instagram_msg": {"uz": f"📸 Instagram: {INSTAGRAM_URL}", "ru": f"📸 Instagram: {INSTAGRAM_URL}", "en": f"📸 Instagram: {INSTAGRAM_URL}"},
        "tg_msg": {"uz": f"💬 Telegram: {TELEGRAM_USERNAME}", "ru": f"💬 Telegram: {TELEGRAM_USERNAME}", "en": f"💬 Telegram: {TELEGRAM_USERNAME}"},

        "services_text": {
            "uz": (
                "🚀 Har qanday murakkablikdagi Telegram botlarni 1–5 kunda yaratib beramiz!\n\n"
                "Masalan:\n"
                "• 🛒 Savdo bot (katalog + buyurtma)\n"
                "• 📦 Zakaz qabul qilish bot\n"
                "• 🎓 O‘quv markaz ro‘yxat bot\n"
                "• 💳 To‘lov ulangan bot (Click/Payme)\n"
                "• 📊 Admin panel + statistika\n"
                "• 🤖 Avto javob (FAQ) bot\n"
                "• 🔐 Obuna tekshiruvchi bot\n"
            ),
            "ru": (
                "🚀 Создаем Telegram-боты любой сложности за 1–5 дней!\n\n"
                "Например:\n"
                "• 🛒 Торговый бот (каталог + заказ)\n"
                "• 📦 Бот приема заказов\n"
                "• 🎓 Бот для учебных центров\n"
                "• 💳 Подключение оплаты (Click/Payme)\n"
                "• 📊 Админ панель + статистика\n"
                "• 🤖 FAQ / автоответчик\n"
                "• 🔐 Проверка подписки\n"
            ),
            "en": (
                "🚀 We create Telegram bots of any complexity in 1–5 days!\n\n"
                "For example:\n"
                "• 🛒 Shop bot (catalog + orders)\n"
                "• 📦 Order bot\n"
                "• 🎓 Course/registration bot\n"
                "• 💳 Payment integration (Click/Payme)\n"
                "• 📊 Admin panel + stats\n"
                "• 🤖 FAQ / auto-reply bot\n"
                "• 🔐 Subscription checker bot\n"
            ),
        }
    }
    return texts[key].get(lang, texts[key]["uz"])


# =====================
# KEYBOARDS
# =====================
def lang_inline():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🇺🇿 O‘zbek", callback_data="lang_uz")],
        [InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang_ru")],
        [InlineKeyboardButton(text="🇬🇧 English", callback_data="lang_en")],
    ])

def main_reply(lang: str):
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=t(lang, "btn_contact")), KeyboardButton(text=t(lang, "btn_instagram"))],
            [KeyboardButton(text=t(lang, "btn_services")), KeyboardButton(text=t(lang, "btn_change_lang"))],
        ],
        resize_keyboard=True
    )

def contact_reply(lang: str):
    # pastdagi panel ichida bo'lim bo'lib turadi
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="💬 Telegram"), KeyboardButton(text="📸 Instagram")],
            [KeyboardButton(text="📞 Telefon")],
            [KeyboardButton(text=t(lang, "btn_back"))],
        ],
        resize_keyboard=True
    )

def services_reply(lang: str):
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=t(lang, "btn_back"))]],
        resize_keyboard=True
    )

# =====================
# START
# =====================
@dp.message(CommandStart())
async def start(message: Message):
    lang = user_lang.get(message.from_user.id)
    if not lang:
        await message.answer(t("uz", "choose_lang"), reply_markup=lang_inline())
        return
    await message.answer(t(lang, "menu"), reply_markup=main_reply(lang))

# =====================
# LANGUAGE SET
# =====================
@dp.callback_query(F.data.startswith("lang_"))
async def set_language(cb: CallbackQuery):
    lang = cb.data.split("_")[1]
    user_lang[cb.from_user.id] = lang

    # til tanlash xabarini o'zini qoldiramiz, faqat tugmalarini olib tashlaymiz
    try:
        await cb.message.edit_reply_markup(reply_markup=None)
    except:
        pass

    # pastga "panel" menyu chiqadi
    await cb.message.answer(t(lang, "menu"), reply_markup=main_reply(lang))
    await cb.answer()

# =====================
# MAIN MENU HANDLERS (Reply keyboard)
# =====================
@dp.message(F.text.in_(["📩 Bog‘lanish", "📩 Связаться", "📩 Contact"]))
async def open_contact(message: Message):
    lang = user_lang.get(message.from_user.id, "uz")
    await message.answer(t(lang, "contact_title"), reply_markup=contact_reply(lang))

@dp.message(F.text.in_(["📸 Instagram", "📸 Instagram"]))
async def instagram(message: Message):
    lang = user_lang.get(message.from_user.id, "uz")
    # reply button url ochmaydi, shuning uchun link yuboramiz
    await message.answer(t(lang, "instagram_msg"))

@dp.message(F.text.in_(["🤖 Xizmatlar", "🤖 Услуги", "🤖 Services"]))
async def open_services(message: Message):
    lang = user_lang.get(message.from_user.id, "uz")
    await message.answer(t(lang, "services_text"), reply_markup=services_reply(lang))

@dp.message(F.text.in_(["🌐 Tilni o‘zgartirish", "🌐 Сменить язык", "🌐 Change language"]))
async def change_lang(message: Message):
    # tilni qayta tanlatamiz (inline)
    await message.answer(t("uz", "choose_lang"), reply_markup=lang_inline())

@dp.message(F.text.in_(["⬅️ Ortga", "⬅️ Назад", "⬅️ Back"]))
async def back(message: Message):
    lang = user_lang.get(message.from_user.id, "uz")
    await message.answer(t(lang, "menu"), reply_markup=main_reply(lang))

# =====================
# CONTACT SUBMENU (Reply keyboard)
# =====================
@dp.message(F.text == "💬 Telegram")
async def contact_tg(message: Message):
    lang = user_lang.get(message.from_user.id, "uz")
    await message.answer(t(lang, "tg_msg"))

@dp.message(F.text == "📞 Telefon")
async def contact_phone(message: Message):
    lang = user_lang.get(message.from_user.id, "uz")
    await message.answer(t(lang, "phone"))

# =====================
# RUN
# =====================
async def main():
    print("Bot ishga tushdi...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
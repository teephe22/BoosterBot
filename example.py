from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import WebAppInfo

TOKEN = "8088335390:AAGFgeqTIdMOHuUCmaWYFK6SvNBoGLtw_Cg"

bot = Bot(TOKEN, parse_mode="HTML")
dp = Dispatcher(bot)

# Store verified IPs and which user owns them
registered_ips = {}   # { "ip": user_id }
registered_users = {} # { user_id: "ip" }


# /start command → sends button with WebApp
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    markup = types.ReplyKeyboardMarkup(
        keyboard=[
            [
                types.KeyboardButton(
                    text='✅ Verification',
                    web_app=WebAppInfo(url='https://7mile0n.github.io/verify/')
                )
            ]
        ],
        resize_keyboard=True
    )
    await message.answer(
        "<b>To register in the bot, go through verification, it will take up to 5 seconds</b>",
        reply_markup=markup
    )


# Handler for WebApp data (when user clicks main button inside WebApp)
@dp.message_handler(content_types=types.ContentType.WEB_APP_DATA)
async def web_app_data(message: types.Message):
    user_id = message.from_user.id
    ip = message.web_app_data.data.strip()   # the IP address from tg.sendData(userip)

    # Debug log
    print(f"User {user_id} sent IP: {ip}")

    # 1. If user is already registered
    if user_id in registered_users:
        await message.answer("⚠️ You are already registered with IP "
                             f"<code>{registered_users[user_id]}</code>.")
        return

    # 2. If IP is already used by another user
    if ip in registered_ips and registered_ips[ip] != user_id:
        await message.answer("🚫 This IP is already registered by another account.\n"
                             "Multiple accounts are not allowed.")
        return

    # 3. Otherwise → save registration
    registered_ips[ip] = user_id
    registered_users[user_id] = ip

    await message.answer(f"🌐 Your IP: <code>{ip}</code>",
                         reply_markup=types.ReplyKeyboardRemove())
    await message.answer("✅ You have been successfully registered!")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)

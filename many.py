import os
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

# TOKENNI BU YERGA YOZ
BOT_TOKEN = "8200840668:AAFAcLUyzg4ltoaZT0Bs2KvoAJNgaN3GSIA"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("📦 Modlar")
    await message.answer(
        "Salom! Minecraft Bedrock modlarini olish uchun tugmani bosing 👇",
        reply_markup=keyboard
    )

@dp.message_handler(lambda msg: msg.text == "📦 Modlar")
async def send_mods(message: types.Message):
    mods_dir = "mods"

    if not os.path.exists(mods_dir):
        await message.answer("❌ Hozircha modlar yo‘q.")
        return

    files = os.listdir(mods_dir)

    if not files:
        await message.answer("❌ mods papkasi bo‘sh.")
        return

    await message.answer("📤 Modlar yuborilmoqda...")

    for file in files:
        path = os.path.join(mods_dir, file)
        try:
            await message.answer_document(open(path, "rb"))
        except:
            await message.answer(f"❌ {file} yuborilmadi.")

if __name__ == "__main__":
    executor.start_polling(dp)

import logging
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

# Bot tokeni
BOT_TOKEN = "8200840668:AAFAcLUyzg4ltoaZT0Bs2KvoAJNgaN3GSIA"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

logging.basicConfig(level=logging.INFO)

# Modlar ro‘yxati
mods = {
    "Crumble REMAKE": "mods/Crumble_REMAKE.mcaddon",
    "Family": "mods/family.mcaddon",
    "Fizik narsalar": "mods/fizik_narsalar.mcaddon",
    "O‘yinchilar uchun qiziq mod": "mods/qiziq_mod.mcaddon"
}

# /start buyrug‘i
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    text = "Salom! 😊 Minecraft modlarini olish uchun pastdan birini tanlang:"
    
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for mod_name in mods.keys():
        keyboard.add(mod_name)

    await message.answer(text, reply_markup=keyboard)

# Mod nomlarini qayta ishlash
@dp.message_handler()
async def send_mod(message: types.Message):
    mod_name = message.text

    if mod_name in mods:
        file_path = mods[mod_name]
        try:
            await message.answer_document(open(file_path, 'rb'))
        except:
            await message.answer("❌ Fayl topilmadi. GitHub ichida *mods* papkasini tekshiring.")
    else:
        await message.answer("Bunday mod yo‘q. Iltimos menyudan tanlang.")

# Botni ishga tushurish
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

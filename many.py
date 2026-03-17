import telebot
import yt_dlp
import os

# BotFather'dan olgan tokenni SHU YERGA qo'ying
TOKEN = '8542620824:AAF6CjdWm5oJqTKxW7xsuWBJ9WO1qkHiLpI'
bot = telebot.TeleBot(TOKEN)

def download_audio(query):
    # Musiqani qidirish va yuklash sozlamalari
    ydl_opts = {
        'format': 'bestaudio/best',
        'noplaylist': True,
        'default_search': 'ytsearch',
        'outtmpl': 'song.mp3',
        'quiet': True
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([query])

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Salom Islom! Qaysi musiqani topib beray? Ismini yozing. 💎")

@bot.message_handler(func=lambda m: True)
def search(message):
    msg = bot.send_message(message.chat.id, "🔍 Qidiryapman, kuting...")
    try:
        # Qidirish va yuklash
        download_audio(message.text)
        
        # Musiqani yuborish
        with open('song.mp3', 'rb') as audio:
            bot.send_audio(message.chat.id, audio, caption=f"✅ {message.text} topildi!")
        
        # RAM to'lib qolmasligi uchun faylni o'chirish
        if os.path.exists("song.mp3"):
            os.remove("song.mp3")
        bot.delete_message(message.chat.id, msg.message_id)

    except Exception as e:
        bot.edit_message_text(f"❌ Xatolik: {e}", message.chat.id, msg.message_id)

print("Bot ishlashga tayyor!")
bot.infinity_polling()

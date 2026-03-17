import telebot
import yt_dlp
import os

# Bot tokeningizni kiriting
TOKEN = '8542620824:AAF6CjdWm5oJqTKxW7xsuWBJ9WO1qkHiLpI'
bot = telebot.TeleBot(TOKEN)

# Musiqa qidirish funksiyasi
def download_music(query):
    ydl_opts = {
        'format': 'bestaudio/best',
        'noplaylist': True,
        'default_search': 'ytsearch',
        'outtmpl': 'music.mp3',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([query])

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Salom Islom! Musiqa nomini yozing, men uni topib beraman.")

@bot.message_handler(func=lambda m: True)
def search_and_send(message):
    msg = bot.send_message(message.chat.id, "Qidiryapman, kuting...")
    try:
        download_music(message.text)
        with open('music.mp3', 'rb') as audio:
            bot.send_audio(message.chat.id, audio)
        os.remove('music.mp3') # Faylni yuborgach o'chirib tashlaymiz
        bot.delete_message(message.chat.id, msg.message_id)
    except Exception as e:
        bot.edit_message_text(f"Xatolik yuz berdi: {e}", message.chat.id, msg.message_id)

print("Bot ishga tushdi...")
bot.infinity_polling()

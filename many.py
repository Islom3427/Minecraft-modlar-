import telebot
import yt_dlp
import os
import time
from flask import Flask
from threading import Thread

# 1. RENDER UCHUN "ALDOVCHI" SAYT QISMI
app = Flask('')

@app.route('/')
def home():
    return "Bot 24/7 holatda ishlamoqda!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# 2. BOTNING ASOSIY QISMI
TOKEN = "8542620824:AAF6CjdWm5oJqTKxW7xsuWBJ9WO1qkHiLpI"
bot = telebot.TeleBot(TOKEN)

def download_audio(url):
    file_name = f"music_{int(time.time())}"
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'{file_name}.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320',
        }],
        'quiet': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    return f"{file_name}.mp3"

@bot.message_handler(commands=['start'])
def start_cmd(message):
    bot.send_message(message.chat.id, "🌟 **Bot 24/7 rejimida yoniq!**\nYouTube linkini yuboring.")

@bot.message_handler(func=lambda m: "youtube.com" in m.text or "youtu.be" in m.text)
def handle_yt(message):
    status = bot.reply_to(message, "📥 **Ishlanmoqda...**")
    try:
        file_path = download_audio(message.text)
        with open(file_path, 'rb') as audio:
            bot.send_audio(message.chat.id, audio, caption="✅ @All_Music_uzb_bot")
        os.remove(file_path)
        bot.delete_message(message.chat.id, status.message_id)
    except Exception as e:
        bot.edit_message_text(f"❌ Xato!", message.chat.id, status.message_id)

# 3. ISHGA TUSHIRISH
if __name__ == "__main__":
    keep_alive() # Serverni yoqadi
    print("⚡️ BOT RENDERDA TIRILDI!")
    bot.infinity_polling()
    

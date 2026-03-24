import os
import telebot
from flask import Flask
import yt_dlp
import threading

# 1. BOT SOZLAMALARI
TOKEN = '8542620824:AAF6CjdWm5oJqTKxW7xsuWBJ9WO1qkHiLpI'
bot = telebot.TeleBot(TOKEN)
server = Flask(__name__)

# Render o'chib qolmasligi uchun kichik sahifa
@server.route("/")
def index():
    return "Bot Render-da muvaffaqiyatli ishlayapti!", 200

# 2. BOT BUYRUQLARI
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Salom Islom! Botingiz Render-da yondi! 🎵\nMusiqa nomini yozing:")

@bot.message_handler(func=lambda m: True)
def handle(message):
    try:
        msg = bot.send_message(message.chat.id, "🔍 Qidirilmoqda...")
        out_file = '/tmp/musiqa.mp3'
        ydl_opts = {
            'format': 'bestaudio/best',
            'default_search': 'ytsearch',
            'outtmpl': out_file,
            'quiet': True,
            'no_warnings': True
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([message.text])
        
        with open(out_file, 'rb') as audio:
            bot.send_audio(message.chat.id, audio, caption="Tayyor! ✅ @islombek2437mc")
        
        if os.path.exists(out_file):
            os.remove(out_file)
        bot.delete_message(message.chat.id, msg.message_id)
    except Exception as e:
        bot.reply_to(message, f"Xato: {str(e)[:100]}")

# 3. BOTNI ISHGA TUSHIRISH
def run_bot():
    bot.infinity_polling()

if __name__ == "__main__":
    # Botni orqa fonda (threading) yurgizamiz
    threading.Thread(target=run_bot).start()
    # Render portini avtomatik aniqlash
    port = int(os.environ.get("PORT", 5000))
    server.run(host='0.0.0.0', port=port)
    

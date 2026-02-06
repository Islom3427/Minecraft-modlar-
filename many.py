import telebot
import yt_dlp
import os
from youtube_search import YoutubeSearch

# Bot tokeningizni shu yerga yozing
TOKEN = 'BOT_TOKENINGIZNI_SHU_YERGA_YOZING'
bot = telebot.TeleBot(TOKEN)

# Musiqa qidirish funksiyasi
def search_youtube(query):
    try:
        results = YoutubeSearch(query, max_results=1).to_dict()
        if results:
            return "https://www.youtube.com" + results[0]['url_suffix']
        return None
    except:
        return None

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Salom! Musiqa nomini yozing yoki YouTube havolasini yuboring. 🎵")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    text = message.text
    chat_id = message.chat.id
    
    # Agar foydalanuvchi link yuborsa o'sha linkni oladi, aks holda qidiradi
    if "youtube.com" in text or "youtu.be" in text:
        url = text
    else:
        status_msg = bot.send_message(chat_id, "🔍 Qidirilmoqda...")
        url = search_youtube(text)
        bot.delete_message(chat_id, status_msg.message_id)

    if not url:
        bot.send_message(chat_id, "❌ Musiqa topilmadi.")
        return

    processing_msg = bot.send_message(chat_id, "📥 Musiqa tayyorlanmoqda, iltimos kuting...")

    # Yuklab olish sozlamalari
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info).replace('.webm', '.mp3').replace('.m4a', '.mp3')
        
        with open(filename, 'rb') as audio:
            bot.send_audio(chat_id, audio, caption="✅ @SizningBotNomingiz orqali yuklab olindi")
        
        # Faylni o'chirish (serverda joy qolishi uchun)
        os.remove(filename)
        bot.delete_message(chat_id, processing_msg.message_id)

    except Exception as e:
        bot.edit_message_text(f"❌ Yuklashda xato: YouTube cheklovi yoki xato yuz berdi.", chat_id, processing_msg.message_id)
        print(f"Xato: {e}")

bot.polling(none_stop=True)

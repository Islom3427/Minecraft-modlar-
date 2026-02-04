import telebot, os, requests, yt_dlp
from youtube_search import YoutubeSearch
from telebot import types

# ⚙️ SOZLAMALAR
TOKEN = "8542620824:AAF6CjdWm5oJqTKxW7xsuWBJ9WO1qkHiLpI"
bot = telebot.TeleBot(TOKEN)

def get_opts():
    return {
        'format': 'bestaudio/best',
        'postprocessors': [{'key': 'FFmpegExtractAudio','preferredcodec': 'mp3','preferredquality': '192'}],
        'quiet': True, 'no_warnings': True,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/122.0.0.0'
    }

def download_audio(url, chat_id, msg_id):
    bot.edit_message_text("⏳ Yuklanmoqda...", chat_id, msg_id)
    try:
        with yt_dlp.YoutubeDL(get_opts()) as ydl:
            info = ydl.extract_info(url, download=True)
            title = info.get('title', 'Musiqa').replace('/', '_')
            perf = info.get('uploader', 'Artist')
            file = ydl.prepare_filename(info).rsplit('.', 1)[0] + ".mp3"
            
            with open(file, 'rb') as audio:
                bot.send_audio(chat_id, audio, title=title, performer=perf)
            
            bot.delete_message(chat_id, msg_id)
            if os.path.exists(file): os.remove(file)
    except Exception as e:
        bot.edit_message_text(f"❌ Xato: {str(e)[:50]}", chat_id, msg_id)

@bot.message_handler(commands=['start'])
def start(m):
    bot.send_message(m.chat.id, "Salom! Musiqa nomini yoki YouTube linkini yuboring.")

@bot.message_handler(func=lambda m: True)
def handle(m):
    if "youtube.com" in m.text or "youtu.be" in m.text:
        st = bot.reply_to(m, "🔗 Tahlil...")
        download_audio(m.text, m.chat.id, st.message_id)
    else:
        st = bot.reply_to(m, "🔎 Qidiruv...")
        res = YoutubeSearch(m.text, max_results=10).to_dict()
        if not res: return bot.edit_message_text("Topilmadi.", m.chat.id, st.message_id)
        
        txt = "Natijalar:\n\n"
        kb = types.InlineKeyboardMarkup(row_width=5)
        btns = [types.InlineKeyboardButton(text=str(i), callback_data=f"dl_{r['id']}") for i, r in enumerate(res, 1)]
        for i, r in enumerate(res, 1): txt += f"{i}. {r['title']}\n"
        kb.add(*btns)
        bot.edit_message_text(txt, m.chat.id, st.message_id, reply_markup=kb)

@bot.callback_query_handler(func=lambda call: call.data.startswith('dl_'))
def call_dl(c):
    url = f"https://www.youtube.com/watch?v={c.data.split('_')[1]}"
    bot.answer_callback_query(c.id, "Yuklash...")
    download_audio(url, c.message.chat.id, c.message.message_id)

if __name__ == "__main__":
    bot.infinity_polling()
    

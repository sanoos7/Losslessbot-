import telebot
import os
import librosa
import numpy as np

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

# 🔍 PRO ANALYSIS FUNCTION
def analyze_audio(file_path):
    y, sr = librosa.load(file_path)

    # Frequency analysis
    spectrum = np.abs(np.fft.rfft(y))
    freqs = np.fft.rfftfreq(len(y), 1/sr)

    max_freq = freqs[np.argmax(spectrum)]

    # Heuristic detection
    if max_freq > 20000:
        return "✅ TRUE LOSSLESS\n🎯 Full frequency spectrum detected"
    elif max_freq < 16000:
        return "❌ LOSSY FILE\n📉 Frequency cutoff detected (~16kHz)"
    else:
        return "⚠️ FAKE LOSSLESS\n🔍 Upscaled from lossy source"

# ▶ START
@bot.message_handler(commands=['start'])
def start(msg):
    bot.reply_to(msg, "🎧 PRO Audio Analyzer\n\nSend audio file")

# 📥 HANDLE FILE
@bot.message_handler(content_types=['audio', 'document'])
def handle_file(msg):
    file_info = bot.get_file(msg.document.file_id if msg.document else msg.audio.file_id)
    downloaded = bot.download_file(file_info.file_path)

    with open("audio", "wb") as f:
        f.write(downloaded)

    bot.reply_to(msg, "🔍 Analyzing...")

    result = analyze_audio("audio")

    bot.reply_to(msg, result)

print("Bot running...")
bot.infinity_polling()

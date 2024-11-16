import os
import telebot
import requests
from yt_dlp import YoutubeDL

# Get bot token from environment variable
BOT_TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Hello! Send me a YouTube link, and I'll download it for you.")

@bot.message_handler(func=lambda message: 'youtube.com' in message.text or 'youtu.be' in message.text)
def handle_youtube_link(message):
    try:
        youtube_url = message.text.strip()
        chat_id = message.chat.id
        
        # Send processing message
        bot.reply_to(message, "Processing your request... Please wait.")
        
        # Download video using yt-dlp
        ydl_opts = {
            'format': 'best[filesize<50M]',  # Limit filesize to 50MB (Telegram's limit)
            'outtmpl': 'downloaded_video.%(ext)s'
        }
        
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(youtube_url, download=True)
            video_file = ydl.prepare_filename(info)
        
        # Send video file
        with open(video_file, 'rb') as video:
            bot.send_video(chat_id, video)
        
        # Clean up
        os.remove(video_file)
        
    except Exception as e:
        bot.reply_to(message, f"Sorry, an error occurred: {str(e)}")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, "Please send a valid YouTube link.")

if __name__ == "__main__":
    bot.polling()

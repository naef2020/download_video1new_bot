
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import yt_dlp
import os

# مسار لحفظ الفيديوهات
DOWNLOAD_PATH = "downloads"

# دالة لتحميل الفيديو
def download_video(url: str):
    ydl_opts = {
        'outtmpl': f'{DOWNLOAD_PATH}/%(title)s.%(ext)s',
        'format': 'bestvideo+bestaudio/best',
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return ydl.prepare_filename(info)

# أمر /start
def start(update: Update, context: CallbackContext):
    update.message.reply_text("أهلاً! أرسل لي رابط الفيديو لتحميله.")

# التعامل مع الروابط
def handle_message(update: Update, context: CallbackContext):
    url = update.message.text
    try:
        update.message.reply_text("جارِ تحميل الفيديو...")
        file_path = download_video(url)
        update.message.reply_video(video=open(file_path, 'rb'))
        os.remove(file_path)  # حذف الفيديو بعد الإرسال
    except Exception as e:
        update.message.reply_text(f"حدث خطأ أثناء التحميل: {e}")

def main():
    TOKEN = "6963116644:AAH0l1GAQ3S6qHhWNkXXINLZY8UaCYmJ3i8"  # استبدل هذا بالتوكن الخاص بك من BotFather
    updater = Updater(TOKEN, use_context=True)

    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    if not os.path.exists(DOWNLOAD_PATH):
        os.makedirs(DOWNLOAD_PATH)
    main()

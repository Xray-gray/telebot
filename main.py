import os
import random
import logging
from flask import Flask, request
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from telegram.ext import CallbackContext

TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
VIDEO_FOLDER = 'videos/barev/'

# Настройка логирования
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
bot = Bot(token=TOKEN)
application = Application.builder().token(TOKEN).build()

async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Բարև, ես Ջարվիս բոտն եմ, ով բարևում է բոլոր նոր մասնակիցներին :)')

async def new_member(update: Update, context: CallbackContext) -> None:
    if update.message.new_chat_members:
        for member in update.message.new_chat_members:
            logging.info(f"New member detected: {member.full_name}")
            await update.message.reply_text(f'Բարի գալուստ, {member.full_name}!')

            video_file = random.choice(os.listdir(VIDEO_FOLDER))
            video_path = os.path.join(VIDEO_FOLDER, video_file)
            logging.info(f"Selected video: {video_file}")

            try:
                with open(video_path, 'rb') as video:
                    await context.bot.send_video(chat_id=update.message.chat_id, video=video)
            except Exception as e:
                logging.error(f"Error sending video: {str(e)}")
                await update.message.reply_text(f'Վիդեոն ուրիշ անգամ: {str(e)}')

@app.route('/' + TOKEN, methods=['POST'])
def webhook():
    json_str = request.get_data(as_text=True)
    update = Update.de_json(json_str, bot)
    application.process_update(update)
    return 'OK'

def set_webhook():
    webhook_url = f"https://your-render-url.com/{TOKEN}"
    bot.set_webhook(url=webhook_url)

if __name__ == '__main__':
    set_webhook()
    app.run(host='0.0.0.0', port=80)

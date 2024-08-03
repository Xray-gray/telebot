import os
import random
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from telegram.ext import CallbackContext

TOKEN = os.getenv('7476413517:AAFfOQzIfWIRKLif2zcAsEPMNHzmwORTO6Y')  # Fetch token from environment variable
VIDEO_FOLDER = 'videos/barev/'

# Настройка логирования
logging.basicConfig(level=logging.INFO)


async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Բարև, ես բոտ եմ, ով բարևում է բոլոր նոր մասնակիցներին :)')


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
                await update.message.reply_text(f'Произошла ошибка при отправке видео: {str(e)}')


def main():
    token = os.getenv('7476413517:AAFfOQzIfWIRKLif2zcAsEPMNHzmwORTO6Y')
    if not token:
        raise ValueError("No TELEGRAM_BOT_TOKEN environment variable set")

    application = Application.builder().token(token).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, new_member))

    application.run_polling()  # Here, `await` is not needed


if __name__ == '__main__':
    main()

import os
import random
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, filters
from telegram.ext import CallbackContext

TOKEN = '7476413517:AAFfOQzIfWIRKLif2zcAsEPMNHzmwORTO6Y'
VIDEO_FOLDER = 'videos/barev/'


def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Բարև, ես բոտ եմ, ով բարևում է բոլոր նոր մասնակիցներին:)')


def new_member(update: Update, context: CallbackContext) -> None:
    for member in update.message.new_chat_members:
        update.message.reply_text(f'Բարի գալուստ, {member.full_name}!')

        try:
            video_file = random.choice(os.listdir(VIDEO_FOLDER))
            video_path = os.path.join(VIDEO_FOLDER, video_file)

            with open(video_path, 'rb') as video:
                context.bot.send_video(chat_id=update.message.chat_id, video=video)
        except Exception as e:
            print(f"Error sending video: {e}")


def main():
    updater = Updater(TOKEN)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.status_update.new_chat_members, new_member))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()

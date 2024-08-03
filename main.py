import os
import random
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from telegram.ext import CallbackContext

TOKEN = '7476413517:AAFfOQzIfWIRKLif2zcAsEPMNHzmwORTO6Y'  # Use a new token if needed
VIDEO_FOLDER = 'videos/barev/'

async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Բարև, ես բոտ եմ, ով բարևում է բոլոր նոր մասնակիցներին :)')

async def new_member(update: Update, context: CallbackContext) -> None:
    for member in update.message.new_chat_members:
        await update.message.reply_text(f'Բարի գալուստ, {member.full_name}!')
        video_file = random.choice(os.listdir(VIDEO_FOLDER))
        video_path = os.path.join(VIDEO_FOLDER, video_file)
        with open(video_path, 'rb') as video:
            await context.bot.send_video(chat_id=update.message.chat_id, video=video)

async def main():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, new_member))
    await application.run_polling()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())

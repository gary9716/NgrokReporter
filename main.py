# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import configparser

# 建立 ConfigParser
config = configparser.ConfigParser()
config.read('config.ini')
TOKEN = config['bot']['token']

import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

def addHandler(application, tag, handler):
    cmdHandler = CommandHandler(tag, handler)
    application.add_handler(cmdHandler)

if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()

    addHandler(application, 'start', start)

    application.run_polling()
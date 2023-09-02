# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import configparser
import subprocess
import time
import signal
import requests

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

ngrok = config['ngrok']['path']
port = config['ngrok']['port']
protocol = config['ngrok']['protocol']
auth = config['ngrok']['auth']
apiToken = config['ngrok']['api-token']
curProc = None
application = None

def handler(signum, frame):
    global curProc
    if curProc:
        curProc.terminate()
        curProc = None
    exit(1)
signal.signal(signal.SIGINT, handler)

def queryTunnelsInfo():
    url = 'https://api.ngrok.com/tunnels'
    headers = {
        'Authorization': f'Bearer {apiToken}',
        'Ngrok-Version': '2'
    }
    response = requests.get(
        url,
        headers=headers,
        timeout=5
    )
    return str(response.json())

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cmd = update.message.text #one can parse arguments from cmd
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text="I'm a ngrok reporter, you can start ngrok with /boot, dump tunnels info with /tunnels")

async def reportTunnels(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text=queryTunnelsInfo())

async def boot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global curProc
    if curProc:
        curProc.kill()
    curProc = subprocess.Popen([ngrok, "authtoken", auth],
                               stdout=subprocess.DEVNULL,
                               stderr=subprocess.STDOUT)
    curProc.wait()
    curProc = subprocess.Popen([ngrok, protocol, port],
                               stdout=subprocess.DEVNULL,
                               stderr=subprocess.STDOUT,
                               text=True)
    time.sleep(1)
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text='ngrok boot')

async def shutDown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text='ok, time to shutdown')
    global curProc
    if curProc:
        curProc.kill()
        curProc = None

def addHandler(application, tag, handler):
    cmdHandler = CommandHandler(tag, handler)
    application.add_handler(cmdHandler)

if __name__ == '__main__':
    try:
        application = ApplicationBuilder().token(TOKEN).build()

        addHandler(application, 'start', start)
        addHandler(application, 'boot', boot)
        addHandler(application, 'tunnels', reportTunnels)
        addHandler(application, 'shutdown', shutDown)

        application.run_polling()
    finally:
        if curProc:
            curProc.kill()
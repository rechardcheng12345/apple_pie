import os
import telebot
from bitfinnex_active_funding import main as active_funding
from bitfinnex_order_status import main as order_status
from bitfinnex_funding_credit import main as check_wallet
from bitfinnex_ledger_history import main as ledger_history

from dotenv import load_dotenv
load_dotenv()

BOT_TOKEN = os.environ.get('BOT_TOKEN')

bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=['active_funding'])
def send_welcome(message):
    bot.reply_to(message, active_funding())


@bot.message_handler(commands=['funding_order'])
def send_welcome(message):
    bot.reply_to(message, order_status())


@bot.message_handler(commands=['ledger_history'])
def send_welcome(message):
    bot.reply_to(message, ledger_history())


@bot.message_handler(commands=['check_wallet'])
def send_welcome(message):
    bot.reply_to(message, check_wallet())


bot.infinity_polling()


# active_funding-Current Funding List
# funding_order-Check Funding Order
# ledger_history-Check Ledger History
# check_wallet-Check Wallet

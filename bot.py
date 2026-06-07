
import telebot
from telebot import types
import json
import os

TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

DATA_FILE = "users.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

@bot.message_handler(commands=['start'])
def start(message):
    data = load_data()
    user_id = str(message.from_user.id)

    if user_id not in data:
        data[user_id] = {
            "balance": 0,
            "referrals": 0
        }

        args = message.text.split()
        if len(args) > 1:
            referrer = args[1].replace("ref_", "")
            if referrer in data and referrer != user_id:
                data[referrer]["balance"] += 10
                data[referrer]["referrals"] += 1

        save_data(data)

    referral_link = f"https://t.me/Btjcdgjbot?start=ref_{user_id}"

    bot.reply_to(
        message,
        f"Welcome!\n\nBalance: ₹{data[user_id]['balance']}\nReferrals: {data[user_id]['referrals']}\n\nYour Referral Link:\n{referral_link}"
    )

bot.infinity_polling()

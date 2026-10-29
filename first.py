import os
import json
import telebot
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(TOKEN)

FILE = "data.json"

def load_data():
    if not os.path.exists(FILE):
        return {"players": {}}

    with open(FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data):
    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, "Привет! Как тебя зовут?")
    bot.register_next_step_handler(message, ask_car)

def ask_car(message):
    if not message.text:
        bot.send_message(message.chat.id, "Напиши своё имя текстом.")
        bot.register_next_step_handler(message, ask_car)
        return

    name = message.text.strip()
    bot.send_message(
        message.chat.id,
        f"Приятно познакомиться, {name}! 🚗\n"
        "Какая твоя любимая машина?"
    )
    bot.register_next_step_handler(message, save_profile, name)

def save_profile(message, name):
    if not message.text:
        bot.send_message(message.chat.id, "Напиши название машины текстом.")
        bot.register_next_step_handler(message, save_profile, name)
        return

    car = message.text.strip()

    data = load_data()
    data["players"][str(message.from_user.id)] = {
        "name": name,
        "favorite_car": car
    }
    save_data(data)

    bot.send_message(
        message.chat.id,
        f"✅ Всё сохранено!\n\n"
        f"👤 Имя: {name}\n"
        f"🏎 Любимая машина: {car}\n\n"
        "Напиши /profile, чтобы посмотреть анкету."
    )

@bot.message_handler(commands=["profile"])
def profile(message):
    data = load_data()
    player = data["players"].get(str(message.from_user.id))

    if player:
        bot.send_message(
            message.chat.id,
            f"👤 Имя: {player['name']}\n"
            f"🏎 Любимая машина: {player['favorite_car']}"
        )
    else:
        bot.send_message(message.chat.id, "Сначала напиши /start")

bot.infinity_polling()
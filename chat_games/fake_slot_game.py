import random
from datetime import datetime
from telegram import Update
from telegram.ext import ContextTypes
import os
import json
import shlex

EMOJIS = ["🍒", "🍋", "🔔", "🍉", "⭐", "🍇", "💎", "🍀", "🍎", "🍊", "🍌", "7️⃣"]

# game data 
DATA_DIR = "data"
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

SLOTS_DATA_FILE = os.path.join(DATA_DIR, "slots_data.json")

try:
    with open(SLOTS_DATA_FILE, "r", encoding="utf-8") as f:
        fake_slot_game_data = json.load(f)
except FileNotFoundError:
    fake_slot_game_data = {}

def spin_slot():
    while True:
        # random 3 smiles
        result = [random.choice(EMOJIS) for _ in range(3)]
        # no jackpot
        if result == ["7️⃣", "7️⃣", "7️⃣"]:
            continue
        return result

def save_slots_data():
    with open(SLOTS_DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(fake_slot_game_data, f, ensure_ascii=False, indent=2)

async def slot_custom(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = str(update.effective_chat.id)
    user_id = str(update.effective_user.id)

    try:
        args = shlex.split(update.message.text)
    except Exception:
        await update.message.reply_text("❗ Помилка парсингу аргументів. Використовуй лапки для назв з пробілами.")
        return

    if len(args) < 3:
        await update.message.reply_text(
            '❗ Використання:\n/slot @username "назва гри"\n'
            'Назва гри може містити пробіли, якщо її взято в лапки.'
        )
        return

    target_username = args[1]
    game_name = args[2]

    if not target_username.startswith("@"):
        await update.message.reply_text("❗ Перший аргумент повинен бути username починаючи з @, наприклад @ivan.")
        return

    if chat_id not in fake_slot_game_data:
        fake_slot_game_data[chat_id] = {}

    user_data = fake_slot_game_data[chat_id].get(user_id, {"date": "", "count": 0})
    today = datetime.now().strftime("%Y-%m-%d")

    if user_data["date"] != today:
        user_data = {"date": today, "count": 0}

    if user_data["count"] >= 3:
        await update.message.reply_text("⛔ Вибач, але ти вже використав усі 3 спроби на сьогодні.")
        return

    result = spin_slot()
    result_str = "".join(result)

    user_data["count"] += 1
    user_data["date"] = today
    fake_slot_game_data[chat_id][user_id] = user_data
    save_slots_data()

    if len(set(result)) == 1 and result[0] != "7️⃣":
        text = f"🎰 [{game_name}] Випало: {result_str}\nНажаль, виграшних комбінацій немає. Спробуй ще!"
    else:
        text = f"🎰 [{game_name}] Випало: {result_str}\nСпробуй виграти джекпот!"

    text += f"\n🎁 Користувач {target_username} не подарує тобі {game_name} :("

    await update.message.reply_text(text)
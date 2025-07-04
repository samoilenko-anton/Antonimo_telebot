import json
import random
from datetime import datetime
from telegram import Update
from telegram.ext import ContextTypes
import os

from predefined_lists.legendary_item_list import legendary_items
from predefined_lists.rare_item_list import rare_items
from predefined_lists.common_item_list import common_items
from predefined_lists.trash_item_list import trash_items

loot_items = {
    "legendary": legendary_items,
    "rare": rare_items,
    "common": common_items,
    "trash": trash_items,
}

DATA_DIR = "data"
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

LOOT_DATA_FILE = os.path.join(DATA_DIR, "loot_data.json")

# game data
try:
    with open(LOOT_DATA_FILE, "r", encoding="utf-8") as f:
        loot_data = json.load(f)
except FileNotFoundError:
    loot_data = {}
    
# save_loot
def save_loot():
    with open(LOOT_DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(loot_data, f, ensure_ascii=False, indent=2)

# /daily_loot
async def daily_loot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = str(update.effective_chat.id)
    user_id = str(update.effective_user.id)
    user_name = update.effective_user.first_name
    today = datetime.now().strftime("%Y-%m-%d")

    if chat_id not in loot_data:
        loot_data[chat_id] = {}

    user_data = loot_data[chat_id].get(user_id)
    if user_data and user_data.get("last_loot_date") == today:
        await update.message.reply_text("📦 Ти вже сьогодні відкривав лут! Завітай завтра.")
        return

    loot_types = [
        ("legendary", "🟡 Легендарний предмет"),
        ("rare", "🔵 Рідкісний предмет"),
        ("common", "⚪️ Звичайний предмет"),
        ("trash", "🟤 Сміття")
    ]
    weights = [1, 4, 8, 6]
    loot_key, loot_text = random.choices(loot_types, weights)[0]

    # rnd item
    item_name, item_desc = random.choice(loot_items[loot_key])

    if not user_data:
        user_data = {
            "name": user_name,
            "legendary": 0,
            "rare": 0,
            "common": 0,
            "trash": 0,
            "total_loots": 0,
            "last_loot_date": ""
        }

    user_data[loot_key] += 1
    user_data["total_loots"] += 1
    user_data["last_loot_date"] = today
    user_data["name"] = user_name

    loot_data[chat_id][user_id] = user_data
    save_loot()

    await update.message.reply_text(f"{loot_text}! 🎁 {item_name}\n🔹 {item_desc}")

# /loot_me
async def loot_me(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    user_name = update.effective_user.first_name

    data = loot_data.get(user_id)
    if not data:
        await update.message.reply_text(f"{user_name}, ти ще не відкривав лут. Спробуй /daily_loot")
        return

    await update.message.reply_text(
        f"📦 Колекція {data['name']}\n"
        f"🟡 Легендарні: {data['legendary']}\n"
        f"🔵 Рідкісні: {data['rare']}\n"
        f"⚪️ Звичайні: {data['common']}\n"
        f"🟤 Сміття: {data['trash']}\n"
        f"🔁 Всього відкрито: {data['total_loots']}"
    )

# /loot_top
async def loot_top(update: Update, context: ContextTypes.DEFAULT_TYPE):
    limit = 25
    if context.args:
        if context.args[0] == "10":
            limit = 10
        elif context.args[0] == "5":
            limit = 5

    ranking = sorted(
        [(d["name"], d["legendary"]) for d in loot_data.values()],
        key=lambda x: x[1],
        reverse=True
    )[:limit]

    if not ranking:
        await update.message.reply_text("📉 Ще ніхто не відкрив жодного луту.")
        return

    result = f"🏆 Топ-{limit} гравців за кількістю легендарних предметів:\n"
    for i, (name, count) in enumerate(ranking, 1):
        result += f"{i}. {name} — {count} легендарних\n"

    await update.message.reply_text(result)
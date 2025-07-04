import json
from telegram import Update
from telegram.ext import ContextTypes
import os

BAN_DATA_FILE = "data/ban_data.json"

# game data 
if not os.path.exists("data"):
    os.makedirs("data")

try:
    with open(BAN_DATA_FILE, "r", encoding="utf-8") as f:
        ban_data = json.load(f)
except FileNotFoundError:
    ban_data = {}

def save_ban_data():
    with open(BAN_DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(ban_data, f, ensure_ascii=False, indent=2)

async def ban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = str(update.effective_chat.id)

    # if not response to a message
    if not update.message.reply_to_message:
        await update.message.reply_text("❗ Будь ласка, використовуйте '/ban' як відповідь на повідомлення користувача.")
        return

    banned_user = update.message.reply_to_message.from_user
    user_identifier = str(banned_user.id)

    # Initialization for chat
    if chat_id not in ban_data:
        ban_data[chat_id] = {}

    # Initialization for user
    if user_identifier not in ban_data[chat_id]:
        ban_data[chat_id][user_identifier] = {
            "count": 0,
            "username": banned_user.username or banned_user.first_name
        }

    # counter
    ban_data[chat_id][user_identifier]["count"] += 1
    save_ban_data()

    await update.message.reply_text(
        f"🚫 Користувача @{ban_data[chat_id][user_identifier]['username']} забанено! "
        f"Всього банів: {ban_data[chat_id][user_identifier]['count']}"
    )

async def ban_top(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = str(update.effective_chat.id)

    if chat_id not in ban_data or len(ban_data[chat_id]) == 0:
        await update.message.reply_text("📉 Немає забанених користувачів у цьому чаті.")
        return

    limit = 10
    if context.args:
        try:
            limit = int(context.args[0])
        except ValueError:
            pass

    top_users = sorted(
        ban_data[chat_id].items(),
        key=lambda x: x[1]["count"],
        reverse=True
    )[:limit]

    text = f"🏆 Топ-{limit} забанених користувачів у цьому чаті:\n"
    for i, (user_id, info) in enumerate(top_users, 1):
        text += f"{i}. @{info['username']} — {info['count']} банів\n"

    await update.message.reply_text(text)
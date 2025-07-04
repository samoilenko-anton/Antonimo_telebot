import json
import random

# game data 
guess_game_data = {}

try:
    with open("data/guess_data.json", "r", encoding="utf-8") as f:
        guess_game_data = json.load(f)
        guess_game_data = {int(chat_id): {int(uid): data for uid, data in chat.items()} for chat_id, chat in guess_game_data.items()}
except FileNotFoundError:
    guess_game_data = {}

# guess game data (save)
def save_guess_data():
    with open("data/guess_data.json", "w", encoding="utf-8") as f:
        json.dump(guess_game_data, f, ensure_ascii=False, indent=2)

# /start_guess
async def start_guess(update, context):
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    user_name = update.effective_user.first_name

    if chat_id not in guess_game_data:
        guess_game_data[chat_id] = {}

    guess_game_data[chat_id][user_id] = {
        "number": random.randint(1, 100),
        "attempts": 0,
        "total_games": guess_game_data[chat_id].get(user_id, {}).get("total_games", 0),
        "total_attempts": guess_game_data[chat_id].get(user_id, {}).get("total_attempts", 0),
        "name": user_name
    }
    save_guess_data()
    await update.message.reply_text("🎯 Я загадав число від 1 до 100. Вгадай його через /guess <число>!")

# /guess <number>
async def guess(update, context):
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    user_name = update.effective_user.first_name

    if chat_id not in guess_game_data or user_id not in guess_game_data[chat_id] or "number" not in guess_game_data[chat_id][user_id]:
        await update.message.reply_text("❗ Спочатку запусти гру через /start_guess")
        return

    if not context.args or not context.args[0].isdigit():
        await update.message.reply_text("Вкажи число після команди. Наприклад: /guess 42")
        return

    guess = int(context.args[0])
    data = guess_game_data[chat_id][user_id]
    data["attempts"] += 1
    data["name"] = user_name
    target = data["number"]

    if guess < target:
        await update.message.reply_text("🔻 Моє число більше")
    elif guess > target:
        await update.message.reply_text("🔺 Моє число менше")
    else:
        attempts = data["attempts"]
        data["total_games"] += 1
        data["total_attempts"] += attempts
        avg = data["total_attempts"] / data["total_games"]
        await update.message.reply_text(f"✅ Вгадав за {attempts} спроб!")
        await update.message.reply_text(f"📊 Твоя середня кількість спроб: {avg:.2f}")
        del data["number"]
        del data["attempts"]
        save_guess_data()

# /guess_leaders — top 25
async def guess_leaders(update, context):
    chat_id = update.effective_chat.id
    chat_data = guess_game_data.get(chat_id, {})

    leaders = [
        (uid, d["name"], d["total_games"], d["total_attempts"], d["total_attempts"] / d["total_games"])
        for uid, d in chat_data.items()
        if d.get("total_games", 0) >= 1
    ]
    leaders.sort(key=lambda x: x[4])
    top25 = leaders[:25]
    if not top25:
        await update.message.reply_text("📉 Ще ніхто не грав у цьому чаті.")
        return
    text = "🏆 Топ-5 гравців цього чату за точністю (менше — краще):\n"
    for i, (uid, name, games, attempts, avg) in enumerate(top25, 1):
        text += f"{i}. {name} — {games} ігор, {attempts} спроб, середнє {avg:.2f}\n"
    await update.message.reply_text(text)

# /reset_guess
async def reset_guess(update, context):
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    if chat_id in guess_game_data and user_id in guess_game_data[chat_id]:
        guess_game_data[chat_id][user_id] = {}
        save_guess_data()
        await update.message.reply_text("🔄 Твоя статистика була обнулена.")
    else:
        await update.message.reply_text("Немає статистики для обнулення.")

# /guess_me
async def guess_me(update, context):
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    user_name = update.effective_user.first_name
    data = guess_game_data.get(chat_id, {}).get(user_id)

    if not data or data.get("total_games", 0) == 0:
        await update.message.reply_text(f"{user_name}, ти ще не грав. Спробуй /start_guess!")
        return

    avg = data["total_attempts"] / data["total_games"]
    await update.message.reply_text(
        f"🧾 Профіль {user_name}:\nІгор: {data['total_games']}\nСпроб: {data['total_attempts']}\nСереднє: {avg:.2f}"
    )

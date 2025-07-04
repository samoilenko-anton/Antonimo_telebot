from telegram import Update

import requests

import random
import os
import json

from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
from datetime import datetime

from keep_alive import keep_alive
from data.data_handler import get_user_response, store_user_response

from predefined_lists.motivation_list import motivation_quotes 
from predefined_lists.universal_houses_list import universal_houses
from predefined_lists.daily_horoscope_list import daily_horoscopes
from predefined_lists.artem_personality_list import artem_personalities
from predefined_lists.pseudo_job_list import pseudo_jobs
from predefined_lists.creature_list import creatures

from chat_games.guess_game import (
    start_guess, guess, guess_leaders, reset_guess, guess_me
)
from chat_games.daily_loot_game import daily_loot, loot_me, loot_top

from chat_games.ban_game import ban, ban_top

from chat_games.fake_slot_game import slot_custom

from chat_games.politics_game import porokhobot

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
BOT_TOKEN = os.getenv("BOT_TOKEN")

# random seed (day)
def get_random_today(user_id):
    today_seed = int(datetime.now().strftime("%Y%m%d"))
    return user_id + today_seed

# Function to generate a humorous "Anton-level" response based on random percentage and units
def generate_response(user_id):
    random.seed(get_random_today(user_id))
    percent = random.randint(0, 100)
    scale_type = random.choice([
        "%", "з 10", "з 5", "з 7 Антонів", "лютоАнтонів", "вітамінів А",
        "на око", "джоулів Антона"
    ])
    
    # based on percent only
    base_templates = [
        f"Твій рівень Антона сьогодні — {percent}%",
        f"За шкалою Антонічності ти на {percent}%", f"Ти Антон на {percent}%.",
        f"Антонність у твоїй крові — {percent}%",
        f"Зараз у тобі приблизно {percent} одиниць Антона.",
        f"Скан завершено. Антонність: {percent}%",
        f"На сьогодні ти Антон на {percent}%, що досить непогано.",
        f"Антонічна діагностика показала: {percent}%",
        f"Рівень Антона: {percent}%. Занотовано.",
        f"{percent}% — саме стільки Антона в тобі на зараз."
    ]

    # scale the number
    scaled_templates = [
        f"За шкалою від 0 до 10: {round(percent / 10, 1)} Антона.",
        f"Це {round(percent / 20, 1)} з 5 Антонів.",
        f"Ти — {round(percent / 14.3, 1)} з 7 Антонів. Майже ліміт.",
        f"{round(percent / 2, 1)} лютоАнтонів. Обережно!",
        f"{round(percent / 4.2, 1)} вітамінів A. Медики попереджали.",
        f"Складно сказати точно, але десь {percent * 7} джоулів Антона.",
        f"На око — десь {percent}%. Але я ж не офтальмолог.",
        f"Груба оцінка: {round(percent / 100, 2)} на шкалі Антонів.",
        f"Це рівень {round(percent / 3.3, 1)} з 30 антонних балів.",
        f"Твій результат: {round(percent / 1.25, 1)} Антон-рейтингу з 80."
    ]

    # when 0%
    zero_responses = [
        "🤖 Антонність не виявлена. Ти чистий NPC.", "📉 0%. Це фіаско, братан.",
        "💀 Не Антон. Не сьогодні. Не ніколи.",
        "👽 Ти більше схожий на Річарда.", "🥶 Нуль. Хіба це можливо?",
        "😒 0. Ти навіть не Антон-мінус.", "🚫 Ти сьогодні без Антона. Суворо.",
        "🧱 Твоя Антонність така ж мертва, як цей бетон.",
        "💤 Ти сьогодні Artem_list[Anton_index]",
        "🕳️ Нічого. Порожнеча. Не Антон."
    ]

    # when 100%
    full_responses = [
        "💯 Абсолютна Антонічність. У тебе навіть паспорт світиться.",
        "🌋 100%. Справжній Антон-первосутність.",
        "🏆 Увійшов до Зали Антонів Вічності.",
        "🧬 У твоїх генах замість ДНК — АНТ.",
        "🦾 Це була ідеальна Антонна хвиля.",
        "🥇 Ти — еталон Антона. Навіть Google підтягується до тебе.",
        "🧠 Максимальна Антон-компетентність досягнута.",
        "🎖️ Тобі варто дати Антон-Медаль.",
        "📡 Антон-сигнал стабільний. Повна синхронізація.",
        "🔥 Ти Антон настільки, що вже палиш повітря навколо."
    ]

    mid_bonus = {
        # 80% -- 100%
        range(80, 100): [
            "🔥 Антонність зашкалює. Ти майже вистрілив лазером із чола.",
            "🧲 Приваблюєш інших Антонів своєю енергією.",
            "🌠 Антон-резонанс на високій частоті.",
            "⚡️ Твій Антон-імпульс майже зірвав сканер.",
            "🛡️ Стабільна форма Антона.", "🔋 Заряд Антона 80%+. Ти готовий.",
            "🦁 Це потужно. Гордий Антон!",
            "💥 Вибухова концентрація Антонічності.",
            "📈 Графік Антонності рве верхню межу.",
            "🎯 Влучно! Це майже повний Антон."
        ],
        # 60% -- 80%
        range(60, 80): [
            "😎 Непогано. Можна навіть сказати — Антон-класік.",
            "🧥 Тримайся, Антоне. В тебе все під контролем.",
            "🎩 Антон-стиль на місці.", "🪞 Стабільна Антонна ідентичність.",
            "🧭 Впевнений напрям Антонізації.",
            "📏 Це прямо по лінійці — рівномірний Антон.",
            "🪶 Легкий, але відчутний рівень Антонної грації.",
            "🫡 Антонність дисциплінована.",
            "📚 Зразковий Антон. Прямо з інструкції.",
            "🚗 Середня швидкість — але вірний шлях."
        ],
        # 40% -- 60%
        range(40, 60): [
            "🤔 Середньостатистичний Антон. Але зі своїм шармом.",
            "⚖️ Баланс Антона витримано.",
            "🛋️ Ти як Антон після обіду — спокійний і невибуховий.",
            "📎 Формально Антон. Неформально — ще подумаємо.",
            "🔍 Трохи Антон, трохи загадка.",
            "🌦️ Мінлива Антонічність. Але не критично.",
            "🥢 Пара Антонів в тобі є.", "🧃 Антон на розведення.",
            "🧸 Тепло, м’яко, спокійно. Антон-мідіум.",
            "🖼️ Ти — картинка середнього Антона."
        ],
        # 20% -- 40%
        range(20, 40): [
            "😐 Маловато. Але ж Антон — це не лише цифра.",
            "🫥 Антон десь поруч, але ще не в тобі.",
            "📉 Ти на спаді Антонного тиску.",
            "🪫 Слаба зарядка. Антона бракує.",
            "🌑 Низька фаза Антона. Але колись піде вгору.",
            "🚶 Початкова стадія Антонності.",
            "🧊 Ще не розтанув до рівня Антона.",
            "🌱 Тільки проростає твоя Антонічна сутність.",
            "🧺 Схоже, Антона залишили в пранні.",
            "🔌 Підключення до Антон-серверу ще не завершене."
        ],
        # 1% -- 20%
        range(1, 20): [
            "🫠 Дуже низька Антонічність. Варто сходити в церкву.",
            "🕳️ Ледь вловимий натяк на Антона.", "📴 Антон у сплячому режимі.",
            "🚽 Антон втік у каналізацію.", "😵‍💫 Стан — Антонний туман.",
            "📉 Це майже провал.", "🕷️ Ти схожий на Антона лише у сні.",
            "🧨 Антон розчинився в повітрі.",
            "🌫️ Туманно. Але це точно не Антон.",
            "📦 Антон загубився на складі особистості."
        ]
    }

    if percent == 0:
        response = f"{random.choice(zero_responses)}"
    elif percent == 100:
        response = f"{random.choice(full_responses)}"
    elif scale_type == "%":
        base = random.choice(base_templates)
        for rng, msg in mid_bonus.items():
            if percent in rng:
                response = f"{base} {msg}"
        response = base
    else:
        response = random.choice(scaled_templates)

    return response

# Assigns a Artem-personality description (random, based on user_id)
def get_artem_personality(user_id: int) -> str:
    random.seed(get_random_today(user_id))
    return random.choice(artem_personalities)

# Daily horoscope message (random, based on user_id)
def get_daily_horoscope(user_id: int) -> str:
    random.seed(get_random_today(user_id))
    return random.choice(daily_horoscopes)

# Assigns a daily 'house' identity (random, based on user_id)
def get_daily_user_house(user_id: int) -> str:
    random.seed(get_random_today(user_id))
    return random.choice(universal_houses)

# /anton_percent
async def anton_percent(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id
    user_name = update.effective_user.first_name

    saved = get_user_response(user_id)
    if saved:
        await update.message.reply_text(saved)
        return

    new_response = user_name + ", " + generate_response(user_id)
    store_user_response(user_id, new_response)
    await update.message.reply_text(new_response)

# /what_artem
async def what_artem(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_name = update.effective_user.first_name
    personality = get_artem_personality(user_id)

    await update.message.reply_text(
        f"{user_name}, твоя Артем-особистість:\n\n{personality}")

# /daily_horoscope
async def daily_horoscope(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_name = update.effective_user.first_name
    text = get_daily_horoscope(user_id)

    await update.message.reply_text(f"🔮 Гороскоп для {user_name}:\n\n{text}")

async def daily_house(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_name = update.effective_user.first_name
    house = get_daily_user_house(user_id)

    await update.message.reply_text(
        f"🏛️ {user_name}, твій будинок на сьогодні \n\n{house}")

# /ask_ai_freak
async def ask_ai_freak(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = " ".join(context.args)
    
    if not user_input:
        await update.message.reply_text(
            "[AI] Напиши щось після /ask_ai_freak, і я відповім 💬")
        return

    try:
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "HTTP-Referer": "antonimo-bot.telebot",
            "X-Title": "Antonimo"
        }

        data = {
            "model":
            "mistralai/mistral-7b-instruct",
            "messages": [
                {"role": "system", "content": "Ти — дружній бот-помічник."},
                {"role": "user", "content": user_input}
            ]
            
        }

        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=data)

        result = response.json()

        # err message
        if "choices" not in result:
            await update.message.reply_text(
                f"❌ OpenRouter відповів несподівано:\n{result}")
            return

        reply = result['choices'][0]['message']['content']
        await update.message.reply_text(reply)

    except Exception as e:
        await update.message.reply_text(f"⚠️ Exception під час запиту: {str(e)}")

# /coinflip — random 50/50
async def coinflip(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.effective_user.first_name
    result = random.choice([
        "🪙 Орел. Це знак — ризикуй!",
        "🪙 Решка. Краще сьогодні не поспішати."
    ])
    await update.message.reply_text(f"{user_name}, твій кидок монети: {result}")

# /motivation — light ironic motivational quotes
async def motivation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.effective_user.first_name
    quote = random.choice(motivation_quotes)
    await update.message.reply_text(f"{user_name}, твоя мотивація на сьогодні:\n\n{quote}")

# /pseudo_job
async def pseudo_job(update: Update, context: ContextTypes.DEFAULT_TYPE):
    random.seed(get_random_today(update.effective_user.id))
    job = random.choice(pseudo_jobs)
    await update.message.reply_text(f"👔 Твоя професія дня: {job}")
    
# /which_creature
async def which_creature(update: Update, context: ContextTypes.DEFAULT_TYPE):
    random.seed(get_random_today(update.effective_user.id))
    creature = random.choice(creatures)
    await update.message.reply_text(f"🐾 Сьогодні ти — {creature}.")

# /slot
def dice_slot_filter(update):
    return update.message.dice is not None and update.message.dice.emoji == "🎰"
dice_filter = filters.MessageFilter(dice_slot_filter)

# logic
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("anton_percent", anton_percent))
app.add_handler(CommandHandler("what_artem", what_artem))
app.add_handler(CommandHandler("daily_horoscope", daily_horoscope))
app.add_handler(CommandHandler("daily_house", daily_house))
app.add_handler(CommandHandler("ask_ai_freak", ask_ai_freak))
app.add_handler(CommandHandler("coinflip", coinflip))
app.add_handler(CommandHandler("motivation", motivation))
app.add_handler(CommandHandler("pseudo_job", pseudo_job))
app.add_handler(CommandHandler("which_creature", which_creature))

app.add_handler(CommandHandler("start_guess", start_guess))
app.add_handler(CommandHandler("guess", guess))
app.add_handler(CommandHandler("guess_leaders", guess_leaders))
app.add_handler(CommandHandler("guess_me", guess_me))
app.add_handler(CommandHandler("reset_guess", reset_guess))

app.add_handler(CommandHandler("daily_loot", daily_loot))
app.add_handler(CommandHandler("loot_me", loot_me))
app.add_handler(CommandHandler("loot_top", loot_top))

app.add_handler(CommandHandler("ban", ban))
app.add_handler(CommandHandler("ban_top", ban_top))

app.add_handler(CommandHandler("slot", slot_custom))

app.add_handler(CommandHandler("porokhobot", porokhobot))

keep_alive()  # start and keep the bot alive
app.run_polling()

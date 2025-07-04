import json
from datetime import datetime
from telegram import Update
from telegram.ext import ContextTypes
import random

def get_message_by_score(score: int) -> str:
    if score == 100:
        return random.choice([
            "🔥 Ти — порохобот №1! Ти вже патрулюєш фронт в Instagram.",
            "💥 Абсолютний порохобот-монстр! Тебе знають навіть у Кремлі.",
            "⚡️ Порохобот, що заряджає країну на 100% — залишайся таким!"
        ])
    elif score >= 90:
        return random.choice([
            "💙 Ти майже на передовій в серці, навіть якщо сидиш на дивані.",
            "🔥 Твій патріотизм вражає більше, ніж обстріли ворога.",
            "💪 Ти не просто порохобот, ти — легенда соцмереж!"
        ])
    elif score >= 75:
        return random.choice([
            "🔥 Порохобот з борщем у руках і лайком на дописі.",
            "💛 Твоя слава шириться швидше, ніж вірус у соцмережах.",
            "👌 Ти патріот з душею фаната і гумором троля."
        ])
    elif score >= 50:
        return random.choice([
            "😎 Ти як борщ — смачний, але не надто гострий.",
            "🤡 Порохобот на півставки: іноді кричиш 'Слава!' іноді спиш.",
            "🙃 Ти в курсі, що робиться, але іноді просто лайкаєш меми."
        ])
    elif score >= 30:
        return random.choice([
            "🤔 Ледве порохобот, але дух у тебе є. Вдячні тобі за це!",
            "😅 Порохобот-любитель — з'являєшся тільки під час гарячих постів.",
            "🦥 Порохобот-інертний: з великою любов’ю до сну і збереження енергії."
        ])
    elif score >= 10:
        return random.choice([
            "😴 Ти порохобот для галочки — навіть спиш, коли треба кричати.",
            "🧟‍♂️ Ти патріот, який прокидається тільки під перемоги ЗСУ.",
            "😬 Твій порохоботизм на рівні \"лайкнув колись у 2014\"."
        ])
    else:
        return random.choice([
            "😂 Порохобот? Скоріше ворог на паузі. Але будемо надіятись!",
            "🙈 Ти уникаєш теми, але рано чи пізно прокинешся.",
            "🤡 Найкращий в світі троль, який грає у порохобота."
        ])

async def porokhobot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id
    today_str = datetime.now().strftime("%Y-%m-%d")
    
    seed_str = f"{chat_id}-{user_id}-{today_str}"
    random.seed(seed_str)

    score = random.randint(0, 100)
    message = get_message_by_score(score)

    await update.message.reply_text(f"📝 Рівень твого порохоботства: {score}%\n{message}\n#СлаваУкраїні 🇺🇦")

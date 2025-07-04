(Ukrainian)

# Telegram Bot with Mini-Games, Personality Featuresand GPT Integration

This Telegram bot is built with Python using the 'python-telegram-bot' library.  
It features multiple mini-games with per-user and per-chat statistics, 
personality features, including a slot machine, a daily loot game,
a porokhobot test, and fun personality assignments for users named Artem
and integrates GPT-based responses via the OpenRouter API.

---

## Features

### Games

- **Guess Game** (`/start_guess`, `/guess`, `/guess_leaders`, `/guess_me`, `/reset_guess`)  
  Classic guess-the-number game from 1 to 100 with per-chat and per-user statistics.

- **Daily Loot** (`/daily_loot`, `/loot_me`, `/loot_top`)  
  Users receive a daily randomized loot item (legendary, rare, common, or trash) with unique names and funny descriptions. Loot statistics are tracked.

- **Fake Slot Game** (`/slot`)  
  Custom slot machine with 12 emojis. The jackpot ("777") never appears, but users are led to believe there's a chance. Limits to 3 attempts per day. Requires specifying another user's username and a game name.

- **Ban Game** (`/ban`, `/ban_top`)  
  Command to ban users in the chat (by replying to their message) and maintain a leaderboard by ban counts.

- **Porokhobot Test** (`/porokhobot`)  
  A personality test measuring "porokhobot" level. The result depends on user ID, chat ID, and date — consistent per day. Provides humorous comments based on score.

---

### Entertainment Commands

- `/anton_percent` — Evaluates "Anton level" with different scales and jokes.
- `/what_artem` — Assigns random "Artem personality" traits.
- `/daily_horoscope` — Daily horoscope.
- `/daily_house` — Daily house assignment.
- `/ask_ai_freak` — Query to OpenRouter AI for answers.
- `/coinflip` — Coin toss with funny messages.
- `/motivation` — Motivational quotes with irony.
- `/pseudo_job` — Random "job of the day".
- `/which_creature` — Daily creature assignment.

---

## Features & Notes

- All games store statistics per chat and per user in JSON files under the data folder.
- Limits on number of attempts (e.g., 3 spins per day for slot).
- Test results are deterministic using seed based on user_id, chat_id, and date.
- Uses OpenRouter AI for answering questions via /ask_ai_freak.
- Easily extendable and configurable commands.

## Data Storage

- Game stats are saved in the 'data' folder ('guess_data.json', 'loot_data.json')  
- Data is loaded at startup and updated after each change  

## Installation

1. Clone the repository  
2. Install dependencies (via 'pip install -r requirements.txt')  
3. Set the environment variable 'BOT_TOKEN' and 'OPENROUTER_API_KEY' with your API key  
4. Run the bot with: python main.py
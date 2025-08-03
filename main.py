
import discord
from discord.ext import commands, tasks
import json
import os
from datetime import datetime, timedelta
from keep_alive import keep_alive

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Конфигурация
MEME_CHANNEL_ID = 123456789012345678  # смени с ID на #мемета
NEWS_CHANNEL_ID = 123456789012345678  # смени с ID на #новини-и-ъпдейти
ROLE_THRESHOLDS = [
    (20, "🧍 Покорителя на Център Мала"),
    (40, "🎩 Приближен до Георги Димитров"),
    (60, "🧔‍♂️ Биг Бос"),
    (80, "🧠 Аврамче"),
    (100, "🏔️ Минделец"),
    (120, "📰 Селски Клюкар"),
    (140, "🔫 Ал Капоне"),
    (160, "👮 Корона Инс"),
    (180, "🍾 Хуска"),
    (200, "💿 Див Турлинчанин")
]
KING_ROLE_NAME = "👑 Турлинчанин"
DATA_FILE = "meme_data.json"

# Зареждане/създаване на база
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump({}, f)

def load_data():
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

@bot.event
async def on_ready():
    print(f"✅ Ботът е онлайн като {bot.user}")
    weekly_check.start()

@bot.event
async def on_message(message):
    if message.author.bot or message.channel.id != MEME_CHANNEL_ID:
        return

    has_media = bool(message.attachments) or "http" in message.content
    if not has_media:
        return

    data = load_data()
    user_id = str(message.author.id)

    if user_id not in data:
        data[user_id] = {"total": 0, "weekly": 0}

    data[user_id]["total"] += 1
    data[user_id]["weekly"] += 1
    save_data(data)

    member = message.author
    guild = message.guild

    for threshold, role_name in ROLE_THRESHOLDS:
        if data[user_id]["total"] == threshold:
            role = discord.utils.get(guild.roles, name=role_name)
            if role:
                await member.add_roles(role)
                news_channel = bot.get_channel(NEWS_CHANNEL_ID)
                if news_channel:
                    await news_channel.send(
                        f"📦 **Нова Меме Роля!**"
                        f"<@{user_id}> качи **{threshold} мемета** в <#{MEME_CHANNEL_ID}>"
                        f"🏅 Получаваш титлата **{role_name}**!"
                        f"Следващото ниво те чака напред – натискай още! 🚀"
                    )
    await bot.process_commands(message)

@tasks.loop(hours=1)
async def weekly_check():
    now = datetime.utcnow()
    if now.weekday() == 6 and now.hour == 17:  # Неделя 20:00 BG време = 17:00 UTC
        data = load_data()
        sorted_users = sorted(data.items(), key=lambda x: x[1]["weekly"], reverse=True)
        if not sorted_users or sorted_users[0][1]["weekly"] == 0:
            return
        guild = bot.guilds[0]
        news_channel = bot.get_channel(NEWS_CHANNEL_ID)
        king_role = discord.utils.get(guild.roles, name=KING_ROLE_NAME)

        # Премахни старата роля
        for member in guild.members:
            if king_role in member.roles:
                await member.remove_roles(king_role)

        top_3 = sorted_users[:3]
        winner_id = int(top_3[0][0])
        winner = guild.get_member(winner_id)
        if winner and king_role:
            await winner.add_roles(king_role)

        text = "**📊 Седмична Меме Класация!**"
        medals = ["🥇", "🥈", "🥉"]
        for i, (uid, val) in enumerate(top_3):
            text += f"{medals[i]} <@{uid}> — {val['weekly']} мемета"
        text += f"👑 Новият **{KING_ROLE_NAME}** е: <@{winner_id}>!"

        if news_channel:
            await news_channel.send(text)

        # Нулирай седмичния брояч
        for user_id in data:
            data[user_id]["weekly"] = 0
        save_data(data)

keep_alive()
bot.run(os.getenv("TOKEN"))

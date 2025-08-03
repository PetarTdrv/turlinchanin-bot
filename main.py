import discord
from discord.ext import commands, tasks
import json
import os

intents = discord.Intents.default()
intents.message_content = True
intents.members = True  # Нужно за роли

bot = commands.Bot(command_prefix="!", intents=intents)

# Тук сложи реалните ID-та от твоя сървър
MEME_CHANNEL_ID = 1318885132048007190    # канал #мемета
NEWS_CHANNEL_ID = 1318885004188586004   # канал #новини-и-ъпдейти

# Файл за запазване на мемета
DATA_FILE = "meme_counts.json"

# Зареждаме мемета от файл (ако има)
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r") as f:
        meme_counts = json.load(f)
    # JSON keys са стрингове, превръщаме ги в int
    meme_counts = {int(k): v for k, v in meme_counts.items()}
else:
    meme_counts = {}

# Роли с техните прагове
roles_thresholds = {
    20: "Покорителя на Център Мала",
    40: "Приближен до Георги Димитров",
    60: "Биг Бос",
    80: "Аврамче",
    100: "Минделец",
    120: "Селски Клюкар",
    140: "Ал Капоне",
    160: "Корона Инс",
    180: "Хуска",
    200: "Див Турлинчанин"
}

turlichanin_role_name = "Турлинчанин 👑"


def save_meme_counts():
    with open(DATA_FILE, "w") as f:
        json.dump(meme_counts, f)


@bot.event
async def on_ready():
    print(f"Ботът е онлайн като {bot.user}")


@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if message.channel.id == MEME_CHANNEL_ID:
        user = message.author
        user_id = user.id

        # Увеличаваме мемета
        meme_counts[user_id] = meme_counts.get(user_id, 0) + 1
        print(f"{user} изпрати меме. Общо: {meme_counts[user_id]}")

        guild = message.guild
        news_channel = bot.get_channel(NEWS_CHANNEL_ID)

        # Проверка за ролите
        new_role_name = None
        for threshold in sorted(roles_thresholds):
            if meme_counts[user_id] >= threshold:
                new_role_name = roles_thresholds[threshold]

        if new_role_name:
            new_role = discord.utils.get(guild.roles, name=new_role_name)
            turlichanin_role = discord.utils.get(guild.roles, name=turlichanin_role_name)
            user_roles = user.roles

            # Премахваме мем роли, различни от новата
            roles_to_remove = [r for r in user_roles if r.name in roles_thresholds.values() and r.name != new_role_name]
            if roles_to_remove:
                await user.remove_roles(*roles_to_remove)
                print(f"Премахнати роли от {user}: {[r.name for r in roles_to_remove]}")

            # Добавяме новата роля, ако я няма
            if new_role and new_role not in user_roles:
                await user.add_roles(new_role)
                print(f"Добавена роля на {user}: {new_role_name}")
                if news_channel:
                    await news_channel.send(f"🎉 {user.mention} току-що получи ролята **{new_role_name}** за изпратени {meme_counts[user_id]} мемета!")

        # Ако има >=200 мемета — добавяме "Турлинчанин 👑"
        if meme_counts[user_id] >= 200:
            turlichanin_role = discord.utils.get(guild.roles, name=turlichanin_role_name)
            if turlichanin_role and turlichanin_role not in user.roles:
                # Премахваме всички мем роли
                roles_to_remove = [r for r in user.roles if r.name in roles_thresholds.values()]
                if roles_to_remove:
                    await user.remove_roles(*roles_to_remove)
                await user.add_roles(turlichanin_role)
                print(f"Добавена роля Турлинчанин 👑 на {user}")
                if news_channel:
                    await news_channel.send(f"👑 {user.mention} е новият **Турлинчанин 👑** с {meme_counts[user_id]} мемета! Честито!")
                meme_counts[user_id] = 0  # Нулиране на броя мемета след Турлинчанин

        save_meme_counts()

    await bot.process_commands(message)


# Тук слагаш своя Discord token
TOKEN = "MTQwMTUxMDAwODk1NjY0OTUxMw.GXwO-R.UoAeH51necyd6yJKXxFxCzm0Ue_gicwhUd08PY"

bot.run(TOKEN)

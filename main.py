import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Ботът е онлайн като {bot.user}")

TOKEN = "MTQwMTUxMDAwODk1NjY0OTUxMw.GXwO-R.UoAeH51necyd6yJKXxFxCzm0Ue_gicwhUd08PY"

bot.run(TOKEN)

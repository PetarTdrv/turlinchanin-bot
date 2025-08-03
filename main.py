import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Ботът е онлайн като {bot.user}")

TOKEN = "ТУК_ПРОСТО_ПОЛЕЖИ_ТОКЕНА_ТВОЙ"

bot.run(TOKEN)

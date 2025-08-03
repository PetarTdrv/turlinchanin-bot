import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Ботът е онлайн като {bot.user}")

TOKEN = "MTQwMTUxMDAwODk1NjY0OTUxMw.GYCmrR.hFFG4oCtXYOGOzBO1Bp_bt7yz-C_7oV3TwLeGY"

bot.run(TOKEN)

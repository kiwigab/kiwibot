import discord, os
from dotenv import load_dotenv

intents = discord.Intents.all()
bot = discord.Bot(intents=intents)

@bot.event
async def on_ready():
    print("The bot started successfully!")

for filename in os.listdir("cogs"):
    if filename.endswith(".py"):
        bot.load_extension(f'cogs.{filename[:-3]}')
            
load_dotenv()
bot.run(os.getenv("DISCORD_TOKEN"))
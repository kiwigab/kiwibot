import discord, os
from dotenv import load_dotenv

intents = discord.Intents.all()
bot = discord.Bot(intents=intents)

@bot.event
async def on_ready():
    print("The bot started successfully!")

for folder, cog_type in [("cogs/commands", "commands"), ("cogs/events", "events")]:
    for filename in os.listdir(folder):
        if filename.endswith(".py"):
            bot.load_extension(f'cogs.{cog_type}.{filename[:-3]}')
            
load_dotenv()
bot.run(os.getenv("DISCORD_TOKEN"))
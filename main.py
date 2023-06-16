import discord, os
from discord.ext import commands
from dotenv import load_dotenv
from database import SupabaseDatabase  

intents = discord.Intents.all()
bot = discord.Bot(intents=intents)
database = SupabaseDatabase()  

@bot.event
async def on_ready():
    await database.connect()  
    print("The bot started successfully!")

@bot.event
async def on_guild_remove(guild):
    guild_id = guild.id
    await database.delete_guild_data(guild_id)  

@bot.event
async def on_disconnect():
    await database.disconnect() 

@bot.slash_command(name="cog", description="reload cog!")
async def reloadcog(ctx, cog_name: str):
    bot.reload_extension(f'cogs.{cog_name}')
    await ctx.respond("reloaded")

for filename in os.listdir("cogs"):
    if filename.endswith(".py"):
        bot.load_extension(f'cogs.{filename[:-3]}')

load_dotenv()
bot.run(os.getenv("DISCORD_TOKEN"))
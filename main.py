import discord
import os

from discord.ext import commands
from dotenv import load_dotenv
from database import SupabaseDatabase

class Bot(commands.Bot):
    def __init__(self, *args, **kwargs):
        intents = discord.Intents.all()
        super().__init__(*args, **kwargs, intents=intents)
        self.database = SupabaseDatabase()

    async def on_ready(self):
        print("The bot started successfully!")

    ## DATABASE
    async def on_connect(self):
        await self.database.connect()

    async def on_resumed(self):
        await self.database.connect()

    async def on_disconnect(self):
        await self.database.disconnect()

    async def on_guild_remove(self, guild):
        guild_id = guild.id
        await self.database.delete_guild_data(guild_id)
    
    ## RELOAD COG
    @commands.slash_command(name="cog", description="reload cog!")
    async def reloadcog(self, ctx, cog_name: str):
        self.reload_extension(f'cogs.{cog_name}')
        await ctx.respond("reloaded")

    ## LOAD COGS
    def load_cogs(self):
        for filename in os.listdir("cogs"):
            if filename.endswith(".py"):
                cog_name = filename[:-3]
                cog_module = f'cogs.{cog_name}'
                
                try:
                    self.load_extension(cog_module)
                except Exception as e:
                    print(f"Failed to load cog {cog_name}: {str(e)}")

    ## RUN BOT
    def run_bot(self):
        load_dotenv()
        self.run(os.getenv("DISCORD_TOKEN"))

bot = Bot()
bot.load_cogs()
bot.run_bot()
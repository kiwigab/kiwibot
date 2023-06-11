import discord, asyncio
from discord.ext import commands
from database import SupabaseDatabase

class Automaticrole(commands.Cog):
    def __init__(self, bot, database):
        self.bot = bot
        self.database = database

    @commands.Cog.listener()
    async def on_ready(self):
        print("events.automaticrole ready")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        autorole = await self.database.get_automatic_role_id(member.guild.id)

        human_role_id = autorole[0]["human_role_id"]
        if human_role_id:
            role = member.guild.get_role(human_role_id)
            await member.add_roles(role)

        bot_role_id = autorole[0]["bot_role_id"]
        if bot_role_id and member.bot:
            role = member.guild.get_role(bot_role_id)
            await member.add_roles(role)
        
def setup(bot):
    database = SupabaseDatabase()
    bot.loop.create_task(database.connect())
    bot.add_cog(Automaticrole(bot, database))
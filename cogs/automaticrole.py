import discord, asyncio
from discord.ext import commands
from main import Bot

class Automaticrole(commands.Cog):
    def __init__(self, bot : Bot):
        self.bot = bot
        self.database = bot.database

    @commands.Cog.listener()
    async def on_ready(self):
        print("events.automaticrole ready")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        guild_data = await self.database.get_guild_data(member.guild.id)

        human_role_id = guild_data[0]["human_role_id"]
        bot_role_id = guild_data[0]["bot_role_id"]

        if human_role_id or not bot_role_id:
            role = member.guild.get_role(human_role_id)
            await member.add_roles(role)

        if bot_role_id and member.bot:
            role = member.guild.get_role(bot_role_id)
            await member.add_roles(role)
        
def setup(bot:Bot):
    bot.add_cog(Automaticrole(bot))
import discord, asyncio
from discord.ext import commands
from database import SupabaseDatabase

class Temporarychannel(commands.Cog):
    def __init__(self, bot, database):
        self.bot = bot
        self.database = database
        self.cooldowns = {}
        self.voice_channels = {}
        self.guild_data_cache = {} 

    @commands.Cog.listener()
    async def on_ready(self):
        print("events.temporarychannel ready")

    async def get_guild_data(self, guild_id):
        if guild_id in self.guild_data_cache:
            return self.guild_data_cache[guild_id]

        guild_data = await self.database.get_guild_data(guild_id)

        self.guild_data_cache[guild_id] = guild_data

        return guild_data

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if after.channel:
            try:
                guild_data = await self.get_guild_data(member.guild.id)
                channel_id = guild_data[0]["temporary_channel_id"]

                if channel_id and channel_id == after.channel.id:
                    if member.id in self.voice_channels:
                        old_channel = member.guild.get_channel(self.voice_channels[member.id])

                        if old_channel:
                            await asyncio.sleep(1)
                            await member.move_to(old_channel)
                            return

                    now = asyncio.get_running_loop().time()
                    if member.id in self.cooldowns and now - self.cooldowns[member.id] < 30:
                        seconds_left = int(30 - (now - self.cooldowns[member.id]))
                        message = f"You are on cooldown for {seconds_left} seconds."
                        await member.send(message, delete_after=10)
                        return

                    self.cooldowns[member.id] = now

                    new_channel = await member.guild.create_voice_channel(
                        name=f"{member.name}'s Channel", category=after.channel.category
                    )
                    self.voice_channels[member.id] = new_channel.id

                    await asyncio.sleep(1)

                    await member.move_to(new_channel)

                    while len(new_channel.members) > 0:
                        await asyncio.sleep(1)

                    await new_channel.delete()
                    del self.voice_channels[member.id]

            except Exception as e:
                print(f"error in temporarychannel: {e}")

    @commands.Cog.listener()
    async def on_disconnect(self):
        await self.database.disconnect()
        
def setup(bot):
    database = SupabaseDatabase()
    bot.loop.create_task(database.connect())
    bot.add_cog(Temporarychannel(bot, database))
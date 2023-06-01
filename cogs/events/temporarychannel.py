import discord, asyncio
from discord.ext import commands
from database import Database

class Temporarychannel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.database = Database()
        self.cooldowns = {} 
        self.voice_channels = {} 

    @commands.Cog.listener()
    async def on_ready(self):
        await self.database.connect()
        print("events.temporarychannel ready")

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if after.channel is not None:
            try:
                channel_id = await self.database.get_temporarychannel(member.guild.id)

                if channel_id == after.channel.id:
                   
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
                    
                    new_channel = await member.guild.create_voice_channel(name=f"{member.name}'s Channel", category=after.channel.category)
                    self.voice_channels[member.id] = new_channel.id

                    await asyncio.sleep(1)

                    await member.move_to(new_channel)

                    while len(new_channel.members) > 0:
                        await asyncio.sleep(1)
                        
                    await new_channel.delete()
                    del self.voice_channels[member.id]

            except Exception as e:
                print(f"error in temporarychannel: {e}")
        
def setup(bot):
    bot.add_cog(Temporarychannel(bot))
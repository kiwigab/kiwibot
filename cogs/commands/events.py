import discord, asyncio
from discord.ext import commands
from discord import SlashCommandGroup
from database import Database

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.database = Database()

    @commands.Cog.listener()
    async def on_ready(self):
        await self.database.connect()
        print("cmds.events ready")

    setup = SlashCommandGroup("setup")

    #TEMPORARY CHANNEL SETUP
    @setup.command(name="temporarychannel", description="Setup a 'Join To Create' channel for temporary voice channels!")
    @commands.cooldown(1, 10, commands.BucketType.guild)
    @commands.guild_only()

    async def temporarychannel(self, ctx):
        embed = discord.Embed(title="Temporary Channel Setup", color=discord.Color.blue())

        if not self.database.conn:
            embed.color=discord.Color.red()
            embed.description = "Apologies, we're currently experiencing an issue connecting to the database. Please try again later."
            await ctx.respond(embed=embed, delete_after=5)
            return

        try: 
            category = await ctx.guild.create_category(name="VOICE")
            await asyncio.sleep(1)
            channel = await ctx.guild.create_voice_channel(name="[🎤] Join To Create", category=category)

            await self.database.set_temporarychannel(ctx.guild.id, channel.id)

            embed.description = "The setup was completed successfully."
            await ctx.respond(embed=embed)

        except:
            embed.color=discord.Color.red()
            embed.description = "There was an error trying to execute this command. Please try again later."
            await ctx.respond(embed=embed, delete_after=5)
            
def setup(bot):
    bot.add_cog(Events(bot))
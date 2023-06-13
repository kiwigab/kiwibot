import discord, asyncio, json, requests, os
from discord.ext import commands
from database import SupabaseDatabase
from easy_pil import Editor, Canvas, Font
from io import BytesIO

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("cmds.fun ready")


    #COINFLIP
    @commands.slash_command(name="coinflip", description="Heads or tails? Flip that coin!")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def coinflip(self, ctx):
        result = random.randint(0, 1)

        if result == 0:
            result_str = "heads"
        else:
            result_str = "tails"

        embed = discord.Embed(title="Coinflip", description=f"The coin landed on {result_str}!", color=discord.Color.blue())

        await ctx.respond(embed=embed)

    # RATE
    @commands.slash_command(name="rate", description="Rate users from the current guild based on different attributes.")
    @commands.cooldown(1, 5, commands.BucketType.user)
    @option("type", choices=["gay", "thot", "simp", "bad", "epicgamer", "stank", "cool", "smart", "funny", "lucky", "dumb"], required=True)
    async def rate(self, ctx, type : str, user : discord.User = None):
        member = user or ctx.author
        embed = discord.Embed(color=discord.Color.blue()) 
        procent = f"{random.randint(0, 100)}%"

        if type == "gay":
            embed.title = "gay rate️‍🌈"
            embed.description = f"{member.mention}, you are {procent} gay"

        elif type == "thot":
            embed.title = "thot rate️‍💦"
            embed.description = f"{member.mention}, you are {procent} thotty"

        elif type == "simp":
            embed.title = "simp rate️‍🥺"
            embed.description = f"{member.mention}, you are {procent} simp"

        elif type == "bad":
            embed.title = "bad rate️‍😈"
            embed.description = f"{member.mention}, you are {procent} bad"

        elif type == "epicgamer":
            embed.title = "epicgamer rate️‍🎮"
            embed.description = f"{member.mention}, you are {procent} an epic gamer"

        elif type == "stank":
            embed.title = "stank rate️‍🦨"
            embed.description = f"{member.mention}, you are {procent} stanky"

        elif type == "cool":
            embed.title = "cool rate😎"
            embed.description = f"{member.mention}, you are {procent} cool"

        elif type == "smart":
            embed.title = "smart rate🧠"
            embed.description = f"{member.mention}, you are {procent} smart"

        elif type == "funny":
            embed.title = "funny rate😂"
            embed.description = f"{member.mention}, you are {procent} funny"

        elif type == "lucky":
            embed.title = "luck rate⭐"
            embed.description = f"{member.mention}, you are {procent} lucky"

        elif type == "dumb":
            embed.title = "dumb rate🤪"
            embed.description = f"{member.mention}, you are {procent} dumb"

        await ctx.respond(embed=embed)


def setup(bot):
    bot.add_cog(Fun(bot))
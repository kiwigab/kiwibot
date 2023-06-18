import discord, asyncio, random, requests
from discord import option
from discord.ext import commands
from langdetect import detect
from main import Bot

class Fun(commands.Cog):
    def __init__(self, bot : Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("cmds.fun ready")

    @commands.slash_command(name="8ball", description="Ask the magic 8-ball a question!")
    async def eight_ball(self, ctx, question):
        responses = {
            "ro": [
                "Da, cu siguranță! ✅",
                "Probabil că da. ✅",
                "Nu pot să-ți răspund acum. 🤔",
                "Mai bine nu-ți spun acum. 🤐",
                "Nu părea probabil. ❌",
                "Absolut deloc! ❌"
            ],
            "en": [
                "Yes, definitely! ✅",
                "Most likely. ✅",
                "I can't answer that right now. 🤔",
                "Better not tell you now. 🤐",
                "Doesn't seem likely. ❌",
                "Absolutely not! ❌"
            ],
            "fr": [
                "Oui, certainement ! ✅",
                "Très probablement. ✅",
                "Je ne peux pas répondre pour le moment. 🤔",
                "Mieux vaut ne pas te le dire maintenant. 🤐",
                "Ça ne semble pas probable. ❌",
                "Absolument pas ! ❌"
            ],
            "bg": [
                "Да, определено! ✅",
                "Много вероятно. ✅",
                "не мога да отговоря на това в момента 🤔",
                "По-добре не ти казвам сега. 🤐",
                "Не изглежда вероятно. ❌",
                "Абсолютно не! ❌"
            ],
            "es": [
                "Sí, ¡definitivamente! ✅",
                "Es muy probable. ✅",
                "No puedo responder eso ahora mismo. 🤔",
                "Mejor no te lo digo ahora. 🤐",
                "No parece probable. ❌",
                "¡Absolutamente no! ❌"
            ]
        }

        language = detect(question)

        if language in responses:
            response = random.choice(responses[language])
        else:
            response = random.choice(responses["en"])

        embed = discord.Embed(title="Magic 8-Ball", color=discord.Color.blue())
        embed.add_field(name="Question", value=question, inline=False)
        embed.add_field(name="Response", value=response, inline=False)
        embed.set_footer(text="Ask the magic 8-ball anything!")

        await ctx.respond(embed=embed)

    #RANDOMFACT
    @commands.slash_command(name="randomfact", description="Get a random fact!")
    async def randomfact(self, ctx):
        response = requests.get("https://useless-facts.sameerkumar.website/api")
        fact = response.json()
        embed = discord.Embed(title="Random Fact", description=fact["data"], color=discord.Color.blue())
        await ctx.send(embed=embed)

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


def setup(bot:Bot):
    bot.add_cog(Fun(bot))
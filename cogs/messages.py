import discord, asyncio, json, requests, os
from discord.ext import commands
from main import Bot
from easy_pil import Editor, Canvas, Font
from io import BytesIO

class Messages(commands.Cog):
    def __init__(self, bot : Bot):
        self.bot = bot
        self.database = bot.database

    @commands.Cog.listener()
    async def on_ready(self):
        print("events.messages ready")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        guild_data = await self.database.get_guild_data(member.guild.id)

        if guild_data:
            welcome_json = guild_data[0]["welcome"]

            if welcome_json:
                welcome_json = json.loads(welcome_json)

                channel = member.guild.get_channel(welcome_json["channel_id"])
                if channel:

                    if welcome_json["welcome_card"]:
                        background = Editor(Canvas((900, 270), color="#424549"))

                        response = requests.get(member.avatar.url)
                        profile = Editor(BytesIO(response.content)).resize((200, 200)).circle_image()

                        poppins_big = Font.poppins(variant="bold", size=50)
                        poppins_regular = Font.poppins(variant="regular", size=30)

                        card_left_shape = [(0, 0), (0, 270), (330, 270), (260, 0)]
                        background.polygon(card_left_shape, "#2C2F33")
                        background.paste(profile, (40, 35))
                        background.ellipse((40, 35), 200, 200, outline="white", stroke_width=5)

                        welcome_message = welcome_json['message']
                        if "[user.mention]" in welcome_message:
                            welcome_message = welcome_message.replace("[user.mention]", member.mention)
                        if "[user.name]" in welcome_message:
                            welcome_message = welcome_message.replace("[user.name]", member.name)
                        if "[guild.name]" in welcome_message:
                            welcome_message = welcome_message.replace("[guild.name]", member.guild.name)

                        background.text((600, 80), "WELCOME", font=poppins_big, color="white", align="center")
                        background.text((600, 140), f"{member.name}#{member.discriminator}", font=poppins_regular, color="white", align="center")

                        image_path = f"./images/welcome_card_{member.id}.png"

                        background.save(image_path)

                        with open(image_path, "rb") as f:
                            await channel.send(welcome_message, file=discord.File(f))
                            f.close()
                            os.remove(image_path)

                    else:
                        await channel.send(welcome_json['message'])

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        guild_data = await self.database.get_guild_data(member.guild.id)

        if guild_data:
            goodbye_json = guild_data[0]["goodbye"]

            if goodbye_json:
                goodbye_json = json.loads(goodbye_json)       

                channel = member.guild.get_channel(goodbye_json["channel_id"])
                if channel:        
                    goodbye_message = goodbye_json['message']
                    if "[user.mention]" in goodbye_message:
                        goodbye_message = goodbye_message.replace("[user.mention]", member.mention)
                    if "[user.name]" in goodbye_message:
                        goodbye_message = goodbye_message.replace("[user.name]", member.name)
                    if "[guild.name]" in goodbye_message:
                        goodbye_message = goodbye_message.replace("[guild.name]", member.guild.name)      

                    await channel.send(goodbye_message)
                
def setup(bot):
    bot.add_cog(Messages(bot))
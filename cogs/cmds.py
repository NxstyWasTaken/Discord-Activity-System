import discord,json,sqlite3
from functions import NxstyFunctions #Functions.py
from discord_components import * #Buttons etc...
from discord.ext import commands as cmds
db = sqlite3.connect("main.sqlite")
cursor = db.cursor()
try:
    with open("config.json",encoding='utf-8') as f:
        bot_config = json.load(f)
except:
    pass
class cmds(cmds.Cog):
    def __init__(self, client):
        self.client = client
    @cmds.command()
    @cmds.has_any_role(bot_config["Perms"]["Admin"])
    async def duty(self,ctx):
        await ctx.message.delete()
        em = discord.Embed(description="**> {on_emoji} {onduty}\n\n> {off_emoji} {offduty}\n\n> ⏱ {activity}\n\n> 🏆 {leaderboard}**".format(on_emoji = self.client.get_emoji(bot_config["on-off-duty"]["on-duty-emoji-id"]),onduty="On Duty",off_emoji= self.client.get_emoji(bot_config["on-off-duty"]["off-duty-emoji-id"]),offduty="Off Duty",activity="Your activity",leaderboard="Leaderboard"),color=discord.Color.green())
        em.set_author(name=f"{ctx.guild.name}",icon_url=f"{ctx.guild.icon_url}")
        await ctx.send(embed=em,components=[[
            Button(emoji = self.client.get_emoji(bot_config["on-off-duty"]["on-duty-emoji-id"]),style = ButtonStyle.green,custom_id=bot_config["Buttons"]["on-button-id"]),
            Button(emoji = self.client.get_emoji(bot_config["on-off-duty"]["off-duty-emoji-id"]),style = ButtonStyle.red,custom_id=bot_config["Buttons"]["off-button-id"]),
            Button(emoji = "⏱",style = ButtonStyle.grey,custom_id=bot_config["Buttons"]["activity-button-id"]),
            Button(emoji = "🏆",style = ButtonStyle.blue,custom_id=bot_config["Buttons"]["leaderboard-button-id"])]])
        
    @cmds.command()
    @cmds.has_any_role(bot_config["Perms"]["Admin"],bot_config["Perms"]["Staff-Manager"])
    async def activity(self,ctx,user:discord.Member = None):
        await ctx.message.delete()
        if ctx.channel.id == bot_config["on-off-duty"]["activity-cmd"]:
            if user is None:
                user = ctx.author
            results = NxstyFunctions.getactivity(user.id)
            if results is not None:
                content = "{hours} {lochours} {minutes} {locmin} {seconds} {locsecs}".format(hours=results[1],lochours="Hours",minutes=results[2],locmin="Minutes",seconds=results[3],locsecs="Seconds")
                embed=discord.Embed(description=f"**{content}**",color=discord.Color.red())
                embed.set_author(name=user.name,icon_url=user.avatar_url)
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(description="**User not found**",color = discord.Color.red())
                await ctx.send(embed=embed)
def setup(client):
    client.add_cog(cmds(client))
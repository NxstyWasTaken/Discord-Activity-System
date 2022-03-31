import discord,json,time,sqlite3
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
class base(cmds.Cog):
    def __init__(self, client):
        self.client = client
    @cmds.Cog.listener()
    async def on_ready(self):
        NxstyFunctions.dbsetup() 
        print('\u001b[32mLogged in as "{name}" (ID: {id})'.format(name=self.client.user.name, id=self.client.user.id))
        print('https://discord.com/oauth2/authorize?client_id={id}&permissions=8&scope=bot%20applications.commands\u001b[0m'.format(id=self.client.user.id))
    @cmds.Cog.listener()
    async def on_button_click(self,interaction):
        if interaction.component.id == bot_config["Buttons"]["on-button-id"]:
            cursor.execute('SELECT * FROM temp_data WHERE userid = {user}'.format(user = interaction.author.id))
            results = cursor.fetchone()
            if results is not None:
                await interaction.send("You are already on shift")
            else:
                staffrole = discord.utils.get(interaction.guild.roles, id=bot_config["on-off-duty"]["on-duty-staff-team-role"])
                cursor.execute('INSERT INTO temp_data(userid,time) VALUES({id},{time})'.format(id=interaction.author.id,time=int(time.time() * 1000)))
                await interaction.author.add_roles(staffrole)
                await interaction.send("You've just entered service")
            db.commit()
        if interaction.component.id == bot_config["Buttons"]["off-button-id"]:
            results = NxstyFunctions.get_temp_data(interaction.author.id)
            if results is not None:
                check = NxstyFunctions.getactivity(interaction.author.id)
                end = int(time.time()*1000)
                diff = end - results[1]
                convert = NxstyFunctions.convert(diff)
                if check is not None:
                    NxstyFunctions.updateuser(interaction.author.id,check,diff)
                else:
                    NxstyFunctions.insertuser(interaction.author.id,diff)
                cursor.execute("DELETE from temp_data WHERE userid = {user}".format(user=interaction.author.id))
                staffrole = discord.utils.get(interaction.guild.roles, id=bot_config["on-off-duty"]["on-duty-staff-team-role"])
                channel = self.client.get_channel(bot_config["on-off-duty"]["on-duty-log"])
                embed=discord.Embed(color = discord.Color.red())
                embed.set_author(name=interaction.author.name,icon_url=interaction.author.avatar_url)
                embed.add_field(name="Hours",value="```{hours}```".format(hours=convert[0]),inline=True)
                embed.add_field(name="Minutes",value="```{minutes}```".format(minutes=convert[1]),inline=True)
                embed.add_field(name="Seconds",value="```{sec}```".format(sec=convert[2]),inline=True)
                await channel.send(embed=embed)
                await interaction.author.remove_roles(staffrole)
                await interaction.send("You just finished your service")
            else:
                await interaction.send("You are not on shift")
            db.commit()
        if interaction.component.id == bot_config["Buttons"]["activity-button-id"]:
            results = NxstyFunctions.getactivity(interaction.author.id)
            if results is not None:
                content = "`{hours} {lochours} {minutes} {locmin} {seconds} {locsecs}`".format(hours=results[1],lochours="Hours",minutes=results[2],locmin="Minutes",seconds=results[3],locsecs="Seconds")
                embed=discord.Embed(title="Your activity",description=f"**{content}**",color=discord.Color.red())
                embed.set_author(name=interaction.author.name,icon_url=interaction.author.avatar_url)
                await interaction.send(embed=embed)
            else:
                await interaction.send("User not found")
        if interaction.component.id == bot_config["Buttons"]["leaderboard-button-id"]:
            results = NxstyFunctions.getleaderboard(10)
            content = ""
            if results:
                for j in range(len(results)):
                    content+= "{count}. {name} Has `{userhours} {localhours} {usermin} {localmin} {usersec} {localsec}`\n".format(count=j+1,name=await self.client.fetch_user(results[j][0]),userhours=results[j][1],localhours="Hours",usermin=results[j][2],localmin="Minutes",usersec=results[j][3],localsec="Seconds")
                embed=discord.Embed(title="{guild}'s {locale}".format(guild=interaction.guild.name,locale="Activity Leaderboard"),description=f"**{content}**",color=discord.Color.red())
                await interaction.respond(embed=embed)
            else:
                await interaction.send("No Results")

def setup(client):
    client.add_cog(base(client))
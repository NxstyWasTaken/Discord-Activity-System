import discord,json,os
from time import sleep
from discord_components import *
cogs = ["cogs.base","cogs.cmds"]
os.system("cls")
try:
    with open("config.json",encoding='utf-8') as f:
        bot_config = json.load(f)
    print("Succesfully Loaded Json File")
except:
    print("Could Not Load Json File")
    sleep(60)
    os._exit(1)
intents = discord.Intents.default()
intents.members = True
nxsty = ComponentsBot(bot_config["prefix"],intents=intents)
nxsty.remove_command("help")
for cog in cogs:
    try:
        nxsty.load_extension(cog)
        print('Succesfully Loaded {cog}'.format(cog=cog))
    except Exception as e:
        print("Could Not Load {cog}: {error}".format(cog=cog,error=str(e)))  
nxsty.run(bot_config["token"])
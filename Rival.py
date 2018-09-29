
import logging
import datetime
import sys
import re
import configparser
import urllib.parse
import urllib.request
import discord
from discord.ext import commands
from discord.ext.commands import Bot,has_role
from utils import *
import asyncio
from subprocess import Popen
from discord.voice_client import VoiceClient


startup_extensions = ["Music"]




# Initialize some global variables
config = configparser.ConfigParser()
config.read('settings.ini')
moderator_roles = config['Roles']['Moderator_Rolenames'].split(',')
owner_id = config['Roles']['Owner_ID']
max_duration = int(config['Settings']['Max_Song_Duration'])

logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
DT = datetime.datetime.today()
handler = logging.FileHandler(filename='Logs\discord' + DT.strftime('%Y%m%d%H%M') + '.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)


bot = commands.Bot(command_prefix=">")
state = {}
@bot.event
async def on_ready():
    print ("Ready")
    
class Main_Commands():
    def __init__(self, bot):
        self.bot = bot


@bot.command(pass_context=True, help="Provides information about a person")
async def info(ctx, user: discord.Member):
    embed = discord.Embed(title="{}'s info".format(user.name), color=0x00ff00)
    embed.add_field(name="Name", value=user.name, inline=True)
    embed.add_field(name="ID", value=user.id, inline=True)
    embed.add_field(name="Status", value=user.status, inline=True)
    embed.add_field(name="Highest role", value=user.top_role)
    embed.add_field(name="Joined", value=user.joined_at)
    embed.set_thumbnail(url=user.avatar_url)
    await bot.say(embed=embed)

@bot.command(pass_context=True, help="provides information about the server")
async def serverinfo(ctx):
    embed = discord.Embed(name="{}'s info".format(ctx.message.server.name), color=0x00ff00)
    embed.set_author(name="Shaderhoth")
    embed.add_field(name="Name", value=ctx.message.server.name, inline=True)
    embed.add_field(name="ID", value=ctx.message.server.id, inline=True)
    embed.add_field(name="Roles", value=len(ctx.message.server.roles), inline=True)
    embed.add_field(name="Members", value=len(ctx.message.server.members))
    embed.set_thumbnail(url=ctx.message.server.icon_url)
    await bot.say(embed=embed)


@bot.command(pass_context=True, help="Adds a role to a user")
async def addrole(ctx, Name, user: discord.User):
    if ctx.message.author.server_permissions.administrator or ctx.message.author.server_permissions.manage_roles:
        Name = str(Name)
        role = discord.utils.get(user.server.roles, name=Name)
        await bot.add_roles(user, role)
    else:
        await bot.say("You have insuficient permissions to run this command (Ban)")

@bot.command(pass_context=True, help="Sends a message to console")
async def request(ctx, Text):
    author = ctx.message.author
    print(str(author) + ': ' + str(Text))

@bot.command(pass_context=True, help="kicks a user")
async def kick(ctx, user: discord.User):
    author = ctx.message.author
    if ctx.message.author.server_permissions.administrator or ctx.message.author.server_permissions.kick_members:
        await bot.kick(user)
    else:
        await bot.say("You have insuficient permissions to run this command (Kick)")

@bot.command(pass_context=True, help="bans a user")
async def ban(ctx, user: discord.User):
    author = ctx.message.author
    if ctx.message.author.server_permissions.administrator or ctx.message.author.server_permissions.ban_members:
        await bot.ban(user)
    else:
        await bot.say("You have insuficient permissions to run this command (Ban)")
    
@bot.event
async def on_message(message):
    channel = bot.get_channel('458778457539870742')
    if message.server is None and message.author != bot.user:
        print(str(message.author) + ": " + str(message.content))
        logger.info(str(message.author) + ": " + str(message.content))
    await bot.process_commands(message)

#if __name__ == "__main__":
#    for extension in startup_extensions:
#        try:
#            bot.load_extension(extension)
#        except Exception as e:
#            exc = '{}: {}'.format(type(e).__name__, e)
#            print('failed to load extension {}\n{}'.format(extension,exc))
#
bot.run("NDY1NDg1Mzk3MTQxNzQ5Nzcw.DiOMlA.tpk1l-k95lSnTkbjiyrd6jxHjuk")



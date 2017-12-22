import discord
import sys
import codecs
import random
from discord.ext import commands
import keywords_dict
import logger
import logging
import configparser
import os.path
from shutil import copyfile
import time

if sys.platform == "win32":
    sys.stdout = codecs.getwriter('utf8')(sys.stdout.buffer)
logging.basicConfig(format='[%(levelname)s @ %(asctime)s] %(message)s', level=20, datefmt='%Y-%m-%d %I:%M:%S %p', filename='bot.log')
logger.log("--- INITIALIZING ---")

kwords = keywords_dict.kwords

nextPun=""

loopN=0

antigushaMode=False

config = configparser.ConfigParser()
if os.path.isfile("config.ini"):
    config.read("config.ini")
else:
    try:
        copyfile("default_config.ini", "config.ini")
        logger.log("Config file config.ini not found, generating a new one from default_config.ini", "warning")
        time.sleep(1)
        config.read("config.ini")
    except:
        logger.log("FATAL: Neither config.ini , nor default_config.ini do not exist, cannot create bot. Exiting in 5 seconds.", "critical")
        time.sleep(5)
        sys.exit(1)

try:
    token = config["Login"]["token"]
    loglevel = int(config["Logging"]["level"])
except:
    logger.log("Something wrong with the config. If you crash, delete it so we can regenerate it.", "error")

logging.Logger.setLevel(logging.getLogger(),loglevel)
logger.log("text", "debug")
logger.log("text")
logger.log("text", "warning")
logger.log("text", "error")
logger.log("text", "critical")

description = '''Puns by Cristian Dragan Buda.'''
bot = commands.Bot(command_prefix='#', description=description)

@bot.event
async def on_ready():
    logger.log("on_ready fired. You are in debug mode.", "debug")
    logger.log("@BudaBot#8055 initialized. Logging in...")
    logger.log('Logged in as ' + bot.user.name + ' with ID [' + bot.user.id + '] on:')
    for sv in bot.servers:
        logger.log('\t[' + str(sv.id) + '] ' + str(sv.name))
        logger.log('\n')
    await bot.change_presence(game=discord.Game(name="DUME PROASTE"))
    while True:
        global loopN
        logger.log("While loop: " + str(loopN))
        loopN = loopN +1
        message = await bot.wait_for_message(check=check_message)
        await bot.send_message(message.channel, nextPun)

@bot.command(pass_context=True)
async def antigusha(ctx):
    global antigushaMode
    if not ctx.message.author.id == "177775499244863488":
        if not antigushaMode:
            antigushaMode = True
            await bot.delete_message(ctx.message)
            await bot.change_presence(game=discord.Game(name="ANTI GUSHA MODE"))
            logger.log("AntigushaMode enabled.")
        else:
            antigushaMode = False
            await bot.delete_message(ctx.message)
            await bot.change_presence(game=discord.Game(name="DUME PROASTE"))
            logger.log("AntigushaMode disabled.")
    else:
        await bot.send_message(ctx.message.channel, "Ai vrea tu, gusha proasta")

@bot.event
async def on_message(message):
    if message.author.id == "177775499244863488" and antigushaMode:
        await bot.delete_message(message)
        await bot.send_message(message.channel, "Iara te bagi, gusha proasta?")
    await bot.process_commands(message)

def check_message(msg:discord.Message=None):
    global nextPun
    for x in kwords.keys():
        y = msg.content.find(x)
        if y != -1:
            nextPun = kwords[x]
            return True
    return False

if token == "YourToken":
    logger.log("Bot login token is invalid. You need to go into config.ini and change the token under Login to your bot's token. Exiting in 5 seconds.", "critical")
    time.sleep(5)
    sys.exit(1)
else:
    try:
        bot.run(token)
    except:
        logger.log("There was an error while connecting the bot to Discord.\nEither your login token is invalid, or idk. Exiting in 5 seconds.", "critical")
        time.sleep(5)
        sys.exit(1)

import discord
import random
from discord.ext import commands
import keywords_dict
import logging

description = '''Puns by Cristian Dragan Buda.'''
bot = commands.Bot(command_prefix='#', description=description)

kwords = keywords_dict.kwords

nextPun=""

loopN=0

antigushaMode=False

logging.basicConfig(format='[%(levelname)s @ %(asctime)s] %(message)s', level=logging.INFO, datefmt='%Y-%m-%d %I:%M:%S %p', filename='bot.log')

@bot.event
async def on_ready():
    logger("@BudaBot#8055 initialized. Logging in...")
    logger('Logged in as ' + bot.user.name + ' with ID [' + bot.user.id + '] on:')
    for sv in bot.servers:
        logger('\t[' + str(sv.id) + '] ' + str(sv.name))
    logger('\n')
    await bot.change_presence(game=discord.Game(name="DUME PROASTE"))
    while True:
        global loopN
        logger("While loop: " + str(loopN))
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
            logger("AntigushaMode enabled.")
        else:
            antigushaMode = False
            await bot.delete_message(ctx.message)
            await bot.change_presence(game=discord.Game(name="DUME PROASTE"))
            logger("AntigushaMode disabled.")
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

def logger(msg, level="info"):
    if level == "info":
        print("[INFO] " + msg)
        logging.info(msg)
    elif level == "warning":
        print("[WARNING] " + msg)
        logging.warning(msg)
    elif level == "error":
        print("[ERROR] " + msg)
        logging.error(msg)
    elif level == "critical":
        print("[CRITICAL] " + msg)
        logging.critical(msg)

with open('token.dat', 'r') as tokenfile:
    token=tokenfile.read().replace('\n', '')

bot.run(token)

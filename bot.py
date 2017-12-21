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

logging.basicConfig(format='[%(levelname)s @ %(asctime)s] %(message)s', level=logging.INFO, datefmt='%Y-%m-%d %I:%M:%S %p', filename='bot.log')

@bot.event
async def on_ready():
    logger("@CristiBot#8055 initialized. Logging in...")
    logger('Logged in as ' + bot.user.name + ' with ID [' + bot.user.id + '] on:')
    for sv in bot.servers:
        logger('\t[' + str(sv.id) + '] ' + str(sv.name))
    logger('\n')
    while True:
        global loopN
        print("\nloop " + str(loopN) + "\n")
        loopN = loopN +1
        message = await bot.wait_for_message(check=check_message)
        await bot.send_message(message.channel, nextPun)

def check_message(msg:discord.Message=None):
    global nextPun
    for x in kwords.keys():
        print(x)
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
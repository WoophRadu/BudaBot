import discord
import random
from discord.ext import commands
import keywords_dict

description = '''Puns by Cristian Dragan Buda.'''
bot = commands.Bot(command_prefix='#', description=description)

kwords = keywords_dict.kwords

nextPun=""

loopN=0

@bot.event
async def on_ready():
    print("@CristiBot#8055 initialized. Logging in...\n")
    print('Logged in as ' + bot.user.name + ' with ID [' + bot.user.id + '] on:')
    for sv in bot.servers:
        print('[' + str(sv.id) + '] ' + str(sv.name))
    print('\n')
    while True:
        global loopN
        print("\nloop\n" + str(loopN))
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
""""@bot.event
async def on_message(message):
    global kwords
    for x in kwords.keys():
        if message.content.find(x):
            pun = kwords[x]
            print(x)
            break
    await bot.send_message(message.channel, pun)"""

with open('token.dat', 'r') as tokenfile:
    token=tokenfile.read().replace('\n', '')

bot.run(token)
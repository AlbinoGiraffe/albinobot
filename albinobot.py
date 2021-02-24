import uwuify
import datetime
import discord
import sys
import os
import hashlib
import random
from dotenv import load_dotenv

intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.reactions = True
client = discord.Client()

load_dotenv()
discord_token = os.getenv("DISCORD_TOKEN")
# print(discord_token)

async def zodiac(question, message):
    zhash = hashlib.md5(question.encode('utf-8'))
    random.seed(zhash)
    x = random.randint(0,2)
    if(x == 0):
        await message.channel.send("Yes!")
        print('yes')
    else:
        if(x==1):
            await message.channel.send("No!")
            print('no')
        else:
            await message.channel.send("IDK BRUH!")
            print('idk')

    print('zodiac')

async def delete_message(message):
    try:
        if(not message.author == client.user):
            await message.delete()
    except:
        print("No Perms!")
        # await message.channel.send("Missing Permissions!")


@ client.event
async def on_connect():
    print('Bot connected')


@ client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))
    print('Waiting')


@ client.event
async def on_message(message):
    # check for recursion
    if message.author == client.user:
        return
    if 'logs' not in message.channel.name:
        print('New Message: {}'.format(message.author.id))

    # if  message.author.id == 476593458392596490:
    #     await message.channel.send('SHUT THE FUCK UP <@476593458392596490>')

    # bot is mentioned
    if client.user.mentioned_in(message):
        print('Mentioned: \'{0}\' {1}'.format(message.content, message.author))
        
        # get bot's datetime
        if "time" in message.content:
            await message.channel.send('It\'s {0}'.format(datetime.datetime.today().isoformat(' ', 'seconds')))
        else:
            await message.channel.send('Hi {0}!'.format(message.author.mention))
            # await message.channel.send('fuck you {0}'.format(message.author.mention))

    # uwuify
    if message.content.startswith('/uwu '):
        new_message = message.content.replace('/uwu ', '')
        await message.channel.send(uwuify.uwu(new_message))

    if message.content.startswith('/clear'):
        await delete_message(message)
        async for m in message.channel.history(limit=200):
            if(m.author == client.user):
                await m.delete()
                print('Deleted {0}'.format(m.content))

    if message.content.startswith('/delete '):
        numDeleted = 0
        await delete_message(message)
        op = message.content.replace('/delete ', '')
        x = op.split()
        if len(x) > 1:
            print("/delete: incorrect number of args")
            await message.channel.send("Parameter Error!")
        else:
            try:

                async for m in message.channel.history(limit=int(x[0])):
                    numDeleted += 1
                    print('Deleted \'{0}\''.format(m.content))
                    await m.delete()
            except:
                print("/delete: expected int but got {}".format(x[0]))
                await message.channel.send("Parameter Error!")
        print("done deleting ({} messages)".format(numDeleted))

    if message.content.startswith('.gb '):
        op = message.content.replace('.gb ', '')
        if len(op) < 1:
            print(".gb: incorrect number of args")
            await message.channel.send("Parameter Error!")
        else:
            print('message: {0}'.format(op))
            # await message.channel.send("it brokey!")
            await zodiac(op, message)

        
    


client.run(discord_token)

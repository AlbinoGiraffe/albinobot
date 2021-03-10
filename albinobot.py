import uwuify
import datetime
import discord
import sys
import os
import random
import cleverbotfree.cbfree
from dotenv import load_dotenv

intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.reactions = True
client = discord.Client()

load_dotenv()
cb = cleverbotfree.cbfree.Cleverbot()
discord_token = os.getenv("DISCORD_TOKEN")
# print(discord_token)


async def zodiac(question, message):
    random.seed()
    x = random.randint(0, 2)
    if(x == 0):
        await message.channel.send("Yes!")
        print('yes')
    else:
        if(x == 1):
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

    # log messages
    if hasattr(message, 'name'):
        if 'logs' not in message.channel.name:
            print('New Message: {0}, Channel: {1}, User: {2}'.format(
                message.content, message.channel.name, message.author.name))
    else:
        print('New Message: {0}, Channel: {1}, User: {2}'.format(
            message.content, message.channel, message.author.name))

    # bot is mentioned
    if client.user.mentioned_in(message):
        print('Mentioned: \'{0}\' {1}'.format(
            message.content, message.author.name))

        # get bot's datetime
        if "time" in message.content:
            await message.channel.send('It\'s {0}'.format(datetime.datetime.today().isoformat(' ', 'seconds')))
        else:
            # send cleverbot query
            query = message.content.replace('<@!560284009469575169> ', '')
            print('query: {}'.format(query))
            response = cb.single_exchange(query)
            # await message.channel.send("{0} {1}".format(message.author.mention, response))
            await message.reply(response)

    # uwuify
    if message.content.startswith('/uwu '):
        new_message = message.content.replace('/uwu ', '')
        await message.channel.send(uwuify.uwu(new_message))

    # only owner can run these >:)
    if(message.author.id == 217644900475338752):
        # clear bot messages
        if message.content.startswith('/clear'):
            await delete_message(message)
            async for m in message.channel.history(limit=200):
                if(m.author == client.user):
                    await m.delete()
                    print('Deleted {0}'.format(m.content))

        # delete x number of messages
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

    # RNG bot
    if message.content.startswith('.gb '):
        op = message.content.replace('.gb ', '')
        if len(op) < 1:
            print(".gb: incorrect number of args")
            await message.channel.send("Parameter Error!")
        else:
            print('message: {0}'.format(op))
            # await message.channel.send("it brokey!")
            await zodiac(op, message)
    if message.content.startswith('/say '):
        new_message = message.content.replace('/say ', '')
        await delete_message(message)
        await message.channel.send(new_message)

    # ping tool
    if message.content.startswith('.ping'):
        await message.channel.send("Pong!")

    # bot is DM'd
    if isinstance(message.channel, discord.channel.DMChannel):
        await message.channel.send(cb.single_exchange(message.content))

    # github link
    if ".github" in message.content:
        await message.channel.send("https://github.com/AlbinoGiraffe/AlbinoBot")

client.run(discord_token)

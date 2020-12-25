import uwuify
import datetime
import discord
import sys
import os
from dotenv import load_dotenv

intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.reactions = True
client = discord.Client()

load_dotenv()
discord_token = os.getenv("DISCORD_TOKEN")
# print(discord_token)


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

    print('New Message: {}'.format(message.author.id))

    if "nigga" in message.content:
        await message.channel.send('SHUT THE FUCK UP')

    # if  message.author.id == 476593458392596490:
    #     await message.channel.send('SHUT THE FUCK UP <@476593458392596490>')

    # bot is mentioned
    if client.user.mentioned_in(message):
        print('Mentioned: \'{0}\' {1}'.format(message.content, message.author))
        # get bot's datetime
        if "time" in message.content:
            await message.channel.send('It\'s {0}'.format(datetime.datetime.today().isoformat(' ', 'seconds')))
            # await message.channel.send('fuck you {0}'.format(message.author.mention))

    # uwuify
    if message.content.startswith('/uwu '):
        await delete_message(message)
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


client.run(discord_token)

import discord
import datetime
import uwuify

intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.reactions = True
client = discord.Client()

discord_token = 'NTYwMjg0MDA5NDY5NTc1MTY5.XJrbJQ.wUOMzEEV9UuivGM8rNJG4iyYpw8'


async def delete_message(message):
    try:
        await message.delete()
    except:
        print("No Perms!")
        await message.channel.send("Missing Permissions!")


@client.event
async def on_connect():
    print('Bot connected')


@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))
    print('Waiting')


@client.event
async def on_message(message):
    # check for recursion
    if message.author == client.user:
        return

    # bot is mentioned
    if "<@!560284009469575169>" in message.content:
        print('Mentioned: \'{0}\' {1}'.format(message.content, message.author))
        # get bot's datetime
        if "time" in message.content:
            await message.channel.send('It\'s {0}'.format(datetime.datetime.today().isoformat(' ', 'seconds')))
            # await message.channel.send('fuck you {0}'.format(message.author.mention))

    if message.content.startswith('/uwu '):
        await delete_message(message)
        if "nigga" in message.content:
            await message.channel.send("Fuck you, i'm not saying that {}".format(message.author.mention))
            return
        new_message = message.content.replace('/uwu ', '')
        await message.channel.send(uwuify.uwu(new_message))

    if message.content.startswith('/clear'):
        await delete_message(message)
        async for m in message.channel.history(limit=200):
            if(m.author == client.user):
                print('Deleted {0}'.format(m.content))
                await m.delete()

    if message.content.startswith('/delete'):
        await delete_message(message)
        op = message.content.replace('/delete ', '')
        x = op.split()
        if len(x) > 1:
            print("/delete: incorrect number of args")
            await message.channel.send("Parameter Error!")
        else:
            try:
                async for m in message.channel.history(limit=int(x[0])):
                    print('Deleted \'{0}\''.format(m.content))
                    await m.delete()
            except:
                print("/delete: expected int but got {}".format(x[0]))
                await message.channel.send("Parameter Error!")
        print("done deleteing")

client.run(discord_token)

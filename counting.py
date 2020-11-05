import discord

intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.reactions = True
client = discord.Client()

discord_token = ''

async def delete_message(message):
    try:
        await message.delete()
    except:
        print("No Perms!")
        await message.channel.send("Missing Permissions!")

global currentNum

@client.event
async def on_connect():
    
    currentNum = 0
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
    m = await message.channel.history(limit=2).flatten()
    

    if(message.content.startswith('/stop')):
        await client.logout()
    if(message.content.startswith('/count ')):
        await delete_message(message)
        op = message.content.replace('/count ', '')
        x = op.split()
        if len(x) > 1:
            print("/count: incorrect number of args")
            await message.channel.send("Parameter Error!")
        else:
            currentNum = x
            print("currentNum set to {0}".format(x))

    if(message.channel.name.startswith('counting-test')):
        # await message.channel.send('Bruh moment')
        print('last message: {0}'.format(m[1].content))
        lastMessage = m[1].content

        if(currentNum == 0):
            currentNum = lastMessage

        # Check if message is a number
        try:
            num = int(message.content)
        except:
            print('not a number: {0}'.format(message.content))
            await message.delete()


client.run(discord_token)



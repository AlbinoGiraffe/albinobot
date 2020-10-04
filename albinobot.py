import discord
intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.reactions = True
client = discord.Client()

discord_token = ''


@client.event
async def on_connect():
    print('Bot connected')


@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))
    print('Waiting')


@client.event
async def on_message(message):
    # print('message {0}'.format(message.content))
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        print('Message received: {0.content}'.format(message))
        await message.channel.send('Hello!')

    if "<@!560284009469575169>" in message.content:
        print('Mentioned: {0}'.format(message.content))
        await message.channel.send('fuck you {0}'.format(message.author.mention))


async def on_reaction_add(reaction, user):
    print('bruh')

client.run(discord_token)

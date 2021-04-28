import uwuify
import datetime
import discord
import sys
import os
import random
import requests
import re
import hashlib
import urllib.parse
# import cleverbotfree.cbfree
from dotenv import load_dotenv

intents = discord.Intents.default()
intents.typing = True
intents.presences = False
intents.reactions = True
client = discord.Client()

load_dotenv()
# cb = cleverbotfree.cbfree.Cleverbot()
discord_token = os.getenv("DISCORD_TOKEN")
# print(discord_token)

URL = "https://www.cleverbot.com/webservicemin?uc=UseOfficialCleverbotAPI"

async def zodiac(question, message):
    random.seed()
    x = random.randint(0, 2)
    if(x == 0):
        await message.channel.send("Yes!")
        # print('yes')
    else:
        if(x == 1):
            await message.channel.send("No!")
            # print('no')
        else:
            await message.channel.send("IDK BRUH!")
            # print('idk')

    # print('zodiac')


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

async def cb_message(message):

    cb.browser.get(cb.url)
    
    query = message.content.replace('<@!560284009469575169> ', '')
    query = query.replace('<', '')
    print('query: {}'.format(query))

    cb.get_form()
    cb.send_input(query)
    cb.browser.close()
    response = cb.get_response()

    # response = cb.single_exchange(query)
    # response = await send(query)
    await message.channel.send("{0} {1}".format(message.author.mention, response))
    await message.reply(response)

async def send(msg):
    body = "stimulus=" + await encode(msg)
    # for i in range(0, len(msg)):
    #     body += '&vText' + (i + 2) + '=' + encodeForSending(this.messages[i]);
    body += '&cb_settings_language=en'
    body += '&cb_settings_scripting=no'
    # if (this.internalId):
    #     body += '&sessionid=' + this.internalId

    body += '&islearning=1'
    body += '&icognoid=wsf'
    body += '&icognocheck=' + str(hashlib.md5(body[7:33].encode('utf-8')).hexdigest())

    # print(body)

    head = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:7.0.1) Gecko/20100101 Firefox/7.0",
            "Referer": "https://www.cleverbot.com",
            "Origin":  "https://www.cleverbot.com",
            "Cookie": "XVIS=TEI939AFFIAGAYQZ"}
    r = requests.post(url = URL, data = body, timeout = 5000, headers = head)

    # print(urllib.parse.unquote(r.headers['CBOUTPUT']))
    return urllib.parse.unquote(r.headers['CBOUTPUT'])

async def encode(msg):
    f = ""
    d = ""
    msg = msg.replace("/[|]/g", "{*}")

    for i in msg:
        if(ord(i) > 255):
            d = repr(i)
            if(d[0:2] == '%u'):
                f += '|' + d[2:]
            else:
                f += d
        else:
            f += i
        
    f = f.replace('|201C', "'").replace('|201D', "'").replace('|2018', "'").replace('|2019', "'").replace('`', "'").replace('%B4', "'").replace('|FF20', '').replace('|FE6B', '')

    # print(f)
    return f

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
            
        # send cleverbot query
        # await cb_message(message)
        await message.channel.send("Hi {}, i'm useless!".format(message.author.mention))

    # uwuify
    if message.content.startswith('/uwu '):
        new_message = message.content.replace('/uwu ', '')
        # sanitize input
        new_message = new_message.replace('@everyone', '@\u200beveryone')

        await delete_message(message)
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
        
        # make bot say something
        if message.content.startswith('/say '):
            new_message = message.content.replace('/say ', '')
            # sanitize input
            new_message = new_message.replace('@everyone', '@\u200beveryone')
            await delete_message(message)
            await message.channel.send(new_message)

    # RNG bot
    if message.content.startswith('.gb '):
        op = message.content.replace('.gb ', '')
        if len(op) < 1:
            print("zodiac: incorrect number of args")
            # await message.channel.send("Parameter Error!")
        else:
            print('zodiac: message: {0}'.format(op))
            # await message.channel.send("it brokey!")
            await zodiac(op, message)

    # ping tool
    if message.content.startswith('.ping'):
        await message.channel.send("Pong!")

    # get bot's datetime
    if message.content.startswith('.time'):
        await message.channel.send('It\'s {0} PST'.format(datetime.datetime.today().isoformat(' ', 'seconds')))

    # bot is DM'd
    if isinstance(message.channel, discord.channel.DMChannel):
        # await cb_message(message)
        # await message.channel.send(cb.single_exchange(message.content))
        await message.channel.send("hello, i dont do anything anymore")

    # github link
    if message.content.startswith('.github'):
        await message.channel.send("https://github.com/AlbinoGiraffe/AlbinoBot")

    # the funny
    if message.content.startswith('/pdf'):
        dad = await client.fetch_user(654564428150472714)
        await message.channel.send("{} pdf file 😳".format(dad.mention))
        await delete_message(message)

# @client.event
# async def on_message_delete(message):
#     if(message.guild.id == 760375168815071264):
#         print("message deleted ({}): {}".format(message.author.name, message.content))
#         if(message.author.id == 670058949709529094):
#             channel = client.get_channel(829165070734327858)
#             embed = discord.Embed(title="Takyon deleted a message", description="", color=0xe74c3c)
#             # embed.add_field(name)
#             embed.add_field(name="Message:", value=message.content, inline=True)
#             embed.set_footer(text="id: {} | {} | #{}".format(message.id, message.created_at, message.channel.name))


#             await channel.send(embed=embed)

# @client.event
# async def on_message_edit(before, after):
#     if(after.guild.id == 760375168815071264):
#         print("message edited ({}): before: {}, after: {}".format(before.author.name, before.content, after.content))
#         if(after.author.id == 670058949709529094):
#             channel = client.get_channel(829165070734327858)
#             embed = discord.Embed(title="Takyon edited a message", description="", color=0xe74c3c)
#             # embed.add_field(name)
#             embed.add_field(name="Before:", value=before.content, inline=True)
#             embed.add_field(name="After:", value=after.content, inline=True)
            
#             embed.set_footer(text="{} | #{}".format(after.created_at, after.channel.name))
            

#             await channel.send(embed=embed)

@client.event
async def on_raw_reaction_add(payload):
    if payload.emoji.name == "📌":
        channel = client.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        reaction = discord.utils.get(message.reactions, emoji=payload.emoji.name)
        if reaction and reaction.count >= 2:
            await message.pin()
        

client.run(discord_token)

import uwuify
import datetime
import discord
import sys
import os
import random

import dotenv
from discord.ext import commands

intents = discord.Intents.default()
intents.typing = True
intents.presences = False
intents.reactions = True

dotenv_file = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_file)

discord_token = os.getenv("DISCORD_TOKEN")
c_prefix = os.getenv("PREFIX")

bot = discord.Client()
bot = commands.Bot(command_prefix=c_prefix)

def check_user(ctx):
    # print("owner check: ({})".format(ctx.message.author.id))
    return (ctx.message.author.id == 217644900475338752)

async def delete_message(message):
    try:
        # if(not message.author == bot.user):
            await message.delete()
    except:
        print("Cannot Delete '{}' NO PERMS".format(message.content))
        # await message.channel.send("Missing Permissions!")

@ bot.command(name="cp")
@ commands.check(check_user)
async def set_command_pref(ctx, n: str):
    bot.command_prefix = n
    dotenv.set_key(dotenv_file, "PREFIX", n)
    await ctx.send("New prefix is: {}".format(n))

@ bot.command()
@ commands.check(check_user)
async def reply(ctx, id: int, *args):
    await ctx.trigger_typing()
    # print("reply")
    msg = ' '.join(args)
    # sanitize
    msg = msg.replace('@everyone', '@\u200beveryone')
    m = await ctx.fetch_message(id)
    await m.reply(msg)
    await delete_message(ctx.message)

@ bot.command()
@ commands.check(check_user)
async def clear(ctx):
    await delete_message(ctx.message)
    async for m in ctx.message.channel.history(limit=200):
        if(m.author == bot.user):
            await m.delete()
            print('Deleted \"{0}\"'.format(m.content))

# delete x number of messages
@ bot.command()
@ commands.check(check_user)
async def delete(ctx, n: int):
    numDeleted = 0
    await delete_message(ctx.message)

    async for m in ctx.message.channel.history(limit=n):
        numDeleted += 1
        print('Deleted \'{0}\''.format(m.content))
        await m.delete()
    print("done deleting ({} messages)".format(numDeleted))
    
# make bot say something
@ bot.command()
@ commands.check(check_user)
async def say(ctx, *args):
    await ctx.trigger_typing()
    new_message = ' '.join(args)
    # sanitize input
    new_message = new_message.replace('@everyone', '@\u200beveryone')
    await delete_message(ctx.message)
    await ctx.send(new_message)

# RNG bot
@ bot.command(name='gb')
async def zodiac(ctx, *args):
    await ctx.trigger_typing()
    random.seed()
    x = random.randint(0, 2)
    if(x == 0):
        await ctx.message.channel.send("Yes!")
        # print('yes')
    else:
        if(x == 1):
            await ctx.message.channel.send("No!")
            # print('no')
        else:
            await ctx.message.channel.send("IDK BRUH!")
            # print('idk')

# ping tool
@ bot.command()
async def ping(ctx):
    await ctx.trigger_typing()
    await ctx.send("Pong!")

# get bot's datetime
@ bot.command()
async def time(ctx):
    await ctx.trigger_typing()
    await ctx.send('It\'s {0} PST'.format(datetime.datetime.today().isoformat(' ', 'seconds')))

# github link
@ bot.command()
async def github(ctx):
    await ctx.trigger_typing()
    await ctx.send("https://github.com/AlbinoGiraffe/AlbinoBot")

# the funny
@ bot.command()
async def pdf(ctx):
    await ctx.trigger_typing()
    dad = await bot.fetch_user(654564428150472714)
    await ctx.send("{} pdf file 😳".format(dad.mention))
    await delete_message(ctx.message)

# uwuifier
@ bot.command()
async def uwu(ctx, *args):
    await ctx.trigger_typing()
    new_message = ' '.join(args)
    # sanitize input
    new_message = new_message.replace('@everyone', '@\u200beveryone')

    await delete_message(ctx.message)
    await ctx.send(uwuify.uwu(new_message))
    
@ bot.event
async def on_connect():
    print('Bot connected')

@ bot.event
async def on_ready():
    print('Logged in as {0.user}'.format(bot))
    print('Waiting')

@ bot.event
async def on_message(message):
    # check for recursion 
    if message.author == bot.user:
        return

    # log messages
    if hasattr(message, 'channel'):
        if 'logs' not in message.channel.name:
            print('New Message: {0}, Channel: {1}, User: {2}'.format(
                message.content, message.channel.name, message.author.name))
    else:
        print('New Message: {0}, Channel: {1}, User: {2}'.format(
            message.content, message.channel, message.author.name))

    # bot is mentioned
    if bot.user.mentioned_in(message):
        print('Mentioned: \'{0}\' {1}'.format(
            message.content, message.author.name))
        await message.channel.send("Hi {}, i'm useless!".format(message.author.mention))

    # only owner can run these >:)
    if(message.author.id == 217644900475338752):
        # clear bot messages
        if message.content.startswith('.kill'):
            pass

    # bot is DM'd
    if isinstance(message.channel, discord.channel.DMChannel):
        # await cb_message(message)
        # await message.channel.send(cb.single_exchange(message.content))
        await message.channel.send("hello, i dont do anything anymore")
    
    await bot.process_commands(message)
    
@ bot.event
async def on_command_error(ctx, err):
    print("Error! ({})".format(err))
    # await ctx.send("Reply error! ({})".format(err))    

@bot.event
async def on_raw_reaction_add(payload):
    if payload.emoji.name == "📌":
        channel = bot.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        reaction = discord.utils.get(message.reactions, emoji=payload.emoji.name)
        if reaction and reaction.count >= 2:
            await message.pin()

# message deleted         
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

# message edited
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


        
bot.run(discord_token)
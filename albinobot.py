from discord.activity import Spotify
from discord.ext.commands.core import check
import starboard as sb
import roles
import economy as ec

import uwuify
import discord
import os
import random
import dotenv
import time
import re
import asyncio
import matplotlib.pyplot as plt

from datetime import datetime
from discord.ext import commands
from discord.ext import tasks
from udpy import UrbanClient
from cleverwrap import CleverWrap
from simpleeval import simple_eval as sp

# time bot startup
start = time.time()

# load .env variables
dotenv_file = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_file)

discord_token = os.getenv("DISCORD_TOKEN")
c_prefix = os.getenv("PREFIX")
admin_id = os.getenv("ADMIN_ID")
cb_api_key = os.getenv("CB_API_KEY")

# start UD and CleverBot api clients
ud_client = UrbanClient()
cb = CleverWrap(str(cb_api_key))

# set up discord api client
bot_intents = discord.Intents.default()
bot_intents.members = True
bot_intents.presences = True
bot = commands.Bot(command_prefix=c_prefix, owner_id=admin_id, intents=bot_intents)
default_activity = ""

# message snipe setup
snipe_message_author = {}
snipe_message_content = {}
snipe_message_date = {}
snipe_message_id = {}

# log messages
async def log(type, message):

    if (type == 'DM'):
        print('[{0}] New Message: {1}, Channel: {2}, User: {3}'.format(
            message.created_at.isoformat(sep=' ', timespec='seconds'),
            message.content, "DM", message.author.name))
    if (type == 'message'):
        print('[{0}] New Message: {1}, Channel: {2}, User: {3}'.format(
            message.created_at.isoformat(sep=' ', timespec='seconds'),
            message.content, message.channel.name, message.author.name))
    if (type == 'mention'):
        print('[{0}] Mentioned: \'{1}\' {2}'.format(
            message.created_at.isoformat(sep=' ', timespec='seconds'),
            message.content, message.author.name))
    if (type == 'delete'):
        print('[{0}] Message Deleted: \'{1}\' {2}'.format(
            message.created_at.isoformat(sep=' ', timespec='seconds'),
            message.content, message.author.name))
    # errors
    if (type == 'pin_error'):
        print("[{}] Error Pinning! ({}, #{})".format(
                    datetime.now().isoformat(sep=' ', timespec='seconds'),
                    message.guild.name, message.channel.name))
    if (type == 'sb_error'):
        print("[{}] Star Board not found! ({})".format(
                    datetime.now().isoformat(sep=' ', timespec='seconds'),
                    message.guild.name))   
    if (type == 'del_error'):
        print("[{}] Error Deleting! ({}, #{})".format(
                    datetime.now().isoformat(sep=' ', timespec='seconds'),
                    message.guild.name, message.channel.name))
    if(type == 'join'):
        print("[{}] Member joined ({}, {}#{})".format(
                    datetime.now().isoformat(sep=' ', timespec='seconds'),
                    message.guild.name,
                    message.name,
                    message.discriminator))


# clean messages for cleverbot
async def clean_input(input):
    query = input.replace('<@560284009469575169> ', '')
    query = query.replace('<@!560284009469575169> ', '')
    query = query.replace('<', '')
    query = query.replace('>', '')
    query = query.replace('@', '')
    return query


# check that user is bot owner or admin
async def check_user(ctx):
    return (ctx.message.author.id == int(
        bot.owner_id)) or ctx.message.author.guild_permissions.administrator


# delete a message
async def delete_message(message):
    try:
        await message.delete()
    except:
        log('del_error', message)


# generate embed for star board
async def board_embed(message, reaction):
    embed = discord.Embed(title=message.author,
                          description=message.content,
                          color=0xe74c3c)
    embed.add_field(name="Jump to Message",
                    value="[Click]({})".format(message.jump_url))
    embed.set_thumbnail(url=message.author.avatar_url)
    timestamp = "{}/{}/{}".format(message.created_at.month,
                                  message.created_at.day,
                                  message.created_at.year)
    embed.set_footer(text="stars: {} • {} • #{}".format(
        reaction.count, timestamp, message.channel.name))

    return embed


## ROLE FUNCTIONS

# break role list into chunks
def split_roles(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


# generate list of roles
async def gen_role_list(role_list, n):
    msg = "```"
    for r in role_list[n]:
        if (not r.is_default()):
            msg = msg + "\"" + r.name + "\"\n"
    msg = msg + "```"
    return msg


# find roles matching id or name
async def find_role(ctx, n):
    result = list()
    x = 0
    for r in ctx.guild.roles:
        try:
            x = int(n)
        except:
            x = 0

        if str(n).lower() == str(r.name).lower():
            result.append(r)
        if x == r.id:
            result.append(r)

    return result

async def list_duplicates(roles):
    msg = "**Duplicate roles! Use role IDs instead**\n"
    for r in roles:
        msg = msg + r.name + " - " + str(r.id) + "\n"
    return msg

# role parent group
@bot.group(help="Role management")
async def role(ctx):
    embd = None
    if ctx.invoked_subcommand is None:
        if(await check_user(ctx)):
            embd = discord.Embed(description="**Role commands:**\n" +
                                "edit [color, name]\n" +
                                "create\n" +
                                "delete\n" + 
                                "list\n" +
                                "listall\n" +
                                "add\n" +
                                "unadd")
        else:
            embd = discord.Embed("```**Role commands:**\n" +
                                "    list (all)\n```")
        await ctx.send(embed=embd)

# role edit group
@role.group(name="edit", help="Edit role attributes <color, name>")
@commands.check(check_user)
async def role_edit(ctx):
    if ctx.invoked_subcommand is None:
        embd = discord.Embed(description="**Role edit commands:**\n" +
                                "color [role name/id] [color]\n" +
                                "name  [role name/id] [new role name]\n")
        await ctx.send(embed=embd)

@role_edit.command(name="color", help="Edit role color <role id/name> <hex/int color>")
@commands.check(check_user)
async def role_edit_color(ctx, rn, *args):
    embd = None
    if(ctx.guild):
        color = ' '.join(args)
        r = await find_role(ctx, rn)

        if(len(r) > 1):
            embd = discord.Embed(description=await list_duplicates(r))
        else:
            if (r):
                if not (re.search(r'^#(?:[0-9a-fA-F]{3}){1,2}$', color)
                        or re.search(r'^(?:[0-9a-fA-F]{3}){1,2}$', color)):
                    embd = discord.Embed(description="**{}** is not valid color code!".format(color))
                else:
                    x = color.lstrip('#')
                    try:
                        await r[0].edit(color=int(x, 16))
                        embd = discord.Embed(description="Role color for **{}** changed to **{}**".format(rn, x), color=int(x, 16))
                    except:
                        embd = discord.Embed(description="Error changing color! (Missing permissions?)")
            else:
                embd = discord.Embed(description="Role **{}** not found!".format(rn))
        
        await ctx.send(embed=embd)
    

@role_edit.command(name="name", help="Edit role name <role id/name> <new name>")
@commands.check(check_user)
async def role_edit_name(ctx, n, *args):
    embd = None
    if(ctx.guild):
        r = await find_role(ctx, n)
        if(len(r) > 1):
            embd = discord.Embed(description=await list_duplicates(r))
        else:
            if(r):
                old_name = r[0].name
                try:
                    if (len(' '.join(args)) == 0):
                        embd = discord.Embed(description="**Role name can't be empty!**")
                    else:
                        await r[0].edit(name=' '.join(args))
                        embd = discord.Embed(description="Role name **{}** changed to **{}**".format(old_name, ' '.join(args)))
                except:
                    embd = discord.Embed(description="**Error changing role name!**")
            else:
                embd = discord.Embed(description="Role **{}** not found!".format(n))
    
        await ctx.send(embed=embd)
        
# role create/delete commands 
@role.command(name="create", help="Create a role <role name>")
@commands.check(check_user)
async def role_create(ctx, *args):
    if (ctx.guild):
        err = False
        end = False
        err_msg = ''
        end_msg = ''

        for n in args:
            try:
                r = await ctx.guild.create_role(name=n)
                
                end = True
                end_msg = end_msg + n + ", "
            except:
                err = True
                err_msg = err_msg + n + ", "

    if (end):
        embd = discord.Embed(description="Role(s) **{}** created".format(end_msg))
        await ctx.send(embed=embd)

    if (err):
        embd = discord.Embed(description="Role(s) **{}** not created!".format(err_msg), color=int('ff0000', 16))
        await ctx.send(embed=embd)

@role.command(name="delete", help="Delete a role <role id/name>")
@commands.check(check_user)
async def role_delete(ctx, *args):
    if (ctx.guild):
        err = False
        end = False
        err_msg = ''
        end_msg = ''

        for n in args:
            r = await find_role(ctx, n)
            if(len(r) > 1):
                await ctx.send(embed=discord.Embed(description=await list_duplicates(r)))
                return
            if(r):
                try:
                    await r[0].delete()
                    end = True
                    end_msg = end_msg + n + ", "
                except:
                    err = True
                    err_msg = err_msg + n + ", "
            else:
                err = True
                err_msg = err_msg + n + ", "

    if (end):
        embd = discord.Embed(description="Role(s) **{}** deleted".format(end_msg))
        await ctx.send(embed=embd)

    if (err):
        embd = discord.Embed(description="Role(s) **{}** not deleted!".format(err_msg), color=int('ff0000', 16))
        await ctx.send(embed=embd)

# role add/unadd commands
@role.command(name="add", help="Make a role assignable <role id/name>")
@commands.check(check_user)
async def role_add(ctx, *args):
    if (ctx.guild):
        err = False
        end = False
        err_msg = ""
        end_msg = ""

        for role in args:
            r = await find_role(ctx, role)
            if(len(r) > 1):
                await ctx.send(embed=discord.Embed(description=await list_duplicates(r)))
                return
            if (r):
                if (not (await roles.is_assignable(r[0].id))):
                    await roles.add_row(ctx, r[0])

                end = True
                end_msg = end_msg + r[0].name + ", "
            else:
                err = True
                err_msg = err_msg + role + ", "

        if (end):
            embd = discord.Embed(description="Role(s) **{}** are now user-assignable".format(end_msg))
            await ctx.send(embed=embd)
        if (err):
            embd = discord.Embed(description="Role(s) **{}** not found!".format(err_msg))
            await ctx.send(embed=embd)

@role.command(name="unadd", help="Make a role unassignable <role id/name>")
@commands.check(check_user)
async def role_unadd(ctx, *args):
    if (ctx.guild):
        err = False
        err_msg = ""
        end_msg = ""

        for role in args:
            r = await find_role(ctx, role)
            if(len(r) > 1):
                await ctx.send(embed=discord.Embed(description=await list_duplicates(r)))
                return
            if (r):
                await roles.delete_row(ctx, r[0])

                end = True
                end_msg = end_msg + r[0].name + ", "
            else:
                err = True
                err_msg = err_msg + role + ", "

        if (end):
            await ctx.send(embed=discord.Embed(description="Role(s) **{}** are now unassignable".format(end_msg)))
        if (err):
            await ctx.send(embed=discord.Embed(description="Role(s) **{}** not found!".format(err_msg)))
    
# role list group
@role.group(name="list", help="List assignable roles <page number>")
async def role_list(ctx, pg=0):
    if ctx.invoked_subcommand is None:
        if (ctx.guild):
            role_list = await roles.get_assignable_roles(int(ctx.guild.id))
            num_roles = len(role_list)

            if (len(role_list) == 0):
                await ctx.send(embed=discord.Embed(description="**No assignable roles!**"))
            else:
                role_list = list(split_roles(role_list, 15))
                rs = len(role_list)
                n = pg - 1

                if (n > rs):
                    n = rs - 1
                if (n < 0):
                    n = 0

                msg = "```"
                for row in role_list[n]:
                    msg = msg + "\"" + row + "\" \n"
                msg = msg + "```"
                embd = discord.Embed(description="**{} Roles that can be self-assigned: (Page {}/{})**\n{}".format(num_roles, n + 1, rs, msg))
                await ctx.send(embed=embd)

@role.command(name="listall", help="List all roles on the server <page number>")
async def role_list_all(ctx, pg=0):
    if (ctx.guild):
        role_list = list(split_roles(ctx.guild.roles, 15))
        num_roles = len(ctx.guild.roles) - 1
        
        rs = len(role_list)
        n = pg - 1

        if (n > rs):
            n = rs - 1
        if (n < 0):
            n = 0

        msg = await gen_role_list(role_list, n)
        
        if(num_roles == 0):
            await ctx.send(embed=discord.Embed(description="**Server has no roles!**"))
            return
        
        embd = discord.Embed(description="**{} Roles (Page {}\{}):**\n{}".format(
            num_roles, n + 1, rs, msg))
        await ctx.send(embed=embd)

@bot.command(name="iamnot", help="Remove a role from yourself <role id/name>")
async def remove_role(ctx, *args):
    if (ctx.guild):
        r = await find_role(ctx, ' '.join(args))
        if(len(r) > 1):
            await ctx.send(embed=discord.Embed(description=await list_duplicates(r)))
            return
        if (r):
            try:
                await ctx.author.remove_roles(r[0])
            except:
                await ctx.send(embed=discord.Embed(description="Error removing the **{}** role!".format(r[0].name), color=r[0].color))
                return
            await ctx.send(embed=discord.Embed(description="Removed the **{}** role!".format(r[0].name), color=r[0].color))
        else:
            await ctx.send(embed=discord.Embed(description="Role **{}** not found!".format(' '.join(args))))

@bot.command(name="iam", help="Give yourself a role <role id/name>")
async def give_role(ctx, *args):
    if (ctx.guild):
        r = await find_role(ctx, ' '.join(args))
        if(len(r) > 1):
            await ctx.send(embed=discord.Embed(await list_duplicates(r)))
            return
        if (r):
            if await roles.is_assignable(r[0].id):
                try:
                    await ctx.author.add_roles(r[0])
                except:
                    await ctx.send(embed=discord.Embed(description="Error giving the **{}** role!".format(r[0].name)))
                    return
                await ctx.send(embed=discord.Embed(description="You now have the **{}** role!".format(r[0].name), color=r[0].color))
            else:
                await ctx.send(embed=discord.Embed(description="You can't have the **{}** role!".format(r[0].name), color=r[0].color))
        else:
            await ctx.send(embed=discord.Embed(description="Role **{}** not found!".format(' '.join(args))))


## END ROLE COMMANDS

# Automatically update to owner's music
@bot.command(name="us", hidden=True)
@commands.check(check_user)
async def init_song(ctx):
    update_song.start(ctx.author)

@tasks.loop(minutes=2)
async def update_song(user):
    if isinstance(user.activity, Spotify):
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="{} - {}".format(user.activity.artist, user.activity.title)))
    else:
        await bot.change_presence(activity=discord.Game(name=default_activity))

# Change game status
@bot.command(name="gs", help="Update bot's game status")
@commands.check(check_user)
async def update_gs(ctx, *args):
    global default_activity 
    default_activity = ' '.join(args)
    
    await bot.change_presence(activity=discord.Game(name=default_activity))
    if default_activity == "":
        embd = discord.Embed(title=f"Cleared bot status")
    else:
        embd = discord.Embed(title=f"Updated bot status to {default_activity}")
    await ctx.send(embed=embd)

# Change listening status
@bot.command(name="ls", help="Update bot's listening status")
@commands.check(check_user)
async def update_gs(ctx, *args):
    default_activity = ' '.join(args)
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=' '.join(args)))

# set command prefix eg. ".gb"
@bot.command(name="cp", help="Change the command prefix")
@commands.check(check_user)
async def set_command_pref(ctx, n: str):
    bot.command_prefix = n
    dotenv.set_key(dotenv_file, "PREFIX", n)
    await ctx.send("New prefix is: {}".format(n))


# reply to a message given it's id (must be in same channel)
@bot.command(help="Make bot reply to a message ID")
@commands.check(check_user)
async def reply(ctx, id: int, *args):
    await ctx.trigger_typing()
    msg = ' '.join(args)
    # sanitize
    msg = msg.replace('@everyone', '@\u200beveryone')
    m = await ctx.fetch_message(id)
    try:
        await m.reply(msg)
    except:
        print("Failed replying!")
    await delete_message(ctx.message)


# clear bot messages
@bot.command(help="Clear bot messages")
@commands.check(check_user)
async def clear(ctx):
    await delete_message(ctx.message)
    async for m in ctx.message.channel.history(limit=200):
        if (m.author == bot.user):
            await m.delete()
            print('Deleted \"{0}\"'.format(m.content))


# delete x number of messages
@bot.command(help="Bulk delete messages")
@commands.check(check_user)
async def delete(ctx, n: int):
    await delete_message(ctx.message)
    delete_list = []
    async for m in ctx.message.channel.history(limit=n):
        delete_list.append(m)

    await ctx.channel.delete_messages(delete_list)
    print("done deleting ({} messages)".format(len(delete_list)))


# make bot say something
@bot.command(help="Make bot say something")
@commands.check(check_user)
async def say(ctx, *args):
    await ctx.trigger_typing()
    new_message = ' '.join(args)
    # sanitize input
    new_message = new_message.replace('@everyone', '@\u200beveryone')
    await delete_message(ctx.message)
    await ctx.send(new_message)


# uwuifier
@bot.command(help="UWUify a message")
@commands.check(check_user)
async def uwu(ctx, *args):
    await ctx.trigger_typing()
    new_message = ' '.join(args)
    # sanitize input
    new_message = new_message.replace('@everyone', '@\u200beveryone')

    await delete_message(ctx.message)
    await ctx.send(uwuify.uwu(new_message))

# anti snipe
@bot.command(name="as")
async def anti_snipe(ctx):
    snipe_message_author[ctx.channel.id] = ""
    snipe_message_content[ctx.channel.id] = ""
    snipe_message_date[ctx.channel.id] = ""
    snipe_message_id[ctx.channel.id] = ""

@bot.command(name="s", help="Snipe a deleted message")
async def snipe(ctx):
    channel = ctx.channel
    try:
        embed = discord.Embed(title=f"{snipe_message_author[channel.id]} deleted a message", color=0xe74c3c)
        embed.add_field(name="Message:", value=snipe_message_content[channel.id], inline=True)
        embed.set_footer(text=f"id: {snipe_message_id[channel.id]} | {snipe_message_date[channel.id]} | #{channel.name}")
        await channel.send(embed=embed)
    except:
        await channel.send("No message to snipe!")
        return

## ECONOMY COMMANDS
@bot.command(name="untrack", hidden=True)
@commands.check(check_user)
async def untrack_user(ctx, user: discord.User):
    if(await ec.is_tracked(ctx.guild.id, user.id)):
        await ec.delete_row(ctx.guild.id, user.id)
        await ctx.send(f"No longer tracking {user.mention}.")

@bot.command(name="track", hidden=True)
@commands.check(check_user)
async def track_user(ctx, user: discord.User, cred=1000):
    if(not await ec.is_tracked(ctx.guild.id, user.id)):
        await ec.add_row(ctx.guild.id, user.id, cred)
        await ctx.send(f"Now tracking {user.mention} with {cred} credits.")

@bot.command(name="updatecreds", hidden=True)
@commands.check(check_user)
async def update_user_credits(ctx, user: discord.User, cred: int):
    await ec.update_cred(ctx.guild.id, user.id, cred)
    await ctx.send(f"Gave {user.mention} {cred} credits.")

@bot.command(name="cc")
async def check_user_credits(ctx, user: discord.User):
    if(await ec.is_tracked(ctx.guild.id, user.id)):
        await ctx.reply(f"{user.mention} has {await ec.get_cred(ctx.guild.id, user.id)} credits.")
    else:
        await ctx.send(f"{user.mention} isn't tracked on this server!")

@bot.command(name="credits", help="check user credits")
async def check_credits(ctx):
    if(await ec.is_tracked(ctx.guild.id, ctx.author.id)):
        await ctx.reply(f"You have {await ec.get_cred(ctx.guild.id, ctx.author.id)} credits")
    else:
        await ctx.send(f"You aren't being tracked on this server!")

@bot.command(name="scores", help="get scoreboard")
async def get_scores(ctx):
    new_scores = []
    scores = await ec.get_user_list(ctx.guild.id)
    # await ctx.send(scores)
    for row in scores:
        try:
            u = ctx.message.guild.get_member(row[0])
            new_scores.append([u.display_name, row[1]])
        except:
            u = "N/A"
    # await ctx.send(new_scores)
    
    x = []
    ypos = []
    for i in new_scores:
        x.append(i[0])
    for i in new_scores:
        ypos.append(i[1])
    xpos = [3 * i for i, _ in enumerate(x)]

    plt.figure(figsize=(35, 10))
    plt.bar(xpos, ypos)
    plt.ylabel('Score')
    plt.xlabel('Members')
    plt.title('Social Credit Scores')
    plt.xticks(xpos, x)
    plt.savefig(f"{ctx.guild.id}.png")
    await ctx.send(file=discord.File(f"{ctx.guild.id}.png"))
    
## END ECONOMY COMMANDS


# Urban Dictionary
@bot.command(name="ud", help="Get an urdban dictionary definition")
async def urban_define(ctx, *args):
    defs = ud_client.get_definition(' '.join(args))
    if (len(defs) == 0):
        embd = discord.Embed(title="Error Getting Word",
                             description="Maybe it doesn't exist on UD?")
        await ctx.send(embed=embd)
    else:
        result = defs[0]
        embd = discord.Embed(title=result.word,
                             description=result.definition,
                             color=0xe74c3c)
        embd.set_footer(text="Example:\n" + result.example)
        await ctx.send(embed=embd)

# RNG bot
@bot.command(name='gb', help="Talk to me")
async def zodiac(ctx, *args):
    query = await clean_input(' '.join(args))
    response = cb.say(query)

    await ctx.channel.trigger_typing()
    if (len(response) > 0):
        await ctx.send(response)
    else:
        await ctx.send("*Ignores you*")
        return


# ping tool
@bot.command(help="Ping the bot")
async def ping(ctx):
    await ctx.trigger_typing()
    await ctx.send("Pong!")


@bot.command(name="time", help="Get bot's time")
async def get_time(ctx):
    await ctx.trigger_typing()
    await ctx.send('It\'s {0} UTC'.format(datetime.today().isoformat(
        ' ', 'seconds')))


# github link
@bot.command(help="Get bot's github link")
async def github(ctx):
    await ctx.trigger_typing()
    await ctx.send("https://github.com/AlbinoGiraffe/AlbinoBot")

@bot.event
async def on_connect():
    print('\nBot connected')


@bot.event
async def on_ready():
    end = time.time()
    print('Logged in as {0.user}'.format(bot))
    print("Ready in", (end - start))
    print('Waiting')


@bot.event
async def on_message(message):
    # check for recursion
    if message.author == bot.user:
        return
    
    # log messages    
    if isinstance(message.channel, discord.channel.DMChannel):
        await log('DM', message)
    else:
        if 'log' not in message.channel.name:
            await log('message', message)
            
    if message.content.startswith("="):
        expr = message.content.replace("=",'')
        await message.reply(str(sp(expr)))
        return

    # tracking
    try:
        if(await ec.is_tracked(message.guild.id, message.author.id)):
            emotion = await ec.process_text(message.content)
            cred = 0
            if(emotion[0] > emotion[1]):
                cred = -int(emotion[0] * 100)
                # await message.channel.send(f"Removed {-cred} credits from {message.author.mention}")
            if(emotion[0] < emotion[1]):
                cred = int(emotion[1] * 100)
                # await message.channel.send(f"Added {cred} credits to {message.author.mention}")
            await ec.update_cred(message.guild.id, message.author.id, cred)    
    except:
        print("Tracking not valid here!")
    
    # snipe messages
    if message.content.lower() == "pls snipe":
        channel = message.channel
        try:
            embed = discord.Embed(title=f"{snipe_message_author[channel.id]} deleted a message", color=0xe74c3c)
            embed.add_field(name="Message:", value=snipe_message_content[channel.id], inline=True)
            embed.set_footer(text=f"id: {snipe_message_id[channel.id]} | {snipe_message_date[channel.id]} | #{channel.name}")
            await channel.send(embed=embed)
        except:
            await channel.send("No message to snipe!")
        return

    # bot is DM'd
    if isinstance(message.channel, discord.channel.DMChannel):
        query = await clean_input(message.content)
        response = cb.say(query)

        await message.channel.trigger_typing()
        if (len(response) > 0):
            await message.channel.send(response)
        else:
            await message.channel.send("*Ignores you*")
            return

    # emphasizes referenced message
    if(message.reference):
        if(message.content.lower() == "what"):
            new_msg = await message.channel.fetch_message(message.reference.message_id)

            if (len(new_msg.attachments) > 0):
                return

            text = new_msg.content
            if (text == text.upper()):
                text = "*{}*".format(text)
            else:
                text = text.upper()
            await message.channel.send(text)
            return

    # emphasizes previous message
    if (message.content.lower() == "what"):
        if (len(message.attachments) > 0):
            return
        m = await message.channel.history(limit=2).flatten()
        new_msg = m[1].content

        if (new_msg == new_msg.upper()):
            new_msg = "*{}*".format(new_msg)
        else:
            new_msg = new_msg.upper()

        await message.channel.send(new_msg)
        return
    
    # conversation
    m = await message.channel.history(limit=2).flatten()
    if(m[1].author == bot.user):
        query = await clean_input(message.content)
        response = cb.say(query)

        await message.channel.trigger_typing()
        try:
            await message.channel.send(response)
        except:
            await message.channel.send("*Ignores you*")

    # bot is mentioned
    if bot.user.mentioned_in(message):
        await log('mention', message)
        query = await clean_input(message.content)
        response = cb.say(query)

        await message.channel.trigger_typing()
        try:
            await message.reply(response)
        except:
            await message.channel.send("*Ignores you*")

    # process bot commands
    await bot.process_commands(message)


@bot.event
async def on_command_error(ctx, err):
    print(
        "[{0}] Error! ({1})".format(datetime.now().isoformat(
            sep=' ', timespec='seconds'), err))


@bot.event
async def on_raw_reaction_add(payload):
    # ignore private channels/ DMs
    channel = bot.get_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)
    reaction = discord.utils.get(message.reactions, emoji=payload.emoji.name)
    if (isinstance(channel, discord.abc.PrivateChannel)):
        return
    
    
    # pin messages
    if payload.emoji.name == "📌":
        if reaction and reaction.count >= 2:
            try:
                await message.pin()
            except:
                # await channel.send("Can't pin! There might be too many pins on this channel?")
                log('pin_error', message)

    # star board
    if payload.emoji.name == "⭐":
        board = discord.utils.get(channel.guild.channels, name="star-board")
        if (board):
            # ignore reactions in board channel
            if (channel.id == board.id):
                return
            if reaction and reaction.count > 2:
                board_id = await sb.check_board(message.id)  # check if message is already on board
                embed = await board_embed(message, reaction)  # generate embed

                if (board_id):
                    try:
                        board_message = await board.fetch_message(board_id)
                    except:
                        # message doesnt exist in board, update list
                        await sb.delete_row(message.id)
                        board_message = await board.send(embed=embed)
                        await sb.add_row(message, board_message, reaction.count)
                    
                    await board_message.edit(embed=embed)
                else:
                    # message not in board, update list
                    board_message = await board.send(embed=embed)
                    await sb.add_row(message, board_message, reaction.count)
        else:
            log ('sb_error', message)
            return

# message deleted
@bot.event
async def on_message_delete(message):
    await log('delete', message)
    snipe_message_author[message.channel.id] = message.author
    snipe_message_content[message.channel.id] = message.content
    snipe_message_date[message.channel.id] = message.created_at
    snipe_message_id[message.channel.id] = message.id
    await asyncio.sleep(60)
    try:
        del snipe_message_author[message.channel.id]
        del snipe_message_content[message.channel.id]
        del snipe_message_date[message.channel.id]
        del snipe_message_id[message.channel.id]
    except:
        return

@bot.event
async def on_member_join(member):
    await log('join', member)
    # channel = member.guild.system_channel
    # await channel.send("Welcome {}!".format(member.mention))

bot.run(discord_token)

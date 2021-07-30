import starboard as sb
import roles

import uwuify
import discord
import os
import random
import dotenv
import time
import re
from datetime import datetime
from discord.ext import commands
from udpy import UrbanClient
from cleverwrap import CleverWrap

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

bot = discord.Client(intents=bot_intents)
bot = commands.Bot(command_prefix=c_prefix, owner_id=admin_id)


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
        # if(not message.author == bot.user):
        await message.delete()
    except:
        print("Cannot Delete '\"{}\"' NO PERMS".format(message.content))
        # await message.channel.send("Missing Permissions!")


# generate embed for star board
async def board_embed(message, reaction):
    embed = discord.Embed(title=message.content,
                          description="",
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
    for r in ctx.guild.roles:
        if str(n).lower() == str(r.name).lower():
            result.append(r)
        if n == r.id:
            result.append(r)
    return result


async def list_duplicates(roles):
    msg = "```Duplicate roles! Use role IDs instead\n"
    for r in roles:
        msg = msg + r.name + " - " + str(r.id) + "\n"
    msg = msg + "```"
    return msg


@bot.command(name="roleedit", help="Edit a role")
@commands.check(check_user)
async def edit_role_assignable(ctx, n, c, *args):
    if (ctx.guild):
        err = False
        end = False
        err_msg = ''
        end_msg = ''

        for role in args:
            r = await find_role(ctx, role)
            if(len(r) > 1):
                await ctx.send(await list_duplicates(r))
                return
            if (r):
                if (n == 'color'):
                    if not (re.search(r'^#(?:[0-9a-fA-F]{3}){1,2}$', c)
                            or re.search(r'^(?:[0-9a-fA-F]{3}){1,2}$', c)):
                        await ctx.send(
                            "**{}** is not valid color code!".format(c))
                        return
                    else:
                        x = c.lstrip('#')
                        try:
                            await r[0].edit(color=int(x, 16))
                            end = True
                            end_msg = end_msg + r[0].name + ", "
                        except:
                            await ctx.send(
                                "Error changing color! (Missing permissions?)")
            else:
                err = True
                err_msg = err_msg + role + ", "

    if (end):
        embd = discord.Embed(
            description="Colors for role(s) **{}** changed to **{}**".format(
                end_msg, x),
            color=int(x, 16))
        await ctx.send(embed=embd)
        # await ctx.send("Colors for role(s) **{}** changed to **{}**".format(end_msg, x))

    if (err):
        await ctx.send("Role(s) **{}** not found!".format(err_msg))


@bot.command(name="rolecreate", help="Create a role")
@commands.check(check_user)
async def create_role(ctx, *args):
    if (ctx.guild):
        roles = await find_role(ctx, ' '.join(args))
        if (len(roles) == 0):
            r = await ctx.guild.create_role(name=' '.join(args))
            await ctx.send("Created role: **{}**".format(r.name))
            print("Created role: {}".format(r.name))
        else:
            await ctx.send("Can't make duplicate role!")


@bot.command(name="roledelete", help="Delete a role")
@commands.check(check_user)
async def delete_role(ctx, n):
    if (ctx.guild):
        r = await find_role(ctx, n)
        if(len(r) > 1):
            await ctx.send(await list_duplicates(r))
            return
        if (r):
            print("Deleted role: {}".format(r[0].name))
            await ctx.send("Deleted role: **{}**".format(r[0].name))
            await r[0].delete()
        else:
            await ctx.send("Role **{}** not found!".format(n))


@bot.command(name="rolelistall", help="List all roles on the server")
async def list_roles(ctx, *args):
    if (ctx.guild):
        role_list = list(split_roles(ctx.guild.roles, 15))
        num_roles = len(ctx.guild.roles)

        rs = len(role_list)
        n = 0
        if (len(args) == 1):
            n = int(' '.join(args)) - 1
            if (n > rs):
                n = rs - 1
            if (n < 0):
                n = 0

        msg = await gen_role_list(role_list, n)
        await ctx.send("**{} Roles (Page {}\{}):**\n{}".format(
            num_roles, n + 1, rs, msg))


@bot.command(name="rolelist", help="List all addable roles")
async def list_assignable(ctx, *args):
    if (ctx.guild):
        role_list = await roles.get_assignable_roles(int(ctx.guild.id))
        num_roles = len(role_list)

        if (len(role_list) == 0):
            await ctx.send("**No assignable roles!**")
        else:
            role_list = list(split_roles(role_list, 15))
            rs = len(role_list)
            n = 0

            if (len(args) == 1):
                n = int(' '.join(args)) - 1
            if (n > rs):
                n = rs - 1
            if (n < 0):
                n = 0

            msg = "```"
            for row in role_list[n]:
                msg = msg + "\"" + row + "\" \n"
            msg = msg + "```"
            await ctx.send(
                "**{} Roles that can be self-assigned: (Page {}/{})**\n{}".
                format(num_roles, n + 1, rs, msg))


@bot.command(name="roleadd", help="Add a self-assignable role")
@commands.check(check_user)
async def make_role_assignable(ctx, *args):
    if (ctx.guild):
        err = False
        end = False
        err_msg = ""
        end_msg = ""

        for role in args:
            r = await find_role(ctx, role)
            if(len(r) > 1):
                await ctx.send(await list_duplicates(r))
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
            await ctx.send(
                "Role(s) **{}** are now user-assignable".format(end_msg))
        if (err):
            await ctx.send("Roles **{}** not found!".format(err_msg))


@bot.command(name="roleunadd", help="Remove a self-assignable role")
@commands.check(check_user)
async def make_role_unassignable(ctx, *args):
    if (ctx.guild):
        err = False
        err_msg = ""
        end_msg = ""

        for role in args:
            r = await find_role(ctx, role)
            if(len(r) > 1):
                await ctx.send(await list_duplicates(r))
                return
            if (r):
                await roles.delete_row(ctx, r[0])

                end = True
                end_msg = end_msg + r[0].name + ", "
            else:
                err = True
                err_msg = err_msg + role + ", "

        if (end):
            await ctx.send(
                "Role(s) **{}** are now unassignable".format(end_msg))
        if (err):
            await ctx.send("Roles **{}** not found!".format(err_msg))


@bot.command(name="iamnot", help="Remove a role from yourself")
@commands.check(check_user)
async def remove_role(ctx, *args):
    if (ctx.guild):
        r = await find_role(ctx, ' '.join(args))
        if(len(r) > 1):
            await ctx.send(await list_duplicates(r))
            return
        if (r):
            try:
                await ctx.author.remove_roles(r[0])
            except:
                await ctx.send("Error removing the **{}** role!".format(r[0].name)
                               )
                return
            await ctx.send("Removed the **{}** role!".format(r[0].name))
        else:
            await ctx.send("Role **{}** not found!".format(' '.join(args)))


# TODO: MAKE FUNNY

@bot.command(name="iam", help="Give yourself a role")
async def give_role(ctx, *args):
    if (ctx.guild):
        r = await find_role(ctx, ' '.join(args))
        if(len(r) > 1):
            await ctx.send(await list_duplicates(r))
            return
        if (r):
            if await roles.is_assignable(r[0].id):
                try:
                    await ctx.author.add_roles(r[0])
                except:
                    await ctx.send("You can't have the **{}** role!".format(
                        r[0].name))
                    return
                await ctx.send("You now have the **{}** role!".format(r[0].name))
            else:
                await ctx.send("You can't have the **{}** role!".format(r[0].name))
        else:
            await ctx.send("Role **{}** not found!".format(' '.join(args)))


## END ROLE COMMANDS


# Change game status
@bot.command(name="gs", help="Update bot's status")
@commands.check(check_user)
async def update_gs(ctx, *args):
    await bot.change_presence(activity=discord.Game(name=' '.join(args)))


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


# set command prefix eg. ".gb"
@bot.command(name="cp", help="Change a command prefix")
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


# RNG bot
@bot.command(name='gb', help="Pick something")
async def zodiac(ctx, *args):
    await ctx.trigger_typing()
    random.seed()
    x = random.randint(0, 2)
    if (x == 0):
        await ctx.message.channel.send("Yes!")
    else:
        if (x == 1):
            await ctx.message.channel.send("No!")
        else:
            await ctx.message.channel.send("IDK BRUH!")


# ping tool
@bot.command(help="Ping the bot")
async def ping(ctx):
    await ctx.trigger_typing()
    await ctx.send("Pong!")


# get bot's datetime
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


# the funny
@bot.command(help="the funny")
async def pdf(ctx):
    await ctx.trigger_typing()
    dad = await bot.fetch_user(654564428150472714)
    await ctx.send("{} pdf file 😳".format(dad.mention))
    await delete_message(ctx.message)


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

    # bot is DM'd
    if isinstance(message.channel, discord.channel.DMChannel):
        query = await clean_input(message.content)
        response = cb.say(query)

        await message.channel.trigger_typing()
        if (len(response) > 0):
            await message.channel.send(response)
        else:
            await message.channel.send("*Ignores you*")

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

    # process bot commands
    await bot.process_commands(message)


@bot.event
async def on_command_error(ctx, err):
    print(
        "[{0}] Error! ({1})".format(datetime.now().isoformat(
            sep=' ', timespec='seconds'), err))


@bot.event
async def on_raw_reaction_add(payload):
    # pin messages
    if payload.emoji.name == "📌":
        channel = bot.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        reaction = discord.utils.get(message.reactions,
                                     emoji=payload.emoji.name)
        if reaction and reaction.count >= 2:
            try:
                await message.pin()
            except:
                # await channel.send("Can't pin! There might be too many pins on this channel?")
                print("[{}] Error Pinning! ({}, #{})".format(
                    datetime.now().isoformat(sep=' ', timespec='seconds'),
                    message.guild.name, channel.name))

    # star board
    if payload.emoji.name == "⭐":
        channel = bot.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        reaction = discord.utils.get(message.reactions,
                                     emoji=payload.emoji.name)
        board = discord.utils.get(channel.guild.channels, name="star-board")

        if (isinstance(channel, discord.abc.PrivateChannel)):
            return
        if (board):
            if (channel.id == board.id):
                return
            if reaction and reaction.count > 1:
                board_id = await sb.check_board(
                    message.id)  # check if message is already on board
                embed = await board_embed(message, reaction)  # generate embed

                if (board_id):
                    try:
                        board_message = await board.fetch_message(board_id)
                    except:
                        # message doesnt exist in board, update list
                        await sb.delete_row(message.id)
                        board_message = await board.send(embed=embed)
                        await sb.add_row(message, board_message,
                                         reaction.count)

                    await board_message.edit(embed=embed)
                else:
                    # message not in board, update list
                    board_message = await board.send(embed=embed)
                    await sb.add_row(message, board_message, reaction.count)
        else:
            return


# message deleted
# @client.event
# async def on_message_delete(message):
#     if(message.guild.id == 760375168815071264):
#         print("message deleted ({}): {}".format(message.author.name, message.content))
#         if(message.author.id == 670058949709529094):
#             channel = client.get_channel(829165070734327858)
#             embed = discord.Embed(title="Takyon deleted a message", help="", color=0xe74c3c)
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
#             embed = discord.Embed(title="Takyon edited a message", help="", color=0xe74c3c)
#             # embed.add_field(name)
#             embed.add_field(name="Before:", value=before.content, inline=True)
#             embed.add_field(name="After:", value=after.content, inline=True)
#             embed.set_footer(text="{} | #{}".format(after.created_at, after.channel.name))
#             await channel.send(embed=embed)

bot.run(discord_token)

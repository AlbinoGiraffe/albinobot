# albinobot

Simple Discord bot written in python using the Discord.py API

## Dependecies

- discord
- python-dotenv
- uwuify
- cleverbotfree
- udpy (for urban dictionary querying)

## Configuration

Bot configuration is taken care of in a .env file placed in the same folder as 'albinobot.py'. In this file, place your token, desired command prefix, and admin user id like so:

```txt
.env
---------------
DISCORD_TOKEN="12345678"
PREFIX="."
ADMIN_ID="12345678"
```
## Running
Simply run it with python 3.

---

## Stuff it can do (as of now)

### User Commands:

- Pin messages after a certain reaction threshold
- Simple Star Board
- Cleverbot integration
- Send uwuified messages
- Simple Yes,No,Maybe RNG function
- User-assignable roles (```.iam Epic```)

### Admin Commands

- Bulk delete messages
- Clear bot messages
- Set command prefix (and save it to the config)
- Make bot reply to a message
- Make bot say something
- Create/Edit/Delete roles
- Manage assignable roles

---

## Command Guide

Change Command Prefix:
> .cp \<new prefix>

Reply to a message:
> .reply \<message id> \<message text>

Clear bot messages:
> .clear

Delete a number of messages in a channel:
> .delete \<number of messages>

Make bot say something:
> .say \<message text>

Get a random answer from the bot:
> .gb \<optional question>

Ping bot:
> .ping

Get time and date of bot:
> .time

Get bot github link
> .github

Send uwuified message:
> .uwu \<message text>

Get the Urban Dictionary defintion of a word:
> .ud \<word>

---

## Role Commands

*All assignable roles for **all** servers are stored in a ```roles.csv``` in the parent directory.*


Edit role(s) (currently only changing the color is supported)
> .roleedit color \<hex or int color value> <role(s)>

Create a role (creates a role with default values)
> .rolecreate \<role name>

Delete a role
> .roledelete \<role name or id>

List all server roles
> .rolelistall \<page number (optional)>

List all user-assignable roles
> .rolelist \<page number>

Add role(s) to the user-asignable list
> .roleadd \<role name(s)>

Remove role(s) from the user-asignable list
> .roleunadd \<role name(s)>

Add a role to yourself
> .iam \<role name>

Remove a role(s) from yourself
> .iam \<role name>

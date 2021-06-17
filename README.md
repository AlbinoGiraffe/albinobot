# albinobot

Simple Discord bot written in python using the Discord.py API

## Dependecies

- discord
- python-dotenv
- uwuify

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
- ~~Cleverbot integration~~ (broken)
- Send uwuified messages
- Simple Yes,No,Maybe RNG function

### Admin Commands

- Bulk delete messages
- Clear bot messages
- Set command prefix (and save it to the config)
- Make bot reply to a message
- Make bot say something

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

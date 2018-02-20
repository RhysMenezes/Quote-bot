import discord
from discord.ext import commands
from discord.ext.commands import Bot
import time
import sqlite3

#prefix
bot = commands.Bot(command_prefix='!')

#check if database is made and load it
db = sqlite3.connect('quotes.db')
cursor = db.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS quotes(user TEXT, message TEXT)')
print('Loaded database')

db.commit()

@bot.event
async def on_ready():
    print ("Connected to discord")

#commands
@bot.command(pass_context=True)
async def ping(ctx):
    await bot.say("pong")
    print ("ping sent")

@bot.command()
async def makequote(*, message: str):

    string = str(message.split(' '))
    print (string[0:])

    #insert into database
    cursor.execute("INSERT INTO quotes VALUES(?,?)",(string[0],string[1:]))
    await bot.say('quote successfully added')

    string = ''
    db.commit()

bot.run("[token key]")
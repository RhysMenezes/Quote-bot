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
async def quote(*, message: str):

    #split the message into words
    string = str(message)
    temp = string.split()

    #take the username out
    user = temp[0]
    del temp[0]

    #join the message back together
    text = " ".join(temp)

    #insert into database
    cursor.execute("INSERT INTO quotes VALUES(?,?)",(user,text))
    await bot.say('quote successfully added')

    string = ''
    db.commit()

    #number of words in the database
    cursor1 = cursor.execute('SELECT * from quotes')
    print (len(cursor1.fetchall()))

@bot.command()
async def getquote(message: str):
    
    #sanitise input
    string=(message,)

    try:
        #query random quote from user
        cursor.execute('SELECT message FROM quotes WHERE user=(?) ORDER BY RANDOM() LIMIT 1',string)
        query = cursor.fetchone()

        #add quotes and username
        output="\""+" ".join(query)+"\" - "+message

        await bot.say(output)

    except Exception:

        await bot.say('No quotes of that user found')

    string = ''   
    db.commit()    

bot.run("[token]")
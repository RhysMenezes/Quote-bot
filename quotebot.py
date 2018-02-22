import discord
from discord.ext import commands
from discord.ext.commands import Bot
import time
import hashlib
import sqlite3

#prefix
bot = commands.Bot(command_prefix='!')

#check if database is made and load it
db = sqlite3.connect('quotes.db')
cursor = db.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS quotes(hash TEXT primary key, user TEXT, message TEXT)')
print("Loaded database")

db.commit()

@bot.event
async def on_ready():
    print ("Connected to discord")

#######commands##########

#test commmand
@bot.command(pass_context=True)
async def ping(ctx):
    await bot.say("pong")
    print ("ping sent")


@bot.command()
async def quotehelp():
    embed = discord.Embed(name="help")
    embed.set_author(name="Quotebot commands:")
    embed.add_field(name="To quote:", value="!quote [user] [message]", inline=False)
    embed.add_field(name="To display", value="!getquote [user]", inline=False)
    await bot.say(embed=embed)


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

    uniqueID=hash(user+message)

    #insert into database
    cursor.execute("INSERT INTO quotes VALUES(?,?,?)",(uniqueID,user,text))
    await bot.say("quote successfully added")

    db.commit()

    #number of words in the database
    rows = cursor.execute('SELECT * from quotes')

    #log to terminal
    print(len(rows.fetchall())+". added - "+user+": \""+text+"\" to database")


@bot.command()
async def getquote(message: str):
    
    #sanitise input
    user=(message,)

    try:
        #query random quote from user
        cursor.execute('SELECT message FROM quotes WHERE user=(?) ORDER BY RANDOM() LIMIT 1',user)
        query = cursor.fetchone()

        #adds quotes
        output="\""+" ".join(query)+"\""

        #log
        print(message+": \""+output+"\" printed to the screen")

        #embeds the output to make it pretty
        style = discord.Embed(name="responding quote", description="- "+message)
        style.set_author(name=output)
        await bot.say(embed=style)

    except Exception:

        await bot.say("No quotes of that user found")

    db.commit()    


bot.run("token")
import discord
from discord.ext import commands
from discord.ext.commands import Bot
import datetime
import hashlib
import sqlite3

#prefix
bot = commands.Bot(command_prefix='!')

#check if database is made and load it
db = sqlite3.connect('quotes.db')
cursor = db.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS quotes(hash TEXT primary key, user TEXT, message TEXT, date_added TEXT)')
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

#help menu
@bot.command()
async def quotehelp():
    embed = discord.Embed(name="help")
    embed.set_author(name="Quotebot commands:")
    embed.add_field(name="To quote:", value="!quote @[user] [message]", inline=False)
    embed.add_field(name="To display", value="!getquote @[user]", inline=False)
    embed.add_field(name="Random quote from a random user", value="!random", inline=False)
    await bot.say(embed=embed)

#print random quote
@bot.command()
async def random():

    cursor.execute("SELECT user,message,date_added FROM quotes ORDER BY RANDOM() LIMIT 1")
    query = cursor.fetchone()

    #log
    print(query[0]+": \""+query[1]+"\" printed to the screen "+str(query[2]))

    #embeds the output
    style = discord.Embed(name="responding quote", description="- "+str(query[0])+" "+str(query[2]))
    style.set_author(name=str(query[1]))
    await bot.say(embed=style)


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
    
    if user[1]!='@':
        await bot.say("Use ```@[user] [message]``` to quote a person")
        return

    uniqueID = hash(user+message)

    #date and time of the message
    time = datetime.datetime.now()
    formatted_time = str(time.strftime("%d-%m-%Y %H:%M"))

    #find if message is in the db already
    cursor.execute("SELECT count(*) FROM quotes WHERE hash = ?",(uniqueID,))
    find = cursor.fetchone()[0]

    if find>0:
        return

    #insert into database
    cursor.execute("INSERT INTO quotes VALUES(?,?,?,?)",(uniqueID,user,text,formatted_time))
    await bot.say("Quote successfully added")

    db.commit()

    #number of words in the database
    rows = cursor.execute("SELECT * from quotes")

    #log to terminal
    print(str(len(rows.fetchall()))+". added - "+str(user)+": \""+str(text)+"\" to database at "+formatted_time)


@bot.command()
async def getquote(message: str):
    
    #sanitise name
    user = (message,)

    try:
        #query random quote from user
        cursor.execute("SELECT message,date_added FROM quotes WHERE user=(?) ORDER BY RANDOM() LIMIT 1",user)
        query = cursor.fetchone()

        #adds quotes to message
        output = "\""+str(query[0])+"\""

        #log
        print(message+": \""+output+"\" printed to the screen "+str(query[1]))

        #embeds the output to make it pretty
        style = discord.Embed(name="responding quote", description="- "+message+" "+str(query[1]))
        style.set_author(name=output)
        await bot.say(embed=style)

    except Exception:

        await bot.say("No quotes of that user found")

    db.commit()    


bot.run("[token]")
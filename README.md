# Quote-bot
A discord bot that can store quotes/messages from users in a database which can be called at any time.

## Requirements
```
Python 3.5+
discord.py
```

## How to run
1. Install the discord.py package.
```
pip install discord.py
```
2. Create a bot application [here](https://discordapp.com/developers/applications/) and get a discord token/secret key.

3. Add your token/secret key where it says [token] at the bottom of the code and run:
```
python quotebot.py
```
## Commands
!quote @[user] [message] - stores a quote by the user  
!getquote @[user] - gets a users quote  
!quotehelp - shows a list of commands and syntax
!random - gets a random quote from a random user

##FAQ
* The program has checks to stop people adding the same quote to a given person

* Check your python version if you have async problems
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

4. Add your token/secret key where it says [token] at the bottom of the code.

3. To add the bot to your server find your client ID from the page above and replace it in X's in the link below.
```
https://discordapp.com/oauth2/authorize?client_id=XXXXXXXXXXXXXXX&scope=bot
```
5. Finally run:
```
python quotebot.py
```
## Commands
!quote @[user] [message] - stores a quote by the user.  
!getquote @[user] - gets a users quote.  
!quotehelp - shows a list of commands and syntax.   
!random - gets a random quote from a random user.

## FAQ
* The program has checks to stop people adding the same quote to a given person.

* Check your python version if you have async problems.

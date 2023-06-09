# Most of this bot is a joke, like who actually has a 'swearlist'. I just wanna mess with my friends. The only reason I am making this is to try and learn python and learn how to interface with an API
# The main goal for this bot would be to link with the Bungie API and do cool functions with it. 
# I can guarantee this is clunky 
import discord
from discord.ext import commands
import os

# Signal will allow us to update our swearlist on CTRL+C
import signal

# Below will handle getting the discord bot's token to log in

from dotenv import load_dotenv
load_dotenv()

# For testing with bungie stuff before I make my own BungieAPI wrapper
import aiobungie
# Random number generator
import random

# Import helper .py
import files.functions as functions
import files.clashAPI as clashAPI

# I think someone misclicked and started watching this repository, so like I'm using .env now.
bclient = aiobungie.Client(os.getenv('BUNGIE_TOKEN'))
# Date and Time
import datetime,time
# UserList

# We need our list of no-no words, lets get it
bad_words = []
try: 
    f = open('swearlist.txt','r+')
    for line in f:
        if not line.strip().lower().isspace():
            bad_words.append(line.strip().lower())
except:
    print("SwearList failed")

# And here will be the responses to the bad words
bad_responses = ["Erm, Language!","That's not gonna fly here buddy","Watch it buster!","I'm warning you kiddo","We don't talk like that around here"]
# And here will be the responses to the people who are excluded
in_the_clear = ["Looks alright to me","I'll let it slide this time","She gets a pass"]
# Responses to truppa
joe_words = [
    "Not funny",
    "Try again tman",
    "No one cares",
    "Did anyone ask?"
]

intented = discord.Intents.all()
client = discord.Client(intents=intented)
bot = commands.Bot(command_prefix='/',intents=intented)
# Time that the discord client starts????
startTime = time.time()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    # channel = client.get_channel(789609064967307274)
    startTime = time.time()
    #await channel.send("Raspberry PyBot Online!")
    # I want the bot to send me a DM when its turned on
    jt_user = await client.fetch_user(173748750068482048)
    jt_dm = await client.create_dm(jt_user)
    
    await jt_dm.send("Bot Online!")
    
    print("Welcome to JT's Discord Bot User Interface")
            
# I want the bot to handle all users in the server, so lets make it able to send messages to new users!
@client.event
async def on_member_join(member):
    # How do I figure out which is the right channel for multiple servers?
    # I could use JSONs later, for now just use ChannelID
    guild = client.get_guild(789357860886675456)                                                                                                    
    channel = guild.get_channel(1108530112699310104)                                                                                                 
    await channel.send(f'**Welcome to the server {member.mention} ! :partying_face:**')                                                             
    

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    # So we need this code to run to update the scoreboard. The scoreboard will eventually use a SQL database, but for now it's just going to use the text file
    

    # This is just the prefix command. I know I'm not doing commands right but I'm learning okay
    if message.content == '$':
        embeded = discord.Embed(
            colour=discord.Colour.blue(),
            description="$ is my prefix. If you\'d like to see more commands enter \"$help\"\n`I am a bot coded in Python by JT`",
            title="Hi There!"
        )
        embeded.set_footer(text="Bleep Bloop - I am a robot!")
        embeded.set_author(name="JT-Bot",url="https://github.com/jtadams02/JT-Bot")
        await message.channel.send(embed=embeded)
        return
    
    # Leaderboard, broken af
    if message.content == '$scoreboard':
        await functions.leaderboard(message)
        return

    # This function is for testing the usage of the clash royale api
    if message.content.lower().startswith('$clash'):
        m = message.content.split(' ')
        if len(m) == 2:
            if m[1].startswith("#"):
                m[1] = m[1][1:]
            # Now we need to call the the clash function
            data = clashAPI.discord_testing(m[1])
            if data == 0:
                await message.channel.send(f"The tag you provided caused an error\nYour input: {m[1]}")
                return
            await message.channel.send(embed=data)
            return
        elif len(m) == 1 :
            await message.channel.send(embed=clashAPI.commands_response())
            return

    # Simple help command
    if message.content == '$help':
        test = "HELP ME"
        embeded = discord.Embed(
            colour=discord.Colour.blue(),
            description="There aren't a lot of commands right now, but here's what we got:\n$members : See whos in this channel and who's online!\n$uptime : See how long the bots been running!\n$swear : Report a swear word you would like to add to the no-no list\n$delete : Delete a swear word from the swear list\n$list : List all of the swears in the swearlist!\n$shutdown : Turn off the discord bot (Only JT can run this)",
            title="Commands:"
        )
        embeded.set_footer(text="Bleep Bloop - I am a robot!")
        embeded.set_author(name="JT-Bot",url="https://github.com/jtadams02/JT-Bot")
        #await message.channel.send("`There aren't a lot of commands right now, but here's what we got:\n$members : See whos in this channel and who's online!\n$uptime : See how long the bots been running!\n$swear : Report a swear word you would like to add to the no-no list\n$delete : Delete a swear word from the swear list\n$list : List all of the swears in the swearlist!\n$shutdown : Turn off the discord bot (Only JT can run this)`")
        await message.channel.send(embed=embeded)
        return

    # I'm gonna make the shutdown command run first due to priority reasons
    if message.content == '$shutdown':
        if message.author.id == 173748750068482048:
            await client.close()
            return # Is this needed?
        else:
            await message.reply('Sorry, but only Supreme Leader JT can run this command! Better luck next time')
            return
        
        
    # Remove 100 messages from the bot
    # Mostly just going to test whether or not the bot has permissions with this one
    if message.content.startswith('$purge') and message.author.id == 173748750068482048:
        # Cannot use the helper function on this due to client not being passed!
        if len(message.content.split()) < 2:
            deleted = await message.channel.purge(limit=100,check=is_me)
            await message.channel.send(f'Deleted {len(deleted)} message(s)')
            return 
        else: 
            return
        
    
    # List Members
    if message.content == '$members':
        list_members = functions.list_online(message)
        await message.channel.send(list_members)
        
    # List the swear list
    if message.content == '$list':
        # Loop time to print
        response1 = '`'
        for word in bad_words:
            response1+=(word+'\n')
        response1+='`'
        # Yeah I don't want this list of swears cluttering it up
        await message.channel.send(response1,delete_after=10.0)
        return

    # Find the most said word in the channel:
    if message.content == "$frequency":
        await functions.frequency(message.channel)
        return
            
        
            
    # Ideally this will add the given swear to the swear list. Jt should maintain the swear list to make sure it is right
    if message.content.startswith("$swear"):
        msg = message.content
        if len(msg.split()) < 2:
            await message.reply("We're sorry, but we cannot add an empty space to the list",delete_after=5.0)
            return
        swear = msg.split(' ')[1]
        if swear.isspace():
            await message.reply("We're sorry, but we cannot add an empty space to the list",delete_after=5.0)
            return
        temp = f # Temp variable I do not think is needed!
        if swear.lower() in bad_words:
            await message.reply("We're sorry, but that swear is already on the list!",delete_after=5.0)
            return
        else:
            #temp.write('\n'+swear.lower())
            bad_words.append(swear.lower())
            toSend = (swear+' has been added to the swearlist. Thank you for making our server a safer place!')
            await message.channel.send(toSend)
            return
        
    # This code will remove swears from the bad_words array and ideally the file    
    if message.content.startswith("$delete"):
        msg = message.content 
        if len(msg.split()) < 2:
            await message.reply("Sorry, but swears are only 1 word long!",delete_after=10.0)
            return
        swear = msg.split(' ')[1]
        if swear.isspace():
            await message.reply("Cannot delete empty string",delete_after=10.0)
            return
        if swear.lower() in bad_words:
            # Now we remove the swear
            while(swear.lower() in bad_words):
                bad_words.remove(swear)
            response = swear +" has been deleted!"
            await message.reply(response)
            return
            #IDK how to remove it from file yet?!
        else: 
            await message.reply("We're sorry, but that swear is not in the swear list!")
            return

            
    # This code is buggy, the time does not work right
    if message.content == '$uptime':
        uptime = str(datetime.timedelta(seconds=int(round(time.time()-startTime))))
        msg = 'JT Bot has been active for: ' + str(uptime)
        await message.channel.send(msg)
        return

    # Just a simple hi
    if message.content.startswith('$hi'):
        await message.channel.send('Hello there! I am a robot!')

    # Below code checks whether or not a word in the message matches a word in bad_words
    # delete_after causes the message to delete after 5 seconds!
    if any(word in message.content.lower() for word in bad_words):
            if message.author.id == 743721232326852628:
                await message.reply(random.choice(in_the_clear),delete_after=10.0)
                return
            else:
                await message.reply(random.choice(bad_responses),delete_after=10.0)
                return

# Below 2 functions will run on a disconnect from wifi, not when CTRL+C is pressed
@client.event
async def on_disconnect():
    # This should run when the discord bot disconnects from the server. At this time I will have it update the swearlist file!
    print('Regular disconnect')
    # We need to update swear list!
    f.close()
    rewriteFile = open('swearlist.txt','w')
    for i in bad_words:
        rewriteFile.write(i.lower()+'\n')
        print(i.lower())
    # Should be perfect

@client.event
async def on_shard_disconnect():
    # This should run when the discord bot disconnects from the server. At this time I will have it update the swearlist file!
    print("Shard Disconnect")
    f.close()
    rewriteFile = open('swearlist.txt','w')
    for i in bad_words:
        rewriteFile.write('\n'+i.lower())
        print ("Writing: " + i.lower + " to file!")
    return

# Helper function for puring bot messages
def is_me(m):
    return m.author == client.user
def is_jt(m):
    return m.author.id == 173748750068482048

client.run(os.getenv('BOT_TOKEN'))



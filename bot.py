# For the bot
import discord

import os
from dotenv import load_dotenv
from tools import *

import unidecode


# For the maths
#import matplotlib.pyplot as plt
#import numpy as np
#import scipy.stats as stats
#import math

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
VERSION = "1.1"

client = discord.Client()

@client.event
async def on_message(message):
    # we do not want the bot to reply to itself, or another bot
    if message.author == client.user:
        return

    channels = ["cours-du-navet"]

    if str(message.channel) in channels:
        # print("Input :"+message.content)

        # Update
        if message.content.startswith('!update'):
            msg=":bell:**New update**:bell:\nWelcome to version "+VERSION+" <@&695628340106756146>\n>> !changelog"

            await message.channel.send(msg)

        # Help
        elif message.content.startswith('!help'):
            msg = ['--------------COMMANDS--------------\n',
                    '`!help` -> list of commands\n',
                    '`!add` **<name> <value>** -> add the value to <name>\'s list  (-1 for no value)\n',
                    '`!change` **<name> <value>** -> change the last value\n',
                    '`!advice` <name> -> give you an advice about when to sell\n',
                    '`!proba` <value> -> probability for the random patterns to offer a price greater or equal to value.\nUse with no value to get an histogram\n'
                    '`!read` <name> / !show <name> -> plot the data of <name>, with some stats\n',
                    '`!changelog` -> print the latest changes to the bot\n',
                    '------------------------------------']
            help_msg =""
            for e in msg:
                help_msg = help_msg+e
            await message.channel.send(help_msg)

        # Print the changelog
        elif message.content.startswith("!changelog"):
            data_file = open("changelog.md",'r')
            lines = data_file.readlines()
            data_file.close()

            res = ""
            for line in lines:
                res+=line
            await message.channel.send(res)

        # Add a value
        elif message.content.startswith('!add'):
            input_values = unidecode.unidecode(message.content[5:].rstrip().lower()).split(" ")
            print("[add]",input_values)
            if len(input_values) == 2:
                input_values[1] = int(input_values[1])
                if add_value(input_values[1],input_values[0]) :
                    await message.channel.send("Error, sorry :(")
                else:
                    await message.channel.send("Done :)")
            else:
                await message.channel.send("Wrong arguments")

        # Change a value
        elif message.content.startswith('!change'):
            input_values = unidecode.unidecode(message.content[8:].rstrip().lower()).split(" ")
            print("[change]",input_values)
            if len(input_values) == 2:
                input_values[1] = int(input_values[1])
                if change_last_value(input_values[1],input_values[0]) :
                    await message.channel.send("Error, sorry :(")
                else:
                    await message.channel.send("Last value changed to {}.".format(input_values[1]))
            else:
                await message.channel.send("Invalid arguments")

        # Say hi to the bot
        elif message.content.startswith('!hello'):
            hommedaffaire = msg.channel.server.roles.mention('name', 'Homme d\'affaires')
            msg = ":bell: "+hommedaffaire.mention()+'\nHello {0.author.mention}'.format(message)
            await message.channel.send(msg)

        # Read data
        elif message.content.startswith('!read') or message.content.startswith('!show'):
            name = unidecode.unidecode(message.content[6:].rstrip().lower())
            print("[read] "+name)

            res=read_data(name)
            if res[0]:
                await message.channel.send("No such name in the database")
            else:
                if name=="all":
                    plot_all()
                else:
                    plot_data(res[1],name)
                await message.channel.send(print_stats(res[1],name), file=discord.File('data-'+name+'.png', 'data.png'))


        # Get some advice for when to sell
        elif message.content.startswith('!advice'):
            name = unidecode.unidecode(message.content[8:].rstrip().lower())
            print("[advice] "+name)
            if name=="all":
                names = get_names()
                for n in names:
                    if not (n=="all" or n=="other"):
                        res=read_data(n)
                        print(pattern(res[1],False))
                        msg = "\n"+n+" : \n"
                        msg+= advice(pattern(res[1],False))
                        await message.channel.send(msg)

            else:
                res=read_data(name)

                if res[0]:
                    await message.channel.send("No such name in the database")
                else:
                    print(pattern(res[1],False))
                    msg = advice(pattern(res[1],False))
                    await message.channel.send(msg)

        # Get some advice for when to sell
        elif message.content.startswith('!proba'):
            val = message.content[7:].rstrip().lower()
            print("[proba] "+val)
            if len(message.content)==6:
                await message.channel.send(plot_proba(), file=discord.File('proba.png', 'proba.png'))
            else:
                try:
                    val = int(val)
                    msg = "Probability to get a selling price above {} until the end of the week :\n {}".format(val,chance(val),"%.4f")
                    await message.channel.send(msg)
                except ValueError:
                    await message.channel.send("Invalid argument")

        # Manage exceptions
        elif message.content == 'raise-exception':
            raise discord.DiscordException

@client.event
async def on_error(event, *args, **kwargs):
    with open('err.log', 'a') as f:
        if event == 'on_message':
            f.write(f'Unhandled message: {args[0]}\n')
        else:
            raise

@client.event
async def on_ready():
    guild = discord.utils.get(client.guilds, name=GUILD)

    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})')
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')
    print('------')
    print("Now listening to cours-du-navet...")

client.run(TOKEN)
# For the bot
import os
from dotenv import load_dotenv
from tools import *

import unidecode


# For the maths
#import matplotlib.pyplot as plt
#import numpy as np
#import scipy.stats as stats
#import math

VERSION = "1.1"
message = input("Commande :")

# print("Input :"+message)

# Update
if message.startswith('!update'):
    msg=":bell:**New update**:bell:\nWelcome to version "+VERSION+"\n!changelog"
    print(msg)

# Help
if message.startswith('!help'):
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
    print(help_msg)

# Print changelog
elif message.startswith("!changelog"):
    data_file = open("changelog.md",'r')
    lines = data_file.readlines()
    data_file.close()

    res = ""
    for line in lines:
        res+=line
    print(res)

# Add a value
elif message.startswith('!add'):
    input_values = unidecode.unidecode(message[5:].rstrip().lower()).split(" ")
    print("[add]",input_values)
    if len(input_values) == 2:
        input_values[1] = int(input_values[1])
        if add_value(input_values[1],input_values[0]) :
            print("Error, sorry :(")
        else:
            print("Done :)")
    else:
        print("Wrong arguments")

# Change a value
elif message.startswith('!change'):
    input_values = unidecode.unidecode(message[8:].rstrip().lower()).split(" ")
    print("[change]",input_values)
    if len(input_values) == 2:
        input_values[1] = int(input_values[1])
        if change_last_value(input_values[1],input_values[0]) :
            print("Error, sorry :(")
        else:
            print("Last value changed to {}.".format(input_values[1]))
    else:
        print("Invalid arguments")

# Say hi to the bot
elif message.startswith('!hello'):
    msg = 'Hello {0.author.mention}'.format(message)
    print(msg)

# Read data
elif message.startswith('!read') or message.startswith('!show'):
    name = unidecode.unidecode(message[6:].rstrip().lower())
    print("[read] "+name)

    res=read_data(name)
    if res[0]:
        print("No such name in the database")
    else:
        if name=="all":
            plot_all()
        else:
            plot_data(res[1],name)
        print(print_stats(res[1],name))


# Get some advice for when to sell
elif message.startswith('!advice'):
	name = unidecode.unidecode(message[8:].rstrip().lower())
	print("[advice] "+name)

	if name=="all":
		names = get_names()
		for n in names:
			if not n=="all":
				res=read_data(n)
				print(pattern(res[1],False))
				msg = advice(pattern(res[1],False))
				print(msg)

	else:
		res=read_data(name)

		if res[0]:
		    print("No such name in the database")
		else:
		    print("This week : ",pattern(res[1],False))
		    msg = advice(pattern(res[1],False))
		    print(msg)

# Get some advice for when to sell
elif message.startswith('!proba'):
    val = message[7:].rstrip().lower()
    print("[proba] "+val)
    if len(message)==6:
        print(plot_proba())
    else:
        try:
            val = int(val)
            msg = "Probability to get a selling price above {} until the end of the week :\n {}".format(val,chance(val),"%.4f")
            print(msg)
        except ValueError:
            print("Invalid argument")

# Manage exceptions
elif message == 'raise-exception':
    raise discord.DiscordException

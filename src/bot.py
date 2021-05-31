import os
import sys
from discord.ext import commands
from dotenv import load_dotenv
from pretty_help import PrettyHelp

bot = commands.Bot(command_prefix='./', help_command=PrettyHelp(sort_commands=True, show_index=False))

''' 
# NEED TO RUN IT WITH ARGUMENT -t for testing
if (len(sys.argv) - 1) != 0 and sys.argv[1] == "-t":
    from distest.patches import patch_target
    bot = patch_target(bot)
else:
    load_dotenv()

TOKEN = os.getenv('TOKEN')
'''
TOKEN = 'ODI3NjExMTgyNzUxOTQwNjE4.YGdi-g.InzJo2uXL_Zez9mnjL4Kys9oyL4'
bot.load_extension("cogs.SQLCog")
bot.load_extension("cogs.BasicCog")
bot.load_extension("cogs.ReactionCog")
bot.run(TOKEN)

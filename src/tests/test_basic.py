import sys

import discord
from distest import TestCollector
from distest import run_dtest_bot
from discord import Embed
import os

TESTER = os.getenv('Tester')
# The tests themselves

test_collector = TestCollector()
created_channel = None


@test_collector()
async def test_scrum(interface):
    await interface.send_message("./Scrum")
    await interface.get_delayed_reply(2, interface.assert_message_equals, 'Master')


@test_collector()
async def test_cool(interface):
    await interface.send_message("./CoolBot")
    await interface.get_delayed_reply(1, interface.assert_message_equals, 'This bot is cool. :)')


@test_collector()
async def test_ping(interface):
    await interface.send_message("ping")
    await interface.get_delayed_reply(1, interface.assert_message_equals, "Pong!")


@test_collector()
async def test_cheers(interface):
    await interface.send_message("hi")
    await interface.get_delayed_reply(1, interface.assert_message_equals, 'Hello there :)')

@test_collector()
async def test_reaction(interface):
    await interface.assert_reaction_equals("ReactionsTestMessage", "👍")


@test_collector()
async def test_dm(interface):
    await interface.send_message("./DM")
    await interface.get_delayed_reply(1, interface.assert_message_equals, "DM sent")


@test_collector()
async def test_removal(interface):
    message = await interface.send_message("Sending Image...")
    await message.channel.send(file=discord.File('src/tests/exPNG.png'))
    check = "Attachment Deleted. \n Please refrain from sending images or code on this channel."

    if await interface.get_delayed_reply(2, interface.assert_message_equals, check):
        await message.channel.send(file=discord.File('src/tests/exPy.py'))
        await interface.get_delayed_reply(2, interface.assert_message_equals, check)

@test_collector()
async def test_poll(interface):
    message = './poll "does the poll test work?" yes no'
    reactions = ['✅', '❌']
    options = ['yes','no']

    description = []
    for x, option in enumerate(options):
        description += '\n{} {}'.format(reactions[x], option)
    embed = Embed(title='does the poll test work?', description=''.join(description))

    await interface.assert_reply_embed_equals(message,embed)



# Actually run the bot

if __name__ == "__main__":
    run_dtest_bot(sys.argv, test_collector)

import asyncio
import datetime

from discord import File, channel
from discord import utils, Embed
from discord.ext import commands


class BasicCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.description = "Some Basic Commands"

    @commands.command(name='CoolBot', brief="Give it a try", description="Give it a try")
    @commands.cooldown(1, 2)
    async def cool_bot(self, ctx):
        await ctx.send('This bot is cool. :)')

    @commands.command(name='Scrum', brief="Give it a try", description="Give it a try")
    async def scrum(self, ctx):
        await ctx.send('Master')

    @commands.command(name='bye', hidden=True)
    async def shutdown(self, ctx):
        await ctx.send('Shutting Down...')
        await asyncio.sleep(3)
        await self.bot.logout()

    # WILL DM THE PERSON WHO INVOKES THE COMMAND
    @commands.command(name="DM", brief="Send a Direct Message to person who called it",
                      description="Send a Direct Message to person who called it")
    @commands.cooldown(1, 2)
    async def dm(self, ctx):
        if not ctx.author.bot:
            await ctx.author.send('BEEP BOOP!')
        await ctx.send('DM sent')

    # MONITORS ALL MESSAGES AND IF CERTAIN PHRASES ARE SAID IT WILL RESPOND.
    # CAN ONLY HAVE ONE LISTENERS (PER COG?)
    @commands.Cog.listener()
    @commands.cooldown(1, 2)
    async def on_message(self, message):
        if message.content.lower() == "hi":
            await message.channel.send('Hello there :)')
            await self.bot.process_commands(message)

        if message.content.lower() == "ping":
            await message.channel.send('Pong!')
            await self.bot.process_commands(message)

        if message.content == "ReactionsTestMessage":
            await message.add_reaction(emoji=u"\U0001F44D")
            await asyncio.sleep(3)
            await message.remove_reaction(member=self.bot.user, emoji=u"\U0001F44D")

            await self.bot.process_commands(message)

        if message.attachments:
            Blacklist = ['c', 'html', 'jpeg', 'css', 'java', 'jpg', 'svg', '.txt', 'docx', 'js', 'py', 'ipynb', 'png',
                         'sql', 'h', 'pdf', 'txt', 'cpp']
            filename = message.attachments[0].filename
            ext = filename.split(".")[-1]
            if ext in Blacklist and not isinstance(message.channel, channel.DMChannel):
                await asyncio.sleep(1)
                await message.delete()
                await message.channel.send("Attachment Deleted. \n Please refrain from sending images or code on this "
                                           "channel.")

                if not message.author.bot:
                    await message.author.send('Please do not send code to the channel, if you need help DM one of the '
                                              'tutors or lecturers.')
                await self.bot.process_commands(message)

    # CLEARS THE CHANNEL COMPLETELY ONLY A PERSON WITH ROLE CAN USE IT
    @commands.command(name="Clear", brief="Clears Messages in Channel",
                      description="Delete x Amount of Messages in Channel \nOnly Users With an Allocated Role can use "
                                  "this Command")
    @commands.cooldown(1, 2)
    # @commands.has_role("")
    async def clear(self, ctx, amount=5):
        await ctx.channel.purge(limit=amount)

    @commands.command(name="Register", brief="Sends a list to the tutor of presents tutors",
                      description="Get a list of people who is present in the voice channel",
                      aliases=["Reg", "reg", "register", "pres", "present"])
    @commands.cooldown(1, 2)
    async def Register(self, ctx):

        role = utils.find(lambda r: r.name == 'tutor' or r.name == 'Tutor', ctx.message.guild.roles)
        members = []
        tutor = []
        try:
            voice_channel = ctx.message.author.voice.channel
            member_list = voice_channel.members
            for i in member_list:
                if role not in i.roles:
                    members.append(i)
                else:
                    tutor.append(i)
        except:
            await ctx.send("You're not in a voice channel")

        file_path = r"../src/csv/Register.txt"
        f = open(file_path, "w")

        date_time = datetime.datetime.now()
        date = date_time.strftime("%d/%m/%Y, %H:%M:%S")
        f.write(date)
        f.write('\n')

        f.write("Tutor: ")
        sep = ""
        for t in tutor:
            f.write(t.name + sep)
            sep = "&"
        f.write("\n\n")

        f.write("Present: \n")

        for m in members:
            f.write(m.name)
            f.write("\n")
        f.close()
        file_name = ctx.guild.name + " " + date_time.strftime("%d/%m/%Y")
        await ctx.author.send(file=File(file_path, filename=file_name))

    # Allows user to create a poll for people to vote on.
    @commands.command(name="Poll", aliases=["poll"])
    async def poll(self, ctx, question, *options: str):
        if len(options) <= 1:
            await ctx.send('You need more than one option to make a poll!')
            return
        if len(options) > 10:
            await ctx.send('You cannot make a poll for more than 10 things!')
            return

        if len(options) == 2 and options[0] == 'yes' and options[1] == 'no':
            reactions = ['✅', '❌']
        else:
            reactions = ['1⃣', '2⃣', '3⃣', '4⃣', '5⃣', '6⃣', '7⃣', '8⃣', '9⃣', '🔟']

        description = []
        for x, option in enumerate(options):
            description += '\n{} {}'.format(reactions[x], option)
        embed = Embed(title=question, description=''.join(description))
        react_message = await ctx.send(embed=embed)
        for react in reactions[:len(options)]:
            await react_message.add_reaction(react)

    # Detects when a reaction is added to a message
    @commands.Cog.listener()
    @commands.cooldown(1, 2)
    async def on_raw_reaction_add(self, payload):  # checks whenever a reaction is added to a message
        # whether the message is in the cache or not

        channel = await self.bot.fetch_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)

        # iterating through each reaction in the message
        for r in message.reactions:

            # checks the reactant isn't a bot and the emoji isn't the one they just reacted with
            if payload.member in await r.users().flatten() and not payload.member.bot and str(r) != str(payload.emoji):
                # removes the reaction
                await message.remove_reaction(r.emoji, payload.member)


def setup(bot):
    bot.add_cog(BasicCog(bot))

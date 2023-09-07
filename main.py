# Project: EngBuddy / Bot Created By: Sahaj Singh / Release V1.1

from discord.ext import commands
from discord import app_commands
from utils.embed import embed
import discord
import openai
import requests
import time
import re
import json
import html
import aiohttp
import sqlite3
import random
import subprocess
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')
token = os.getenv('DISCORD_TOKEN')

sfu_red = 0xA6192E
rateProf = 0x0055FD
courseDigger = 0xE4bC0C
dalle_api_endpoint = "https://api.openai.com/v1/images/generations"
client = commands.Bot(command_prefix="!", intents=discord.Intents.all())
whitelist = []
messages = [
    "Don’t do anything stupid.",
    "I wouldn’t do that if I were you.",
    "Try me.",
    "Sit down and shut up.",
    "We’re not so different, you and I.",
    "Get outta there!",
    "Is that all you’ve got?",
    "Yeah, you better run!",
    "I am your father.",
    "There’s a storm coming.",
    "You look like shit.",
    "We can do this the easy way, or the hard way.",
    "You just don’t get it, do you?",
    "You're acting like a crazy person.",
    "Surprise Motherfucker!",
    "I'm just getting started.",
    "I'm going to enjoy watching you die."
]
previous_message = None


@client.event
async def on_ready():
    try:
        await populate()
        await client.change_presence(activity=discord.Game(name="MATLAB"))
        await client.tree.sync()
    except Exception as e:
        print(f"Something went wrong: {e}")
        exit()


@client.command()
async def add(ctx, *, id_value=None):
    if id_value is not None:
        if ctx.message.author.id == 484395342859862017:
            await add_new_id(id_value)
            user = await client.fetch_user(id_value)
            me = await client.fetch_user(484395342859862017)
            await user.send(f"You have been added to the whitelist by {ctx.author.name}")
            await me.send(f"{user.name}#{user.discriminator} has been added to the whitelist.")
        else:
            await ctx.message.author.send(f"Nice try buddy guy {ctx.author.mention}")


async def shutdown_bot():
    me = await client.fetch_user(484395342859862017)
    await me.send("Going to recharge my batteries!")
    await client.close()


@client.command()
async def kill(ctx):
    if ctx.message.author.id == 484395342859862017:
        await shutdown_bot()
    else:
        await ctx.message.author.send(f"Nice try buddy guy {ctx.author.mention}")


@client.tree.command(name="help", description="Information about available commands")
async def help_func(interaction: discord.Interaction):
    embed_holder = discord.Embed(title="My Commands", description="Here are the slash commands you can use with me:",
                                 color=0x4169e1)
    embed_holder.add_field(name="", value="", inline=False)
    embed_holder.add_field(
        name="about", value="Let me tell you about myself!", inline=False)
    embed_holder.add_field(
        name="resource", value="Here are a few resources you can use!", inline=False)
    embed_holder.add_field(
        name="ask", value="Ask me something and I will respond to the best of my ability. *Restricted Use for Now - Ask Sahaj for PERMS", inline=False)
    embed_holder.add_field(
        name="imagine", value="Ask me make an image and I will create one! *Restricted Use for Now - Ask Sahaj for PERMS", inline=False)
    embed_holder.add_field(
        name="sfu", value="Information about available sfu classes.", inline=False)
    embed_holder.add_field(
        name="outline", value="Outline of an available sfu classes.", inline=False)
    embed_holder.add_field(
        name="rate_prof", value="I will pull an available rating of the prof.", inline=False)
    embed_holder.add_field(
        name="rate_course", value="I will pull an available rating of the course.", inline=False)
    embed_holder.add_field(
        name="echo", value="Returns the provided argument.", inline=False)
    embed_holder.add_field(
        name="arcade", value="Ask me what game is being played on the arcade machine. *Under development for Now", inline=False)
    embed_holder.add_field(
        name="others", value="I also have some secrets for you to discover.", inline=False)
    await interaction.response.send_message(embed=embed_holder, ephemeral=True)


@client.tree.command(name="arcade", description="Ask me what game is being played on the arcade machine!")
@app_commands.describe(visibility="Options: private, public or dm")
async def arcade(interaction: discord.Interaction, *, visibility: str = None):
    if interaction.user.id not in whitelist:
        me = await client.fetch_user(484395342859862017)
        await me.send(f"{interaction.user.name}#{interaction.user.discriminator} tried to use the imagine command.")
        await interaction.response.send_message("You dont have access. Ask Sahaj for access!", ephemeral=True)
        return
    if visibility is not None:
        if remove_spaces(visibility.lower()) == "private":
            selector = True
        elif remove_spaces(visibility.lower()) == "public":
            selector = False
        else:
            selector = False
    else:
        selector = False
    await interaction.response.defer(ephemeral=selector)
    if is_emulator_running():
        try:
            with open("/dev/shm/runcommand.log", "r") as f:
                runcommand_log = f.read()

            rom_path_match = re.search(
                r'(?<=/roms/).*\.(amstradcpc|atari2600|atari7800|atarilynx|coleco|fds|gb|gbc|mame-libretro|megadrive'
                r'|n64|nes|ngpc|psp|sega32x|sg-1000|vectrex|arcade|atari5200|atari800|channelf|fba|gamegear|gba'
                r'|genesis|mastersystem|msx|neogeo|ngp|pcengine|psx|segacd|snes|zxspectrum|iso)',
                runcommand_log)

            if rom_path_match:
                rom_path = rom_path_match.group(0)
                game_name = rom_path.split(
                    "/")[-1].split(".")[0].split("(")[0].split("[")[0].strip()
                if rom_path.split("/")[-2] == "psp":
                    game_name = re.sub(r'^\d{4} - ', '', game_name)

                await interaction.followup.send("Currently running game:", game_name)
            else:
                await interaction.followup.send("No game currently running.")
        except Exception as e:
            print("Error:", e)
            await interaction.followup.send("No game currently running.")
    else:
        await interaction.followup.send("No game currently running.")


@client.tree.command(name="resource", description="Here are a few resources you can use!")
@app_commands.describe(visibility="Options: private, public or dm")
async def resource(interaction: discord.Interaction, *, visibility: str = None):
    # Create a new embed object for resources
    resource_embed = discord.Embed(title="ESSS Resources",
                                   description="Useful links for ESSS members!\u200B",
                                   color=0x4169e1)
    resource_embed.add_field(
        name="Common Room", value="ASB8842: ESSS Common Room", inline=False)
    resource_embed.add_field(
        name="Office", value="ASB8834: ESSS Office", inline=False)
    resource_embed.add_field(name="", value="", inline=False)
    resource_embed.add_field(name="", value="", inline=False)

    # Course Planning & SFU MATLAB Facebook
    resource_embed.add_field(
        name="📚 Course Resources", value="", inline=False)
    resource_embed.add_field(
        name="Course Planning", value="[sfu.coursenavigator.ca](https://sfu.coursenavigator.ca/) 🤠", inline=False)
    resource_embed.add_field(name="SFU MATLAB Facebook",
                             value="[Facebook Group](https://www.facebook.com/groups/sfumatlab)", inline=False)
    resource_embed.add_field(name="SFU MATLAB Intagream",
                             value="[Facebook Group](https://www.instagram.com/sfu_matlab/)", inline=False)
    resource_embed.add_field(name="", value="", inline=False)
    resource_embed.add_field(name="", value="", inline=False)

    # ESSS Social Media
    resource_embed.add_field(
        name="📱 ESSS Social Media", value="", inline=False)
    resource_embed.add_field(
        name="Linktree", value="[linktr.ee/sfuesss](https://linktr.ee/sfuesss)", inline=True)
    resource_embed.add_field(
        name="Website", value="[sfu.ca/esss](http://www.esss.ca)", inline=True)
    resource_embed.add_field(
        name="Instagram", value="[Instagram](https://www.instagram.com/sfuengineers)", inline=True)
    resource_embed.add_field(
        name="Facebook", value="[Facebook](https://www.facebook.com/SFU.ESSS)", inline=True)
    resource_embed.add_field(
        name="LinkedIn", value="[LinkedIn](https://www.linkedin.com/company/sfu-engineering-science-student-society)", inline=True)
    resource_embed.add_field(
        name="Twitter", value="[Twitter](https://twitter.com/sfuengineering)", inline=True)
    resource_embed.add_field(name="", value="", inline=False)
    resource_embed.add_field(name="", value="", inline=False)

    # Free Software
    resource_embed.add_field(
        name="💻 Free Software", value="", inline=False)
    resource_embed.add_field(
        name="Altium Designer", value="[altium.com](https://www.altium.com/education/student-licenses)", inline=True)
    resource_embed.add_field(name="SFU Software Catalogue (MATLAB)(SOLIDWORKS)",
                             value="[sfu.ca](https://www.sfu.ca/information-systems/services/software.html)", inline=True)
    resource_embed.add_field(name="Autodesk (AutoCAD)(Fusion 360)",
                             value="[autodesk.com](https://www.autodesk.com/education/edu-software/overview?sorting=featured&filters=individual)", inline=True)
    resource_embed.add_field(
        name="Zemax OpticStudio", value="[zemax.com](https://academic.zemax.com/student-application/)", inline=True)
    resource_embed.add_field(name="", value="", inline=False)
    resource_embed.add_field(name="", value="", inline=False)

    # Affiliates and Design Teams
    resource_embed.add_field(
        name="🤝 Affiliates and Design Teams", value="", inline=False)
    resource_embed.add_field(
        name="WiE", value="[Discord](https://discord.gg/NdmbAMhVHY)", inline=True)
    resource_embed.add_field(
        name="WiE Design", value="[Discord](https://discord.gg/YX45E9Cr7j)", inline=True)
    resource_embed.add_field(
        name="Robot Soccer", value="[Discord](https://discord.gg/Hyc48DJSEU)", inline=False)
    resource_embed.add_field(
        name="Team Phantom", value="[teamphantom.ca](https://www.teamphantom.ca/)", inline=False)
    resource_embed.add_field(name="", value="", inline=False)
    resource_embed.add_field(name="", value="", inline=False)

    # Course and Cohort Server Catalogue
    resource_embed.add_field(
        name="🏫 Course and Cohort Server Catalogue", value="", inline=False)
    resource_embed.add_field(
        name="Year 3 Term 1", value="[Discord](https://discord.gg/tJgJU3wtGp)", inline=True)
    resource_embed.add_field(
        name="FAS First Years", value="[Discord](https://discord.gg/nu9QUYxfbE)", inline=True)
    resource_embed.add_field(name="", value="", inline=False)
    resource_embed.add_field(name="", value="", inline=False)

    # Handling visibility based on your previous code
    dm = False
    if visibility is not None:
        if remove_spaces(visibility.lower()) == "private":
            selector = True
        elif remove_spaces(visibility.lower()) == "public":
            selector = False
        elif remove_spaces(visibility.lower()) == "dm":
            selector = False
            dm = True
        else:
            selector = True
    else:
        selector = True

    await interaction.response.defer(ephemeral=selector)
    try:
        if dm:
            await interaction.user.send(embed=resource_embed)
            await interaction.followup.send("Please check your DM! BTW You can talk to me directly in DMs!")
        else:
            await interaction.followup.send(embed=resource_embed)
    except Exception as e:
        print(f"Something went wrong: {e}")
        await interaction.followup.send("Sorry, I couldn't send the resource information.")


@client.tree.command(name="imagine", description="Ask me to make an image!")
@app_commands.describe(prompt="Ask me to make an image!")
@app_commands.describe(visibility="Options: private, public or dm")
async def imagine(interaction: discord.Interaction, *, prompt: str, visibility: str = None):
    if interaction.user.id not in whitelist:
        me = await client.fetch_user(484395342859862017)
        await me.send(f"{interaction.user.name}#{interaction.user.discriminator} tried to use the imagine command.")
        await interaction.response.send_message("You dont have access. Ask Sahaj for access!", ephemeral=True)
        return
    dm = False
    if visibility is not None:
        if remove_spaces(visibility.lower()) == "private":
            selector = True
        elif remove_spaces(visibility.lower()) == "public":
            selector = False
        elif remove_spaces(visibility.lower()) == "dm":
            selector = False
            dm = True
        else:
            selector = True
    else:
        selector = True
    await interaction.response.defer(ephemeral=selector)

    headers = {"Authorization": f"Bearer {openai.api_key}"}
    data = {
        "model": "image-alpha-001",
        "prompt": prompt,
        "num_images": 1,
        "size": "1024x1024",
        "response_format": "url"
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(dalle_api_endpoint, headers=headers, json=data) as response:
            if response.status == 200:
                response_json = await response.json()
                image_url = response_json["data"][0]["url"]
                if dm:
                    await interaction.user.send(image_url)
                    await interaction.followup.send("Please check your DM! BTW You can talk to me directly in DMS!")
                else:
                    await interaction.followup.send(image_url)
            else:
                await interaction.followup.send("Sorry something went wrong generating your image.")


@client.tree.command(name="ask", description="Ask me something!")
@app_commands.describe(question="Ask me something!")
@app_commands.describe(visibility="Options: private, public or dm")
async def ask(interaction: discord.Interaction, *, question: str, visibility: str = None):
    if interaction.user.id not in whitelist:
        me = await client.fetch_user(484395342859862017)
        await me.send(f"{interaction.user.name}#{interaction.user.discriminator} tried to use the ask command.")
        await interaction.response.send_message("You dont have access. Ask Sahaj for access!", ephemeral=True)
        return
    dm = False
    if visibility is not None:
        if remove_spaces(visibility.lower()) == "private":
            selector = True
        elif remove_spaces(visibility.lower()) == "public":
            selector = False
        elif remove_spaces(visibility.lower()) == "dm":
            selector = False
            dm = True
        else:
            selector = True
    else:
        selector = True
    await interaction.response.defer(ephemeral=selector)
    try:
        response = await chatgpt_call(question)
        if dm:
            await interaction.user.send(f'Prompt: {question}\n\n Response: {response}')
            await interaction.followup.send("Please check your DM! BTW You can talk to me directly in DMS!")
        else:
            await interaction.followup.send(f'Prompt: {question}\n\n Response: {response}')
    except openai.OpenAIError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Something went wrong: {e}")
        await interaction.followup.send("Sorry, I couldn't generate a response for that question.")


@client.tree.command(name="echo", description="Returns the provided argument!")
@app_commands.describe(argument="Returns the provided argument")
async def echo(interaction: discord.Interaction, *, argument: str):
    await interaction.response.send_message(argument, ephemeral=False)


@client.tree.command(name="about", description="Let me tell you about myself!")
async def about(interaction: discord.Interaction):
    embed_holder = discord.Embed(title="About Me!", description="Here is a little info about me:",
                                 color=0x4169e1)
    embed_holder.set_thumbnail(url=client.user.avatar.url)
    embed_holder.add_field(name="", value="", inline=False)
    embed_holder.add_field(
        name=f'Hey there, My Name is {client.user.name}!', value='', inline=True)
    embed_holder.add_field(name='Description:',
                           value='EngBuddy is your personal engineering assistant available 24/7 on the '
                                 'ESSS Discord server. With its advanced AI capabilities, '
                                 'EngBuddy provides personalized support to help you succeed in your '
                                 'studies and build meaningful connections with your peers.',
                           inline=False)
    embed_holder.add_field(
        name='For more information: Invoke the help slash command!', value='', inline=True)
    await interaction.response.send_message(embed=embed_holder, ephemeral=True)


@client.tree.command(name="sfu", description="Information about available sfu classes")
@app_commands.describe(course="Information about available sfu classes")
@app_commands.describe(visibility="Options: private or public")
async def sfu(interaction: discord.Interaction, *, course: str, visibility: str = None):
    if visibility is not None:
        if remove_spaces(visibility.lower()) == "private":
            selector = True
        elif remove_spaces(visibility.lower()) == "public":
            selector = False
        else:
            selector = False
    else:
        selector = False
    await interaction.response.defer(ephemeral=selector)
    if not course:
        e_obj = await embed(
            interaction,
            title='Invalid Arguments',
            author=client.user.name,
            avatar=client.user.avatar.url,
            colour=sfu_red,
            content=[['Usage', '`/sfu <arg>`'], ['Example', '`/sfu ensc252`']],
            footer='SFU Error'
        )
        if e_obj is not False:
            await interaction.followup.send(embed=e_obj)
        return

    year = time.localtime()[0]
    term = time.localtime()[1]

    if term <= 4:
        term = 'spring'
    elif 5 <= term <= 8:
        term = 'summer'
    else:
        term = 'fall'

    # Check if arg needs to be manually split
    course = remove_spaces(course)
    if len(course) == 1:
        # split
        crs = re.findall(r'(\D+)(\d+)', course[0])

        if len(crs) < 1:
            # Bad args
            e_obj = await embed(
                interaction,
                title='Bad Arguments',
                author=client.user.name,
                avatar=client.user.avatar.url,
                colour=sfu_red,
                content=[['Usage', '`/sfu <arg>`'],
                         ['Example', '`/sfu ensc252`']],
                footer='SFU Error'
            )
            if e_obj is not False:
                await interaction.followup.send(embed=e_obj)
            return

        course_code = crs[0][0].lower()
        course_num = crs[0][1].lower()
    else:
        crs = re.findall(r'(\D+)(\d+)', course)

        if len(crs) < 1:
            # Bad args
            e_obj = await embed(
                interaction,
                title='Bad Arguments',
                author=client.user.name,
                avatar=client.user.avatar.url,
                colour=sfu_red,
                content=[['Usage', '`/sfu <arg>`'],
                         ['Example', '`/sfu ensc252`']],
                footer='SFU Error'
            )
            if e_obj is not False:
                await interaction.followup.send(embed=e_obj)
            return

        course_code = crs[0][0].lower()
        course_num = crs[0][1].lower()

    url = 'http://www.sfu.ca/bin/wcm/academic-calendar?{0}/{1}/courses/{2}/{3}'.format(year, term, course_code,
                                                                                       course_num)
    async with aiohttp.ClientSession() as req:
        res = await req.get(url)
        if res.status == 200:
            data = ''
            while True:
                chunk = await res.content.read(10)
                if not chunk:
                    break
                data += str(chunk.decode())
            data = json.loads(data)
        else:
            e_obj = await embed(
                interaction,
                title=f'Results from SFU for {course}',
                author=client.user.name,
                avatar=client.user.avatar.url,
                colour=sfu_red,
                description=(
                    'Couldn\'t find anything for:\n{0}/{1}/{2}/{3}/\nMake sure you entered all the arguments '
                    'correctly').format(
                    year,
                    term.upper(),
                    course_code.upper(),
                    course_num
                ),
                footer='SFU Error'
            )
            if e_obj is not False:
                await interaction.followup.send(embed=e_obj)
            return

    sfu_url = 'http://www.sfu.ca/students/calendar/{0}/{1}/courses/{2}/{3}.html'.format(year, term, course_code,
                                                                                        course_num)
    img = 'http://www.sfu.ca/content/sfu/clf/jcr:content/main_content/image_0.img.1280.high.jpg' \
          '/1468454298527.jpg'
    link = '[here]({})'.format(sfu_url)
    footer = 'Written by EngBuddy'

    fields = [
        [data['title'], data['description']],
        ["URL", link]
    ]

    embed_obj = await embed(
        interaction,
        title=f'Results from SFU for {course}',
        author=client.user.name,
        avatar=client.user.avatar.url,
        content=fields,
        colour=sfu_red,
        thumbnail=img,
        footer=footer
    )
    if embed_obj is not False:
        await interaction.followup.send(embed=embed_obj)


@client.tree.command(name="outline", description="Outline of an available sfu classes")
@app_commands.describe(course="Outline of an available sfu classes")
@app_commands.describe(visibility="Options: private or public")
async def outline(interaction: discord.Interaction, *, course: str, visibility: str = None):
    if visibility is not None:
        if remove_spaces(visibility.lower()) == "private":
            selector = True
        elif remove_spaces(visibility.lower()) == "public":
            selector = False
        else:
            selector = False
    else:
        selector = False
    await interaction.response.defer(ephemeral=selector)
    course_value = course
    usage = [
        ['Usage', '`/outline <course> [<term> <section> next]`\n*<term>, <section>, and next are optional ar'
                  'guments*\nInclude the keyword `next` to look at the next semester\'s outline. Note: `next` is'
                  ' used for course registration purposes and if the next semester info isn\'t available it\'ll '
                  'return an error.'],
        ['Example', '`/outline ensc252\n/outline ensc252 fall\n/outline ensc252 d200\n/outline ensc252'
                    ' spring d200\n/outline ensc252 next`']]

    if not course:
        e_obj = await embed(
            interaction,
            title='Invalid Arguments',
            author=client.user.name,
            avatar=client.user.avatar.url,
            colour=sfu_red,
            content=usage,
            footer='SFU Outline Error'
        )
        if e_obj is not False:
            await interaction.followup.send(embed=e_obj)
        return
    course = course.split()
    if 'next' in course:
        year = 'registration'
        term = 'registration'
        course.remove('next')
    else:
        year = 'current'
        term = 'current'

    section = ''

    arg_num = len(course)

    if arg_num > 1 and course[1][:len(course[1]) - 1].isdigit():
        # User gave course in two parts
        course_code = course[0].lower()
        course_num = course[1].lower()
        course = course[:1] + course[2:]
        arg_num = len(course)
    else:
        # Split course[0] into parts
        crs = re.findall(r'(\d*\D+)', course[0])
        if len(crs) < 2:
            # this incase the course num doesn't end in a letter, need to
            crs = re.split(r'(\d+)', course[0])
            # split with different regex

        if len(crs) < 2:
            # Bad args
            e_obj = await embed(
                interaction,
                title='Bad Arguments',
                author=client.user.name,
                avatar=client.user.avatar.url,
                colour=sfu_red,
                content=usage,
                footer='SFU Outline Error'
            )
            if e_obj is not False:
                await interaction.followup.send(embed=e_obj)
            return

        course_code = crs[0].lower()
        course_num = crs[1]

    # Course and term or section is specified
    if arg_num == 2:
        # Figure out if section or term was given
        temp = course[1].lower()
        if temp[3].isdigit():
            section = temp
        elif term != 'registration':
            if temp == 'fall':
                term = temp
            elif temp == 'summer':
                term = temp
            elif temp == 'spring':
                term = temp

    # Course, term, and section is specified
    elif arg_num == 3:
        # Check if last arg is section
        if course[2][3].isdigit():
            section = course[2].lower()
        if term != 'registration':
            if course[1] == 'fall' or course[1] == 'spring' or course[1] == 'summer':
                term = course[1].lower()
            else:
                # Send something saying be in this order
                e_obj = await embed(
                    interaction,
                    title='Bad Arguments',
                    author=client.user.name,
                    avatar=client.user.avatar.url,
                    colour=sfu_red,
                    description=(
                        'Make sure your arguments are in the following order:\n<course> '
                        '<term> <section>\nexample: `/outline ensc252 fall d200`\n term and section'
                        ' are optional args'
                    ),
                    footer='SFU Outline Error'
                )
                if e_obj is not False:
                    await interaction.followup.send(embed=e_obj)
                return

    # Set up url for get
    if section == '':
        # get req the section
        async with aiohttp.ClientSession() as req:
            res = await req.get('http://www.sfu.ca/bin/wcm/course-outlines?{0}/{1}/{2}/{3}'.format(year, term,
                                                                                                   course_code,
                                                                                                   course_num))
            if res.status == 200:
                data = ''
                while not res.content.at_eof():
                    chunk = await res.content.readchunk()
                    data += str(chunk[0].decode())
                res = json.loads(data)
                for x in res:
                    if x['sectionCode'] in ['LEC', 'LAB', 'TUT', 'SEM']:
                        section = x['value']
                        break
            else:
                e_obj = await embed(
                    interaction,
                    title='SFU Course Outlines',
                    author=client.user.name,
                    avatar=client.user.avatar.url,
                    colour=sfu_red,
                    description=(
                        'Couldn\'t find anything for `{} {}`\n Maybe the course doesn\'t exist? '
                        'Or isn\'t offered right now.'.format(
                            course_code.upper(),
                            str(course_num).upper()
                        )
                    ),
                    footer='SFU Outline Error'
                )
                if e_obj is not False:
                    await interaction.followup.send(embed=e_obj)
                return

    url = 'http://www.sfu.ca/bin/wcm/course-outlines?{0}/{1}/{2}/{3}/{4}'.format(year, term, course_code,
                                                                                 course_num, section)

    async with aiohttp.ClientSession() as req:
        res = await req.get(url)
        if res.status == 200:
            data = ''
            while not res.content.at_eof():
                chunk = await res.content.readchunk()
                data += str(chunk[0].decode())

            data = json.loads(data)
        else:
            e_obj = await embed(
                interaction,
                title='SFU Course Outlines',
                author=client.user.name,
                avatar=client.user.avatar.url,
                colour=sfu_red,
                description=(
                    'Couldn\'t find anything for `{} {}`\n Maybe the course doesn\'t exist? Or isn\'t '
                    'offered right now.'.format(
                        course_code.upper(), str(course_num).upper())
                ),
                footer='SFU Outline Error'
            )
            if e_obj is not False:
                await interaction.followup.send(embed=e_obj)
            return

        try:
            # Main course information
            info = data['info']

            # Course schedule information
            schedule = data['courseSchedule']
        except (Exception,):
            e_obj = await embed(
                interaction,
                title='SFU Course Outlines',
                author=client.user.name,
                avatar=client.user.avatar.url,
                colour=sfu_red,
                description=(
                    'Couldn\'t find anything for `{} {}`\n Maybe the course doesn\'t exist? Or isn\'t offered '
                    'right now.'.format(course_code.upper(), str(course_num).upper())),
                footer='SFU Outline Error')
            if e_obj is not False:
                await interaction.followup.send(embed=e_obj)
            return

        outline_value = info['outlinePath'].upper()
        title = info['title']
        try:
            instructor = ''
            instructors = data['instructor']
            for prof in instructors:
                instructor += prof['name']
                instructor += ' [{}]\n'.format(prof['email'])
        except (Exception,):
            instructor = 'TBA'

        # Course schedule info parsing
        crs = ''
        for x in schedule:
            # [LEC] days time, room, campus
            sec_code = '[{}]'.format(x['sectionCode'])
            days = x['days']
            tme = '{}-{}'.format(x['startTime'], x['endTime'])
            room = '{} {}'.format(x['buildingCode'], x['roomNumber'])
            campus = x['campus']
            crs = '{}{} {} {}, {}, {}\n'.format(
                crs, sec_code, days, tme, room, campus)

        class_times = crs

        # Exam info
        exam_times = 'TBA'
        ''
        ''
        ''
        try:
            # Course might not have an exam
            tim = '{}-{}'.format(data['examSchedule'][0]
                                 ['startTime'], data['examSchedule'][0]['endTime'])
            date = data['examSchedule'][0]['startDate'].split()
            date = '{} {} {}'.format(date[0], date[1], date[2])

            exam_times = '{} {}'.format(tim, date)

            # Room info much later
            room_info = (
                '{} {}, {}'.format(
                    data['examSchedule'][0]['buildingCode'],
                    data['schedule']['roomNumber'],
                    data['examSchedule'][0]['campus']
                )
            )
            exam_times += '\n{}'.format(room_info)
        except (Exception,):
            pass
        # Other details
        # need to cap len for details
        description = data['info']['description']
        try:
            details = html.unescape(data['info']['courseDetails'])
            details = re.sub('<[^<]+?>', '', details)
            if len(details) > 200:
                details = '{}\n(...)'.format(details[:200])
        except (Exception,):
            details = 'None'
        try:
            prerequisites = data['info']['prerequisites'] or 'None'
        except (Exception,):
            prerequisites = 'None'

        try:
            corequisites = data['info']['corequisites']
        except (Exception,):
            corequisites = ''

        url = 'http://www.sfu.ca/outlines.html?{}'.format(
            data['info']['outlinePath'])
        # Make tuple of the data for the fields
        fields = [
            ['Outline', outline_value],
            ['Title', title],
            ['Instructor', instructor],
            ['Class Times', class_times],
            ['Exam Times', exam_times],
            ['Description', description],
            ['Details', details],
            ['Prerequisites', prerequisites]
        ]

        if corequisites:
            fields.append(['Corequisites', corequisites])
        fields.append(['URL', '[here]({})'.format(url)])
        img = 'http://www.sfu.ca/content/sfu/clf/jcr:content/main_content/image_0.img.1280.high.jpg/1468454298527.jpg'
        e_obj = await embed(
            interaction,
            title=f'SFU Outline Results for {course_value}',
            author=client.user.name,
            avatar=client.user.avatar.url,
            colour=sfu_red,
            thumbnail=img,
            content=fields,
            footer='Written by EngBuddy'
        )
        if e_obj is not False:
            await interaction.followup.send(embed=e_obj)


@client.tree.command(name="rate_prof", description="I will pull an available rating of the prof")
@app_commands.describe(name="Provide the name of the prof")
@app_commands.describe(visibility="Options: private or public")
async def rate_prof(interaction: discord.Interaction, *, name: str, visibility: str = None):
    if visibility is not None:
        if remove_spaces(visibility.lower()) == "private":
            selector = True
        elif remove_spaces(visibility.lower()) == "public":
            selector = False
        else:
            selector = False
    else:
        selector = False
    await interaction.response.defer(ephemeral=selector)
    if not name:
        e_obj = await embed(
            interaction,
            title='Invalid Arguments',
            author=client.user.name,
            avatar=client.user.avatar.url,
            colour=rateProf,
            content=[['Usage', '`/rate_prof <arg>`'],
                     ['Example', '`/rate_prof Craig Scratchley`']],
            footer='rateProf Error'
        )
        if e_obj is not False:
            await interaction.followup.send(embed=e_obj)
        return

    # Check if there is a space in the name
    if len(name.split()) < 2:
        e_obj = await embed(
            interaction,
            title='Invalid Arguments:\nFirst and Last name Required',
            author=client.user.name,
            avatar=client.user.avatar.url,
            colour=rateProf,
            content=[['Usage', '`/rate_prof <arg>`'],
                     ['Example', '`/rate_prof Craig Scratchley`']],
            footer='rateProf Error'
        )
        if e_obj is not False:
            await interaction.followup.send(embed=e_obj)
        return

    url = "https://www.ratemyprofessors.com/search/professors/{}?q={}"
    prof_name = name.replace(" ", "+")
    univ_id = 1482
    search_url = url.format(univ_id, prof_name)
    response = requests.get(search_url)
    if response.status_code != 200:
        e_obj = await embed(
            interaction,
            title='No Response:\nPlease Try Again',
            author=client.user.name,
            avatar=client.user.avatar.url,
            colour=rateProf,
            content=[['Usage', '`/rate_prof <arg>`'],
                     ['Example', '`/rate_prof Craig Scratchley`']],
            footer='rateProf Error'
        )
        if e_obj is not False:
            await interaction.followup.send(embed=e_obj)
        return
    else:
        match = re.search(
            r'window\.__RELAY_STORE__\s*=\s*(\{.*});', response.text)
        if not match:
            e_obj = await embed(
                interaction,
                title='No Match Found:\nPlease Try Again',
                author=client.user.name,
                avatar=client.user.avatar.url,
                colour=rateProf,
                content=[['Usage', '`/rate_prof <arg>`'],
                         ['Example', '`/rate_prof Craig Scratchley`']],
                footer='rateProf Error'
            )
            if e_obj is not False:
                await interaction.followup.send(embed=e_obj)
            return
        else:
            data = json.loads(match.group(1))
            professor_data = []
            for key, value in data.items():
                if 'legacyId' in json.dumps(value):
                    legacy_id = str(value['legacyId'])
                    avg_rating = str(value['avgRating'])
                    num_ratings = str(value['numRatings'])
                    would_take_again_percent = str(
                        value['wouldTakeAgainPercent'])
                    avg_difficulty = str(value['avgDifficulty'])
                    first_name = str(value['firstName'])
                    last_name = str(value['lastName'])
                    department = str(value['department'])
                    rmp_url = 'https://www.ratemyprofessors.com/professor/{0}'.format(
                        legacy_id)
                    link = '[here]({})'.format(rmp_url)
                    fields = [
                        ['Name', first_name + " " + last_name],
                        ['Department', department],
                        ['Rating', avg_rating],
                        ['Number of Ratings', num_ratings],
                        ['Difficulty', avg_difficulty],
                        ['Would Take Again', would_take_again_percent],
                        ['Url', link]
                    ]
                    professor_data.append(tuple(fields))
                    img = 'http://www.sfu.ca/content/sfu/clf/jcr:content/main_content/image_0.img.1280.high.jpg' \
                          '/1468454298527.jpg'
                    e_obj = await embed(
                        interaction,
                        title=f'RateMyProf Results: ',
                        author=client.user.name,
                        avatar=client.user.avatar.url,
                        colour=rateProf,
                        thumbnail=img,
                        content=fields,
                        footer='Written by EngBuddy'
                    )
                    if e_obj is not False:
                        await interaction.followup.send(embed=e_obj)
            if len(professor_data) == 0:
                e_obj = await embed(
                    interaction,
                    title='No Response:\nPlease Try Again',
                    author=client.user.name,
                    avatar=client.user.avatar.url,
                    colour=rateProf,
                    content=[['Usage', '`/rate_prof <arg>`'],
                             ['Example', '`/rate_prof Craig Scratchley`']],
                    footer='rateProf Error'
                )
                if e_obj is not False:
                    await interaction.followup.send(embed=e_obj)
                return


@client.tree.command(name="rate_course", description="I will pull an available rating of the course")
@app_commands.describe(course="Provide the name of the course")
@app_commands.describe(visibility="Options: private or public")
async def rate_course(interaction: discord.Interaction, *, course: str, visibility: str = None):
    if visibility is not None:
        if remove_spaces(visibility.lower()) == "private":
            selector = True
        elif remove_spaces(visibility.lower()) == "public":
            selector = False
        else:
            selector = False
    else:
        selector = False
    await interaction.response.defer(ephemeral=selector)
    course = course.upper()
    match = re.match(r'(\D+)(\d+)', course)
    if match:
        course_name = match.group(1).upper()  # Capitalize the alphabetic part
        course_number = match.group(2)
        search_course = '{} {}'.format(remove_spaces(
            course_name), remove_spaces(course_number))
        course_parts = search_course.split()
        if len(course_parts) != 2:
            e_obj = await embed(
                interaction,
                title='Invalid Arguments',
                author=client.user.name,
                avatar=client.user.avatar.url,
                colour=courseDigger,
                content=[['Usage', '`/rate_course <arg>`'],
                         ['Example', '`/rate_course ENSC 252`']],
                footer='rate_course Error'
            )
            if e_obj is not False:
                await interaction.followup.send(embed=e_obj)
            return
        else:
            conn = sqlite3.connect('sfu_grades.db')
            tables = conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table';").fetchall()
            for table in tables:
                table_name = table[0]
                if 'course_name' in [column[1] for column in
                                     conn.execute("PRAGMA table_info('{}');".format(table_name)).fetchall()]:
                    row = conn.execute(
                        "SELECT * FROM {} WHERE course_name='{}';".format(table_name, search_course)).fetchall()
                    if row:
                        fields = [
                            ['Course Name', str(row[0][0])],
                            ['Median Grade', str(row[0][1])],
                            ['Fail Rate', f"{row[0][2]}%"]
                        ]
                        img = 'http://www.sfu.ca/content/sfu/clf/jcr:content/main_content/image_0.img.1280.high.jpg' \
                              '/1468454298527.jpg'
                        e_obj = await embed(
                            interaction,
                            title=f'CourseDiggers Results: ',
                            author=client.user.name,
                            avatar=client.user.avatar.url,
                            colour=courseDigger,
                            thumbnail=img,
                            content=fields,
                            footer='Written by EngBuddy'
                        )
                        if e_obj is not False:
                            await interaction.followup.send(embed=e_obj)
                    else:
                        e_obj = await embed(
                            interaction,
                            title='No Response:\nPlease Try Again',
                            author=client.user.name,
                            avatar=client.user.avatar.url,
                            colour=courseDigger,
                            content=[['Usage', '`/rate_course <arg>`'],
                                     ['Example', '`/rate_course ENSC 252`']],
                            footer='rate_course Error'
                        )
                        if e_obj is not False:
                            await interaction.followup.send(embed=e_obj)
                        return
            conn.close()
    else:
        e_obj = await embed(
            interaction,
            title='Invalid Arguments',
            author=client.user.name,
            avatar=client.user.avatar.url,
            colour=courseDigger,
            content=[['Usage', '`/rate_course <arg>`'],
                     ['Example', '`/rate_course ENSC 252`']],
            footer='rate_course Error'
        )
        if e_obj is not False:
            await interaction.followup.send(embed=e_obj)
        return


async def send_unique_message(message):
    global previous_message
    chosen_message = random.choice(messages)

    # Check if the chosen message is the same as the previous message
    while chosen_message == previous_message:
        chosen_message = random.choice(messages)

    previous_message = chosen_message
    await message.channel.send(f'{message.author.mention} {chosen_message}')


@client.event
async def on_message(message):
    # Make sure bot doesn't get stuck in an infinite loop
    if message.author == client.user:
        return
    if client.user.mentioned_in(message):
        await message.channel.send(f"Hello {message.author.mention}, how can I help you? Type `/help` for a list of my commands.")
    # Grab latest announcement in announcements channel and store it in a json file
    if str(message.channel) == "announcements" and not message.author.bot:
        image_urls = [attachment.url for attachment in message.attachments]
        latest_announcement = {"author": str(message.author), "content": message.content,
                               "date": str(message.created_at), "images": image_urls}
        # Load existing data
        try:
            with open('latest_announcement.json', 'r') as json_file:
                try:
                    data = json.load(json_file)
                except json.JSONDecodeError:
                    data = []
        except FileNotFoundError:
            data = []
        # Add the latest announcement to the top and then write updated data back into the file
        data.insert(0, latest_announcement)
        with open('latest_announcement.json', 'w') as json_file:
            json.dump(data, json_file, indent=4)
        # Update Github repo
        try:
            subprocess.check_call(['git', 'add', 'latest_announcement.json'])
            subprocess.check_call(
                ['git', 'commit', '-m', 'Update latest_announcement.json'])
            subprocess.check_call(['git', 'push'])
        except subprocess.CalledProcessError as e:
            print(f"Error updating GitHub repo: {e}")
        return

    if isinstance(message.channel, discord.DMChannel):
        if message.author.id not in whitelist:
            me = await client.fetch_user(484395342859862017)
            await me.send(f"{message.author} tried to use the bot in DMs")
            await message.channel.send("You dont have access. Ask Sahaj for access!")
            return
        async with message.channel.typing():
            try:
                response = await chatgpt_call(message.content)
            except openai.OpenAIError as e:
                print(f"Error: {e}")
        await message.channel.send(response)
    if message.author.bot:
        await send_unique_message(message)
    try:
        response = handle_message(remove_spaces(message.content))
        if response == 1:
            await message.channel.send("01000100 01100001 01100100 01100100 01111001")
        elif response == 2:
            await message.channel.send("He's a nice guy!")
        elif response == 3:
            await message.channel.send("He's a...nice try ;)")
        elif response == 4:
            await message.channel.send("There is only one mike...")
        elif response == 5:
            await message.channel.send("Does it make sense, guys? Let's have an example.")
        elif response == 6:
            await message.channel.send("Follow SFU MATLAB on Instagram! Now!!!")
    except Exception as e:
        print(f"Error processing message: {e}")

    await client.process_commands(message)


def handle_message(name):
    if "sahaj" in (name.lower()).strip():
        return 1
    if "craig" in (name.lower()).strip():
        return 2
    elif "сгаig" in (name.lower()).strip():
        return 3
    elif "mike" in (name.lower()).strip():
        return 4
    elif "majid" in (name.lower()).strip():
        return 5
    elif "matlab" in (name.lower()).strip():
        return 6
    else:
        return 0


async def chatgpt_call(question):
    url = "https://api.openai.com/v1/chat/completions"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {openai.api_key}",
    }

    data = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "user", "content": question}
        ]
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=data) as response:
            response_json = await response.json()

    chat_response = response_json["choices"][0]["message"]["content"]
    return chat_response[:2000]


async def populate():
    with open('ids.txt', 'r') as f:
        for line in f:
            id_value = line.strip()
            whitelist.append(int(id_value))


async def add_new_id(new_id):
    whitelist.append(int(new_id))
    with open('ids.txt', 'a') as f:
        f.write('\n' + new_id)


def remove_spaces(value):
    return value.replace(" ", "") if value else value


def is_emulator_running():
    try:
        output = subprocess.check_output(
            ["pgrep", "-f", "retroarch|PPSSPPSDL"])
        if output:
            return True
    except subprocess.CalledProcessError:
        pass
    return False


client.run(token)

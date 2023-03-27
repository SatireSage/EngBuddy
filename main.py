from discord.ext import commands
from discord import app_commands
import discord
import openai
import requests

openai.api_key = "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"
dalle_api_endpoint = "https://api.openai.com/v1/images/generations"
token = 'MTA4OTQwMTU5OTExMTIwMDg4MQ.GWYYvv.BAGtiyaB-pPmpV3OvdJmZwURPub6OuxZ42_l1w'
client = commands.Bot(command_prefix="!", intents=discord.Intents.all())
whitelist = [484395342859862017, 880315590378659862, 435638340188897290, 496201894209912832, 319589948766552076,
             707830806705602642, 748791122028920843, 712189433285181491, 709522217334997143, 164102395150860288, 414191464709619714]


@client.event
async def on_ready():
    try:
        await client.change_presence(activity=discord.Game(name="MATLAB"))
        await client.tree.sync()
    except Exception as e:
        print("Something went wrong.")
        exit()


@client.tree.command(name="help", description="Information about available commands")
async def help(interaction: discord.Interaction):
    embed = discord.Embed(title="My Commands", description="Here are the slash commands you can use with me:",
                          color=0x4169e1)
    embed.add_field(name="", value="", inline=False)
    embed.add_field(
        name="about", value="Let me tell you about myself", inline=False)
    embed.add_field(
        name="imagine", value="Ask me make an image and I will create one", inline=False)
    embed.add_field(
        name="ask", value="Ask me something and I will respond to the best of my ability", inline=False)
    embed.add_field(
        name="public", value="Ask me something and I will respond in the current channel", inline=False)
    embed.add_field(
        name="private", value="Ask me something and I will respond in your DM", inline=False)
    embed.add_field(
        name="echo", value="Returns the provided argument", inline=False)
    embed.add_field(
        name="others", value="I also have some secrets for you to discover", inline=False)
    await interaction.response.send_message(embed=embed, ephemeral=True)


@client.tree.command(name="imagine", description="Ask me to make an image!")
@app_commands.describe(prompt="Ask me to make an image!")
async def imagine(interaction: discord.Interaction, *, prompt: str):
    await interaction.response.defer(ephemeral=True)
    headers = {"Authorization": f"Bearer {openai.api_key}"}
    data = {
        "model": "image-alpha-001",
        "prompt": prompt,
        "num_images": 1,
        "size": "1024x1024",
        "response_format": "url"
    }
    response = requests.post(dalle_api_endpoint, headers=headers, json=data)

    if response.status_code == 200:
        image_url = response.json()["data"][0]["url"]
        if interaction.user.id in whitelist:
            await interaction.followup.send(image_url, ephemeral=True)
        else:
            await interaction.followup.send("You dont have access. Ask Sahaj for access!", ephemeral=True)
    else:
        await interaction.followup.send("Sorry something went wrong generating your image.", ephemeral=True)


@client.tree.command(name="ask", description="Ask me something!")
@app_commands.describe(question="Ask me something!")
async def ask(interaction: discord.Interaction, *, question: str):
    await interaction.response.defer(ephemeral=True)
    try:
        response = chatgpt_call(question)
        if interaction.user.id in whitelist:
            await interaction.followup.send(f'Prompt: {question}\n\n Response: {response}')
        else:
            await interaction.followup.send("You dont have access. Ask Sahaj for access!")
    except Exception as e:
        await interaction.followup.send("Sorry, I couldn't generate a response for that question.")


@client.tree.command(name="public", description="Ask me something and I will respond in the current channel!")
@app_commands.describe(question="Ask me something and I will respond in the current channel!")
async def public(interaction: discord.Interaction, *, question: str):
    await interaction.response.defer(ephemeral=False)
    try:
        response = chatgpt_call(question)
        if interaction.user.id in whitelist:
            await interaction.followup.send(f'Prompt: {question}\n\n Response: {response}')
        else:
            await interaction.followup.send("You dont have access. Ask Sahaj for access!")
    except Exception as e:
        await interaction.followup.send("Sorry, I couldn't generate a response for that question.")


@client.tree.command(name="private", description="Ask me something and I will respond in your DM!")
@app_commands.describe(question="Ask me something and I will respond in your DM!")
async def private(interaction: discord.Interaction, *, question: str):
    await interaction.response.defer(ephemeral=True)
    try:
        response = chatgpt_call(question)
        if interaction.user.id in whitelist:
            await interaction.user.send(f'Prompt: {question}\n\n Response: {response}')
        else:
            await interaction.followup.send("You dont have access. Ask Sahaj for access!")
        await interaction.followup.send("Please check your DM! BTW You can talk to me directly in DMS!")
    except Exception as e:
        await interaction.user.send("Sorry, I couldn't generate a response for that question.")


@client.tree.command(name="echo", description="Returns the provided argument!")
@app_commands.describe(argument="Returns the provided argument")
async def echo(interaction: discord.Interaction, *, argument: str):
    if interaction.user.id in whitelist:
        await interaction.response.send_message(argument, ephemeral=False)
    else:
        await interaction.response.send_message("You dont have access. Ask Sahaj for access!", ephemeral=True)


@client.tree.command(name="about", description="Let me tell you about myself!")
async def about(interaction: discord.Interaction):
    embed = discord.Embed(title="About Me!", description="Here is a little info about me:",
                          color=0x4169e1)
    embed.set_thumbnail(url=client.user.avatar.url)
    embed.add_field(name="", value="", inline=False)
    embed.add_field(
        name=f'Hey there, My Name is {client.user.name}!', value='', inline=True)
    embed.add_field(name='Description:', value='EngBuddy is your personal engineering assistant available 24/7 on the '
                    'ESSS Discord server. With its advanced AI capabilities, '
                    'EngBuddy provides personalized support to help you succeed in your '
                    'studies and build meaningful connections with your peers.', inline=False)
    embed.add_field(
        name='For more information: Invoke the help slash command!', value='', inline=True)
    await interaction.response.send_message(embed=embed, ephemeral=True)


@client.event
async def on_message(message):
    # Make sure bot doesn't get stuck in an infinite loop
    if message.author == client.user:
        return
    if isinstance(message.channel, discord.DMChannel):
        if message.author.id not in whitelist:
            await message.channel.send("You dont have access. Ask Sahaj for access!")
            return
        async with message.channel.typing():
            response = chatgpt_call(message.content)
        await message.channel.send(response)
    if message.author.id not in whitelist:
        return
    try:
        response = handle_message(remove_spaces(message.content))
        if response:
            await message.channel.send("he's a nice guy")
    except Exception as e:
        print(f"Error processing message: {e}")

    await client.process_commands(message)


def handle_message(name):
    if "craig" in (name.lower()).strip():
        return True
    else:
        return False


def chatgpt_call(question):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": question}
        ]
    )
    chat_response = completion.choices[0].message.content
    return chat_response


def remove_spaces(value):
    return value.replace(" ", "") if value else value


client.run(token)

import discord
import asyncio  # noqa, flake8 F401
import json  # noqa, flake8 F401


async def embed(interaction, title='', content='', description='', author='', colour=0x00bfbd, thumbnail='',
                avatar='', footer=''):
    """
    title:<str> Title of the embed 99% of the time it'll be the command name, exceptions when it makes sense like
        with the sfu command.\n
    content:<array[tuples]> Array of tuples. Tuple per field of the embed. Field name at index 0 and value at index
        1. \n
    description:<str> Appears under the title. \n
    author:<str> Used to indicate user who invoked the command or the bot itself when it makes sense like with the
        echo command.\n
    colour:<0x......> Used to set the coloured strip on the left side of the embed, by default set to a nice blue
        colour.\n
    link: <deprecated>\n
    thumbnail:<str> Url to image to be used in the embed. Thumbnail appears top right corner of the embed.\n
    avatar:<str> Used to set avatar next to author's name. Must be url. \n
    footer:<str> Used for whatever."""
    # these are put in place cause of the limits on embed described here
    # https://discordapp.com/developers/docs/resources/channel#embed-limits
    if len(title) > 256:
        title = f"{title}"
        await interaction.response.send_message(
            "Embed Error:\nlength of the title "
            f"being added to the title field is {len(title) - 256} characters "
            "too big, please cut down to a size of 256"
        )
        return False

    if len(description) > 2048:
        await interaction.response.send_message(
            f"Embed Error:\nlength of description being added to the "
            f"description field is {len(description) - 2048} characters too big, please cut "
            "down to a size of 2048"
        )
        return False

    if len(content) > 25:
        await interaction.response.send_message("Embed Error:\nlength of content being added to the content field "
                                                f"is {(len(content) - 25)} indices too big, please cut down to a size of 25")
        return False

    for idx, record in enumerate(content):
        if len(record[0]) > 256:
            await interaction.response.send_message(
                f"Embed Error:\nlength of record[0] for content index {idx} being added to the name "
                f"field is {(len(record[0]) - 256)} characters too big, please cut down to a size of 256"
            )
            return False
        if len(record[1]) > 1024:
            await interaction.response.send_message(f"Embed Error:\nlength of record[1] for content index {idx} being added to the value "
                                                    f"field is {(len(record[1]) - 1024)} characters too big, please cut down to a "
                                                    "size of 1024")
            return False

    if len(footer) > 2048:
        await interaction.response.send_message(
            f"Embed Error:\nlength of footer being added to the footer field is "
            f"{len(footer) - 2048} characters too big, please cut down to a size of 2048"
        )
        return False

    emb_obj = discord.Embed(title=title, type='rich')
    emb_obj.description = description
    emb_obj.set_author(name=author, icon_url=avatar)
    emb_obj.colour = colour
    emb_obj.set_thumbnail(url=thumbnail)
    emb_obj.set_footer(text=footer)
    # parse content to add fields
    for x in content:
        emb_obj.add_field(name=x[0], value=x[1], inline=False)
    return emb_obj

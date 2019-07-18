import discord
import os
import Get_AniList as ga
from dotenv import load_dotenv

load_dotenv()


client = discord.Client()


def correct_struct(message):
    if message.content.startswith("<") and message.content.endswith(">"):
        return True
    return False


@client.event
async def on_ready():
    print("I'm in")
    print(client.user)


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if correct_struct(message):
        info = ga.search(message.content[1:-1])
        link = "[AL Link]" + "(" + \
            info["link"] + ")"
        e = discord.Embed(title=info["name"],
                          description=info["description"] + ' \n\n' + link)
        # e.add_field(name="Synopsis", value=info["description"])
        await message.channel.send(embed=e)


token = os.environ.get("DISCORD_BOT_TOKEN")

client.run(token)

import discord
import os
import Get_AniList as ga
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
        link = "[AL Link]" + "(" + \
            ga.search(message.content[1:-1]) + ")"
        e = discord.Embed(title='hello', url="https://discordapp.com",
                          description="lets see if this works " + link)
        await message.channel.send("hello", embed=e)


token = os.environ.get("DISCORD_BOT_TOKEN")

client.run(token)

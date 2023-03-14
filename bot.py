# created by yr0p | github: https://github.com/yr0p
# Deposit for me: 1EKpNDyqSGs49WFPKaQGeokE3vXea63QMw
import discord
import os
import random
import youtube_dl
import asyncio
from discord.ext import commands
from discord.utils import get
from discord import FFmpegPCMAudio
from discord.ext.commands import has_permissions

bot = commands.Bot(command_prefix = 'touka?')
bot.remove_command('help') # remove the command help default

# message about bot is active.
@bot.event
async def on_ready():
    print('Logging in as: {}\n'.format(bot.user.name))

# new command help
@bot.command()
async def help(ctx):
    embed = discord.Embed(
        colour=discord.Colour.dark_purple(),
        #title="{}".format(test['saud']),
        #description="This embed help you."
    )
    #embed.set_author(name=bot.user.name, icon_url='https://media1.tenor.com/images/8d9357a1c51275296f630f0e8690647f/tenor.gif?itemid=5628253')
    embed.set_image(url='https://media1.tenor.com/images/8d9357a1c51275296f630f0e8690647f/tenor.gif?itemid=5628253')
    #embed.set_thumbnail(url='https://media1.tenor.com/images/8d9357a1c51275296f630f0e8690647f/tenor.gif?itemid=5628253')
    # commands the bot
    embed.add_field(name='touka?hate', value='This is the command for her to insult.', inline=False)
    embed.add_field(name='touka?kick (member) (reason)', value='This is the command for kick a member.')
    embed.add_field(name='touka?ban (member) (reason)', value='This is the command for ban a member.')
    embed.add_field(name='touka?unban (member)', value='This is the command for unban a member.')
    embed.add_field(name='touka?clear (value)', value='This is the command for to clear the chat.')
    embed.add_field(name='touka?play (url) or (name_music)', value='This is the command for play musics (doesn’t play a playlist, and you’ll have to wait for the song to finish before adding another one, or “touka? leave”.).', inline=False)
    embed.add_field(name='touka?leave', value='This is the command for leave the voice channel.')
    embed.add_field(name='touka?help', value='This is the command to help you with the commands.', inline=False)

    await ctx.send(embed=embed)

# command for kick users.
@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, user: discord.Member, *, reason):
    await user.kick(reason='')

# command for ban users.
@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, user: discord.Member, *, reason):
    await user.ban(reason)

# command for unban users.
@bot.command
@commands.has_permissions(ban_members=True)
async def unban(ctx, *, Member):
    list_ban = await ctx.guild.bans()
    membro_name, membro_descriminador = member.split('#')

    for banido in list_ban:
        user = banido.user
        if (user.name, user.discriminador) == (membro_name, membro_descriminador):
            await ctx.guild.unban(user)

# commands for clear menssages.
@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount=500): # the value in amount is the value max for clear messages (100).
    await ctx.channel.purge(limit=amount)

# commands for join the channel.
@bot.command()
async def join(ctx):
    channel = ctx.author.voice.channel
    await channel.connect()

# command for play music
@bot.command()
async def play(ctx, url_or_search):
    ydl_opts = { # set the option for youtube_dl download.
        "default_search": "ytsearch",
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    
    dir_name = './' # set directory for find 'name_file.mp3'
    test = os.listdir(dir_name) # list the directory 

    for item in test:# found all call the 'name_file'.mp3
        if item.endswith('.mp3'):# find the file end witch .mp3
            os.remove(os.path.join(dir_name, item))# remove file in directory "./".

    with youtube_dl.YoutubeDL(ydl_opts) as ydl: # transform youtube_dl.YoutubeDL(ydl_opts) in ydl.
        print("Downloading audio now\n")
        ydl.download([url_or_search]) # start dowload the link or search.

    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            print(f"Renamed File: {file}\n")
            os.rename(file, "music.mp3")

    channel = ctx.message.author.voice.channel # connect to the channel you are connected to.
    if not channel:
        await ctx.send("You are not connected to a voice channel.")
        return
    voice = get(bot.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
    source = FFmpegPCMAudio('music.mp3')
    player = voice.play(source)

    info = ydl.extract_info(url_or_search, download=False) # extact 
    info = info['entries']
    description = info[0]['description']
    title_ = info[0]['title']
    thumbnail = info[0]['thumbnails']
    thumb = thumbnail[0]['url']
    # embeds
    embed = discord.Embed(
        colour=discord.Colour.dark_purple(),
        #description="This embed help you."
    )
    embed.add_field(name='{}'.format(title_), value='music is playing now...')
    embed.set_thumbnail(url='{}'.format(thumb))

    await ctx.send(embed=embed)
#command for leave channel.
@bot.command()
async def leave(ctx):
    await ctx.voice_client.disconnect()

#command for view your ping

# command for insults.
@bot.command()
async def hate(ctx):
    insults = [ 'Baka.', 'Idiot!', 'Shit.', 'Shit!']

    response = random.choice(insults)
    await ctx.send(response)


bot.run('your token')

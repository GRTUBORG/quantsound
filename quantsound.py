import asyncio
import os
import discord
import youtube_dl

from youtube_dl import YoutubeDL
from asyncio import sleep
from discord.ext import commands
from discord.ext.commands import Bot
from discord.utils import get

YDL_OPTIONS = {'format': 'worstaudio/best', 'noplaylist': 'True', 'simulate': 'True', 'preferredquality': '192', 'preferredcodec': 'mp3', 'key': 'FFmpegExtractAudio'}
FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

youtube_dl.utils.bug_reports_message = lambda: ''

intents = discord.Intents.all()
Bot = commands.Bot(command_prefix = ["!"], intents = discord.Intents.all())
Bot.remove_command('help')

@Bot.event
async def on_ready():
    await Bot.change_presence(activity = discord.Activity(type = discord.ActivityType.listening, name = "!help"))
    print('{0.user} в онлайне!'.format(Bot))
    
@Bot.command(aliases = ['p'])
async def play(ctx, *, url, volume = 0.5):
    global vc
    
    voice_channel = ctx.message.author.voice.channel
    vc = await voice_channel.connect()
    if vc.is_playing():
        await ctx.send(f'{ctx.message.author.mention}, the music is already playing.')
    else:
        correct_url = url[:8]
        correct_url1 = 'https://'
        
        if correct_url != correct_url1:
            key_error = 0
            with YoutubeDL(YDL_OPTIONS) as ydl:
                info = ydl.extract_info(f'ytsearch:{url}', download = False)
                URL = info['entries'][0]['formats'][0]['url']
                title = info['entries'][0]['title']
                id = info['entries'][0]['id']
        else: 
            key_error = 1
            with YoutubeDL(YDL_OPTIONS) as ydl:
                info = ydl.extract_info(url, download = False)
                URL = info['formats'][0]['url']
                title_url = info['title']
                id = info['id']
        
        vc.play(discord.FFmpegPCMAudio(executable = "/app/vendor/ffmpeg/ffmpeg", source = URL, **FFMPEG_OPTIONS))
        vc.source = discord.PCMVolumeTransformer(vc.source)
        vc.source.volume = volume
        if key_error == 0:
            embed = discord.Embed(title = title, url = f'https://www.youtube.com/watch?v={id}')
            await ctx.send(embed = embed)
        else:
            embed = discord.Embed(title = title_url, url = f'https://www.youtube.com/watch?v={id}')
            await ctx.send(embed = embed)
   

@Bot.command()
async def volume(ctx, *, volume: int):
    author = ctx.message.author
    ctx.voice_client.source.volume = volume / 100
    message = await ctx.send(f"{author.mention}, the volume is set to {volume}%")
    await asyncio.sleep(5)
    await ctx.message.delete()
    await message.delete()

    
@Bot.command()
async def pause(ctx):
    voice = get(Bot.voice_clients, guild = ctx.guild)
    if voice and voice.is_playing():
        if vc == voice:
            voice.pause()
            message = ctx.message
            await message.add_reaction('👌')
        else:
            await ctx.send('You are not connected to the channel!')
    else: 
        await ctx.send('There is nothing to suspend!')

        
@Bot.command()
async def resume(ctx):
    voice = get(Bot.voice_clients, guild = ctx.guild)
    if voice and not voice.is_playing():
        voice.resume()
        message = ctx.message
        await message.add_reaction('👌')
    else:
        await ctx.send('The music is already playing')

        
@Bot.command(aliases = ['leave'])
async def stop(ctx):
    voice = get(Bot.voice_clients, guild = ctx.guild)
    if voice:
        message = ctx.message
        await message.add_reaction('👌')
        await ctx.voice_client.disconnect()
 
@Bot.command()
async def help(ctx):
    author = ctx.message.author
    embed = discord.Embed(title = 'Help', description = f'Hello, {author.mention}! List of all commands:\n'
                          '• `!help` outputs the help command;\n'
                          '• `!play` (aliases: `!p`) playback songs/streams. Arguments: the query or the reference;\n'
                          '• `!volume` changing the volume. Arguments: integer from 0 to 100;\n'
                          '• `!pause` pause the current playback;\n'
                          '• `!resume` continue playing;\n'
                          '• `!stop` (aliases: `!leave`) full stop of playback with subsequent disconnection of the bot from the voice channel.')
    await ctx.send(embed = embed)
    
token = os.environ.get('bot_token')
Bot.run(str(token))

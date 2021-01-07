#Attention! This code is written for the Heroku service! 
#Therefore, if you encounter any shortcomings/errors/bugs on other services, please write to me. 
#We will understand!

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

help_message = (':flag_ru:\n'
                '**[Europa +](https://europaplus.ru)**, **[Radio Record](https://www.radiorecord.ru)**, '
                '**[Record Deep](https://www.radiorecord.ru/station/deep)**, **[Radio Enegry](https://www.energyfm.ru)**'
                '\n\n'
                ':flag_us:\n'
                '**[West coast](http://the-radio.ru/radio/pvpjamz-west-coast-r637)**')

youtube_dl.utils.bug_reports_message = lambda: ''

intents = discord.Intents.all()
Bot = commands.Bot(command_prefix = ["!"], intents = discord.Intents.all())
Bot.remove_command('help')




@Bot.event
async def on_ready():
    await Bot.change_presence(activity = discord.Activity(type = discord.ActivityType.listening, name = "!help 🎶 v7.1.21"))
    print('{0.user} в онлайне!'.format(Bot))
 

@Bot.command(aliases = ['p'])
async def play(ctx, *, url, volume = 0.5):
    global vc
    
    author = ctx.message.author
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
                title = info['title']
                id = info['id']
        
        vc.play(discord.FFmpegPCMAudio(executable = "/app/vendor/ffmpeg/ffmpeg", source = URL, **FFMPEG_OPTIONS))
        vc.source = discord.PCMVolumeTransformer(vc.source)
        vc.source.volume = volume
        
        embed = discord.Embed(description = f'Now playing: [{title}](https://www.youtube.com/watch?v={id}) [{author.mention}]', color = 0xbc03ff)
        await ctx.send(embed = embed)

        
@Bot.command()
async def radio(ctx, *, name = 'help', volume = 0.5):
    if name == '--help' or name == 'help' or name == '' or name == ' ':
        embed = discord.Embed(title = 'List of available radio stations', description = help_message)
        message = await ctx.send(embed = embed)
        await asyncio.sleep(15)
        await message.delete()
    else:
        name = name.lower()
        author = ctx.message.author
    
        if name == 'европа +' or name == 'europa +' or name == 'европа плюс' or name == 'europa plus':
            source = 'http://ep128.streamr.ru'
            embed = discord.Embed(description = f'Now playing: [Europa +](https://europaplus.ru) [{author.mention}]', color = 0xbc03ff)
            await ctx.send(embed = embed)

        elif name == 'радио рекорд' or name == 'radio record' or name == 'радио record' or name == 'record':
            source = 'http://air2.radiorecord.ru:805/rr_320'
            embed = discord.Embed(description = f'Now playing: [Radio Record](https://www.radiorecord.ru) [{author.mention}]', color = 0xbc03ff)
            await ctx.send(embed = embed)
            
        elif name == 'record deep' or name == 'deep' or name == 'радио deep' or name == 'radio deep':
            source = 'http://air2.radiorecord.ru:805/deep_320'
            embed = discord.Embed(description = f'Now playing: [Record Deep](https://www.radiorecord.ru/station/deep) [{author.mention}]', color = 0xbc03ff)
            await ctx.send(embed = embed)

        elif name == 'radio energy' or name == 'energy' or name == 'энерджи' or name == 'радио энерджи':
            source = 'https://pub0302.101.ru:8443/stream/air/aac/64/99'
            embed = discord.Embed(description = f'Now playing: [Radio Enegry](https://www.energyfm.ru) [{author.mention}]', color = 0xbc03ff)
            await ctx.send(embed = embed)

        else:
            await ctx.send('I caught an invalid request, I play the radio station `Europe +`')
            source = 'http://ep128.streamr.ru'

        voice_channel = ctx.message.author.voice.channel
        vc = await voice_channel.connect(reconnect = True)
            
        vc.play(discord.FFmpegPCMAudio(executable = "/app/vendor/ffmpeg/ffmpeg", source = source, **FFMPEG_OPTIONS))
        vc.source = discord.PCMVolumeTransformer(vc.source)
        vc.source.volume = volume

            
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
        await message.add_reaction('🤘')
    else:
        await ctx.send('The music is already playing')

        
@Bot.command(aliases = ['leave'])
async def stop(ctx):
    voice = get(Bot.voice_clients, guild = ctx.guild)
    if voice:
        message = ctx.message
        await message.add_reaction('👋')
        await ctx.voice_client.disconnect()
 

@Bot.command()
async def help(ctx):
    author = ctx.message.author
    embed = discord.Embed(title = 'Help', description = f'Hello, {author.mention}! List of all commands:\n'
                          '• `!help` outputs the help command;\n'
                          '• `!play` (aliases: `!p`) playback songs/streams. Arguments: the query or the reference;\n'
                          '• `!radio` playing the radio. The radio list is available by command: `!radio help`;\n'
                          '• `!volume` changing the volume. Arguments: integer from 0 to 100;\n'
                          '• `!pause` pause the current playback;\n'
                          '• `!resume` continue playing;\n'
                          '• `!stop` (aliases: `!leave`) full stop of playback with subsequent disconnection of the bot from the voice channel.')
    await ctx.send(embed = embed)
  

token = os.environ.get('bot_token')
Bot.run(str(token))

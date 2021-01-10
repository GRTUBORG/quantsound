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
                '**[Europe +](https://europaplus.ru)**, **[Radio Record](https://www.radiorecord.ru)**, '
                '**[Record Deep](https://www.radiorecord.ru/station/deep)**, **[Radio Energy](https://www.energyfm.ru)**'
                '\n\n'
                ':flag_us:\n'
                '**[West coast](http://the-radio.ru/radio/pvpjamz-west-coast-r637)**')

youtube_dl.utils.bug_reports_message = lambda: ''

intents = discord.Intents.all()
prefix = "qs!"
Bot = commands.Bot(command_prefix = prefix, intents = discord.Intents.all())
Bot.remove_command('help')




@Bot.event
async def on_ready():
    await Bot.change_presence(activity = discord.Activity(type = discord.ActivityType.listening, name = "qs!help 🎶 v9.1.21"))
    print('{0.user} в онлайне!'.format(Bot))


@Bot.event
async def on_command_error(ctx, error):
    pass

@Bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        author = ctx.message.author
        embed = discord.Embed(description = f'Attention, {author.mention}! This command __does not exist__! Check the spelling, or write the command `{prefix}help`', color = 0xff1a1a)
        await ctx.send(embed = embed)
        

@Bot.command(aliases = ['p'])
async def play(ctx, *, url, volume = 0.5):
    global vc
    
    author = ctx.message.author
    voice_channel = ctx.message.author.voice.channel
    
    try:
        vc = await voice_channel.connect()
    except:
        None
        
    if vc.is_playing():
        message = await ctx.send(f'{ctx.message.author.mention}, the music is already playing. Please wait for your turn!')
        await asyncio.sleep(10)
        await message.delete()
    else:
        embed = discord.Embed(description = f'A few seconds, {author.mention}')
        message = await ctx.send(embed = embed)
            
        correct_url = url[:8]
        correct_url1 = 'https://'
            
        if correct_url != correct_url1:
            with YoutubeDL(YDL_OPTIONS) as ydl:
                info = ydl.extract_info(f'ytsearch:{url}', download = False)
                URL = info['entries'][0]['formats'][0]['url']
                title = info['entries'][0]['title']
                id = info['entries'][0]['id']
                picture = info['entries'][0]['thumbnails'][0]['url']
        else: 
            with YoutubeDL(YDL_OPTIONS) as ydl:
                info = ydl.extract_info(url, download = False)
                URL = info['formats'][0]['url']
                title = info['title']
                id = info['id']                
            
        vc.play(discord.FFmpegPCMAudio(executable = "/app/vendor/ffmpeg/ffmpeg", source = URL, **FFMPEG_OPTIONS))
        vc.source = discord.PCMVolumeTransformer(vc.source)
        vc.source.volume = volume
            
        await message.delete()
            
        try:
            embed = discord.Embed(description = f'Now playing: [{title}](https://www.youtube.com/watch?v={id}) [{author.mention}]', color = 0xbc03ff)
            embed.set_thumbnail(url = picture)
            await ctx.send(embed = embed)
        except:
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
    
        if name == 'европа +' or name == 'europe +' or name == 'европа плюс' or name == 'europe plus':
            source = 'http://ep128.streamr.ru'
            url = 'https://bit.ly/39gx54n'
            embed = discord.Embed(description = f'Now playing: [Europe +](https://europaplus.ru) [{author.mention}]', color = 0xbc03ff)
            embed.set_author(name = 'Radio', icon_url = url)
            await ctx.send(embed = embed)

        elif name == 'радио рекорд' or name == 'radio record' or name == 'радио record' or name == 'record':
            source = 'http://air2.radiorecord.ru:805/rr_320'
            url = 'https://bit.ly/3hV2xcx'
            embed = discord.Embed(description = f'Now playing: [Radio Record](https://www.radiorecord.ru) [{author.mention}]', color = 0xbc03ff)
            embed.set_author(name = 'Radio', icon_url = url)
            await ctx.send(embed = embed)
            
        elif name == 'record deep' or name == 'deep' or name == 'радио deep' or name == 'radio deep':
            source = 'http://air2.radiorecord.ru:805/deep_320'
            url = 'https://bit.ly/3hYQPgX'
            embed = discord.Embed(description = f'Now playing: [Record Deep](https://www.radiorecord.ru/station/deep) [{author.mention}]', color = 0xbc03ff)
            embed.set_author(name = 'Radio', icon_url = url)
            await ctx.send(embed = embed)

        elif name == 'radio energy' or name == 'energy' or name == 'энерджи' or name == 'радио энерджи':
            source = 'https://pub0302.101.ru:8443/stream/air/aac/64/99'
            url = 'https://bit.ly/2JXXUlg'
            embed = discord.Embed(description = f'Now playing: [Radio Energy](https://www.energyfm.ru) [{author.mention}]', color = 0xbc03ff)
            embed.set_author(name = 'Radio', icon_url = url)
            await ctx.send(embed = embed)
            
        elif name == 'radio west' or name == 'west coast' or name == 'радио вест коаст' or name == 'вест коаст':
            source = 'https://stream.pvpjamz.com/stream'
            url = 'https://bit.ly/2LEv9L6'
            embed = discord.Embed(description = f'Now playing: [Weat Coast](http://the-radio.ru/radio/pvpjamz-west-coast-r637) [{author.mention}]', color = 0xbc03ff)
            embed.set_author(name = 'Radio', icon_url = url)
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
    voice_channel = ctx.message.author.voice.channel
    voice = get(Bot.voice_clients, guild = ctx.guild)
    if voice and voice.is_playing():
        voice.pause()
        message = ctx.message
        await message.add_reaction('👌')
    else: 
        await ctx.send('There is nothing to suspend!')

        
@Bot.command()
async def resume(ctx):
    voice_channel = ctx.message.author.voice.channel
    voice = get(Bot.voice_clients, guild = ctx.guild)
    if voice and not voice.is_playing():
        voice.resume()
        message = ctx.message
        await message.add_reaction('🤘')
    else:
        await ctx.send('The music is already playing')

        
@Bot.command(aliases = ['leave'])
async def stop(ctx):
    voice_channel = ctx.message.author.voice.channel
    voice = get(Bot.voice_clients, guild = ctx.guild)
    if voice:
        message = ctx.message
        await message.add_reaction('👋')
        await ctx.voice_client.disconnect()

        
@Bot.command()
async def help(ctx):
    author = ctx.message.author
    embed = discord.Embed(title = 'Help', description = f'Hello, {author.mention}! List of all commands:\n'
                          f'• `{prefix}help` outputs the help command;\n'
                          f'• `{prefix}play` (aliases: `{prefix}p`) playback songs/streams. Arguments: the query or the reference;\n'
                          f'• `{prefix}radio` playing the radio. The radio list is available by command: `{prefix}radio help`;\n'
                          f'• `{prefix}volume` changing the volume. Arguments: integer from 0 to 100;\n'
                          f'• `{prefix}pause` pause the current playback;\n'
                          f'• `{prefix}resume` continue playing;\n'
                          f'• `{prefix}stop` (aliases: `{prefix}leave`) full stop of playback with subsequent disconnection of the bot from the voice channel;\n'
                          f'• `{prefix}author` all information about the authors of quantsound.')
    await ctx.send(embed = embed)


@Bot.command(aliases = ['AUTHOR'])
async def author(ctx):
    await ctx.message.delete()
    embed = discord.Embed(title = 'Our team:', description = '• Developer: **[Denis Blinov](https://vk.com/d.blinov79)**,\n'
                                                             '• Developer github: **[GRTUBORG](https://github.com/GRTUBORG)**;\n'
                                                             '• From giving discord member **•Satoemari•#3381**;\n'
                                                             '• Our group in VK: **[quantsound](https://vk.com/quantsound_discord)**.',
                                                             color = 0xbc03ff)
    await ctx.send(embed = embed)
    

token = os.environ.get('bot_token')
Bot.run(str(token))

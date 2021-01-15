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
update = '14.01.21'
youtube_dl.utils.bug_reports_message = lambda: ''

intents = discord.Intents.all()
prefix = "qs!"
Bot = commands.Bot(command_prefix = prefix, intents = discord.Intents.all())
Bot.remove_command('help')




@Bot.event
async def on_ready():
    print('{0.user} в онлайне!'.format(Bot))
    while True:
        await Bot.change_presence(activity = discord.Activity(type = discord.ActivityType.listening, name = "qs!help 🎶"))
        await sleep(30)
        await Bot.change_presence(activity = discord.Activity(type = discord.ActivityType.listening, name = f"latest update: {update}"))
        await sleep(5)

@Bot.event
async def on_voice_state_update(member, before, after):
    global length
    if before.channel is None and after.channel is not None:
        length = len(after.channel.members)
    elif before.channel is not None and after.channel is None:
        length = len(before.channel.members)

@Bot.event
async def on_command_error(ctx, error):
    pass

@Bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        author = ctx.message.author
        embed = discord.Embed(description = f'Attention, {author.mention}! This command __does not exist__! Check the spelling, or write the command `{prefix}help`', color = 0xff1a1a)
        embed.set_footer(text = "supports by quantsound")
        await ctx.send(embed = embed)
        

@Bot.command(aliases = ['p'])
async def play(ctx, *, url, volume = 0.5):
    global vc
    
    try:
        message = ctx.message
        await message.add_reaction('🎵')
    except:
        None
    
    author = ctx.message.author
    try:
        voice_channel = ctx.message.author.voice.channel
    except:
        message = await ctx.send(f"{author.mention}, you're not connected to the voice channel!")
        await asyncio.sleep(5)
        await message.delete()
    
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
                """duration = info['entries'][0]['duration']                    #track duration,
                if duration == 0:                                               #needs to be corrected
                    duration = "I can't tell the time. Most likely, you have turned on the stream"
                else:
                    duration = str(datetime.timedelta(seconds = duration))"""
                URL = info['entries'][0]['formats'][0]['url']
                title = info['entries'][0]['title']
                id = info['entries'][0]['id']
                picture = info['entries'][0]['thumbnails'][0]['url']
        else: 
            with YoutubeDL(YDL_OPTIONS) as ydl:
                info = ydl.extract_info(url, download = False)
                """duration = info['duration']                                  #track duration,
                if duration == 0:                                               #needs to be corrected
                    duration = "I can't tell the time. Most likely, you have turned on the stream"
                else:
                    duration = str(datetime.timedelta(seconds = duration))"""
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
            embed.set_footer(text = "supports by quantsound")
            await ctx.send(embed = embed)
        except:
            embed = discord.Embed(description = f'Now playing: [{title}](https://www.youtube.com/watch?v={id}) [{author.mention}]', color = 0xbc03ff)
            embed.set_footer(text = "supports by quantsound")
            await ctx.send(embed = embed)
        
        while length != 1:
            await asyncio.sleep(1) 
        else:
            await ctx.voice_client.disconnect() 
            
            
@Bot.command()
async def radio(ctx, *, name = 'help', volume = 0.5):
    if name == '--help' or name == 'help' or name == '' or name == ' ':
        embed = discord.Embed(title = 'List of available radio stations', description = help_message)
        embed.set_footer(text = "supports by quantsound")
        message = await ctx.send(embed = embed)
        await asyncio.sleep(15)
        await message.delete()
    else:
        try:
            message = ctx.message
            await message.add_reaction('📻')
        except:
            None
            
        name = name.lower()
        author = ctx.message.author
    
        if name == 'европа +' or name == 'europe +' or name == 'европа плюс' or name == 'europe plus':
            source = 'http://ep128.streamr.ru'
            url = 'https://bit.ly/39gx54n'
            embed = discord.Embed(description = f'Now playing: [Europe +](https://europaplus.ru) [{author.mention}]', color = 0xbc03ff)
            embed.set_author(name = 'Radio', icon_url = url)
            embed.set_footer(text = "supports by quantsound")
            await ctx.send(embed = embed)

        elif name == 'радио рекорд' or name == 'radio record' or name == 'радио record' or name == 'record':
            source = 'http://air2.radiorecord.ru:805/rr_320'
            url = 'https://bit.ly/3hV2xcx'
            embed = discord.Embed(description = f'Now playing: [Radio Record](https://www.radiorecord.ru) [{author.mention}]', color = 0xbc03ff)
            embed.set_author(name = 'Radio', icon_url = url)
            embed.set_footer(text = "supports by quantsound")
            await ctx.send(embed = embed)
            
        elif name == 'record deep' or name == 'deep' or name == 'радио deep' or name == 'radio deep':
            source = 'http://air2.radiorecord.ru:805/deep_320'
            url = 'https://bit.ly/3hYQPgX'
            embed = discord.Embed(description = f'Now playing: [Record Deep](https://www.radiorecord.ru/station/deep) [{author.mention}]', color = 0xbc03ff)
            embed.set_author(name = 'Radio', icon_url = url)
            embed.set_footer(text = "supports by quantsound")
            await ctx.send(embed = embed)

        elif name == 'radio energy' or name == 'energy' or name == 'энерджи' or name == 'радио энерджи':
            source = 'https://pub0302.101.ru:8443/stream/air/aac/64/99'
            url = 'https://bit.ly/2JXXUlg'
            embed = discord.Embed(description = f'Now playing: [Radio Energy](https://www.energyfm.ru) [{author.mention}]', color = 0xbc03ff)
            embed.set_author(name = 'Radio', icon_url = url)
            embed.set_footer(text = "supports by quantsound")
            await ctx.send(embed = embed)
            
        elif name == 'radio west' or name == 'west coast' or name == 'радио вест коаст' or name == 'вест коаст':
            source = 'https://stream.pvpjamz.com/stream'
            url = 'https://bit.ly/2LEv9L6'
            embed = discord.Embed(description = f'Now playing: [Weat Coast](http://the-radio.ru/radio/pvpjamz-west-coast-r637) [{author.mention}]', color = 0xbc03ff)
            embed.set_author(name = 'Radio', icon_url = url)
            embed.set_footer(text = "supports by quantsound")
            await ctx.send(embed = embed)

        else:
            message_invalid = await ctx.send('I caught an invalid request, I play the radio station `Europe +`')
            source = 'http://ep128.streamr.ru'
            url = 'https://bit.ly/39gx54n'
            embed = discord.Embed(description = f'Now playing: [Europe +](https://europaplus.ru) [{author.mention}]', color = 0xbc03ff)
            embed.set_author(name = 'Radio', icon_url = url)
            embed.set_footer(text = "supports by quantsound")
            await ctx.send(embed = embed)

        voice_channel = ctx.message.author.voice.channel
        vc = await voice_channel.connect(reconnect = True)
            
        vc.play(discord.FFmpegPCMAudio(executable = "/app/vendor/ffmpeg/ffmpeg", source = source, **FFMPEG_OPTIONS))
        vc.source = discord.PCMVolumeTransformer(vc.source)
        vc.source.volume = volume
        
        await asyncio.sleep(5)
        await message_invalid.delete()
        
        while length != 1:
            await asyncio.sleep(1) 
        else:
            await ctx.voice_client.disconnect() 
            
            
@Bot.command()
async def volume(ctx, *, volume: int):
    author = ctx.message.author
    ctx.voice_client.source.volume = volume / 100
    message = await ctx.send(f"{author.mention}, the volume is set to {volume}%")
    await asyncio.sleep(5)
    await message.delete()

    
@Bot.command()
async def pause(ctx):
    try:
        voice_channel = ctx.message.author.voice.channel
        voice = get(Bot.voice_clients, guild = ctx.guild)
    except:
        message = await ctx.send(f"{author.mention}, you're not connected to the voice channel!")
        await asyncio.sleep(5)
        await message.delete()
        
    if voice and voice.is_playing():
        voice.pause()
        try:
            message = ctx.message
            await message.add_reaction('👌')
        except:
            None
            
    elif not voice:
        message = await ctx.send("I'm not connected to the channel!")
        await asyncio.sleep(5)
        await message.delete()
    else: 
        await ctx.send('There is nothing to suspend!')

        
@Bot.command()
async def resume(ctx):
    try:
        voice_channel = ctx.message.author.voice.channel
        voice = get(Bot.voice_clients, guild = ctx.guild)
    except:
        message = await ctx.send(f"{author.mention}, you're not connected to the voice channel!")
        await asyncio.sleep(5)
        await message.delete()
        
    if voice and not voice.is_playing():
        voice.resume()
        try:
            message = ctx.message
            await message.add_reaction('🤘')
        except:
            None
            
    elif not voice:
        message = await ctx.send("I'm not connected to the channel!")
        await asyncio.sleep(5)
        await message.delete()
    else:
        await ctx.send('The music is already playing')

        
@Bot.command(aliases = ['leave'])
async def stop(ctx):
    author = ctx.message.author
    try:
        voice_channel = ctx.message.author.voice.channel
        voice = get(Bot.voice_clients, guild = ctx.guild)
    except:
        message = await ctx.send(f"{author.mention}, you're not connected to the voice channel!")
        await asyncio.sleep(5)
        await message.delete()
        
    if voice:
        try:
            message = ctx.message
            await message.add_reaction('👋')
        except:
            None
            
        await ctx.voice_client.disconnect()
    else:
        message = await ctx.send("I'm not connected to the channel!")
        await asyncio.sleep(5)
        await message.delete()

        
@Bot.command()
async def help(ctx):
    author = ctx.message.author
    embed = discord.Embed(description = f'**Hello, {author.mention}! List of all commands:**\n'
                          f'• `{prefix}help` outputs the help command;\n'
                          f'• `{prefix}play` (aliases: `{prefix}p`) playback songs/streams. Arguments: the query or the reference;\n'
                          f'• `{prefix}radio` playing the radio. The radio list is available by command: `{prefix}radio help`;\n'
                          f'• `{prefix}volume` changing the volume. Arguments: integer from 0 to 100;\n'
                          f'• `{prefix}pause` pause the current playback;\n'
                          f'• `{prefix}resume` continue playing;\n'
                          f'• `{prefix}stop` (aliases: `{prefix}leave`) full stop of playback with subsequent disconnection of the bot from the voice channel;\n'
                          f'• `{prefix}author` all information about the authors of quantsound;\n'
                          f'• `{prefix}donate` assistance to developers of the bot;\n'
                          f'• `{prefix}servers` find out information about servers. It works only on the home server and displays the number of servers on which the bot is installed.\n\n\n'
                          '[Invite quantsound](https://discord.com/oauth2/authorize?client_id=795312210343624724&permissions=8&scope=bot) | [Support server](https://discord.gg/rjMDwaB)', color = 0xbc03ff)
    embed.set_author(name = "Quantsound Support", icon_url = "https://bit.ly/39w96yc")
    embed.set_footer(text = "supports by quantsound")
    await ctx.send(embed = embed)


@Bot.command(aliases = ['AUTHOR'])
async def author(ctx):
    embed = discord.Embed(title = 'Our team:', description = '• Developer: **[Denis Blinov](https://vk.com/d.blinov79)**,\n'
                                                             '• Developer github: **[GRTUBORG](https://github.com/GRTUBORG)**;\n'
                                                             '• From giving discord member **[•Satoemari•#3381](https://discord.com/users/394850460420538389)**;\n'
                                                             '• Our group in VK: **[quantsound](https://vk.com/quantsound_discord)**.',
                                                             color = 0xbc03ff)
    embed.set_footer(text = "supports by quantsound")
    await ctx.send(embed = embed)

    
@Bot.command()
async def donate(ctx):
    author = ctx.message.author
    embed = discord.Embed(description = f"Hi {author.mention}, I'm really glad you stopped by!\n"
                                        'Our bot is free for the Discord community, but our team will be grateful '
                                        'to you for donating absolutely any amount to the further development of **quantsound**\n\n'
                                        'Payment is available on several e-wallets:\n'
                                        '• [QIWI](https://qiwi.com/n/OVERFLOW16),\n'
                                        '• [ЮMoney](https://money.yandex.ru/to/410015133921329),\n\n'
                                        '*Paypal* and *Webmoney* will also be available soon...\n\n'
                                        'Thank you for choosing us! \n🤍', color = 0xbc03ff)
    embed.set_author(name = "The donations page", icon_url = "https://bit.ly/39w96yc")
    embed.set_footer(text = "supports by quantsound")
    await ctx.send(embed = embed)
    
    
@Bot.command()
async def servers(ctx):
    if ctx.guild.id == 526097247285280768:
        servers = Bot.guilds
        await ctx.send(f'Бот установлен на {len(servers)} серверах')
    else:
        message = await ctx.send("You don't have access to this command! \nGo to the bot's home server to use this command!")
        await asyncio.sleep(5) 
        await message.delete()


        
token = os.environ.get('bot_token')
Bot.run(str(token))

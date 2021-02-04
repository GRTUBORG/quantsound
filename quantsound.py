#Attention! This code is written for the Heroku service! 
#Therefore, if you encounter any shortcomings/errors/bugs on other services, please write to me. 
#We will understand!

import asyncio
import os
import discord
import youtube_dl
import re
import datetime

from youtube_dl import YoutubeDL
from asyncio import sleep
from discord.ext import commands
from discord.ext.commands import Bot
from discord.utils import get
from datetime import date, time, timedelta

YDL_OPTIONS = {'format': 'worstaudio/best', 'noplaylist': 'True', 'simulate': 'True', 'preferredquality': '192', 'preferredcodec': 'mp3', 'key': 'FFmpegExtractAudio'}
FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

available_services = ('**[1tv](https://www.1tv.ru)**, **[Pornhub](https://rt.pornhub.com)**, ' 
                      '**[YouTube](https://www.youtube.com)**, **[twitch](https://www.twitch.tv)**')

yoomoney_url = os.environ.get('yoomoney_url')
qiwi_url = os.environ.get('qiwi_url')
vk_page = os.environ.get('vk_page')
count_servers = os.environ.get('count_servers')
update = os.environ.get('update')
token = os.environ.get('bot_token')

help_message = (':radio:\n'
                '**[Europe +](https://europaplus.ru)**, **[Radio Energy](https://www.energyfm.ru)**, **[West coast](http://the-radio.ru/radio/pvpjamz-west-coast-r637)**, **[CORE RADIO](https://coreradio.ru)**, **[Phonk](https://101.ru/radio/user/865080)**, **[Radio Record](https://www.radiorecord.ru)**, '
                '**[Record Deep](https://www.radiorecord.ru/station/deep)**, **[Record Pirate Station](https://www.radiorecord.ru)**, **[Record Black Rap](https://www.radiorecord.ru)**, '
                '**[Record Rock](https://www.radiorecord.ru)**, **[Record Trap](https://www.radiorecord.ru)**, **[Record Dubstep](https://www.radiorecord.ru)**')

youtube_dl.utils.bug_reports_message = lambda: ''

intents = discord.Intents.all()
prefix = "qs!"
Bot = commands.Bot(command_prefix = prefix, intents = discord.Intents.all())
Bot.remove_command('help')

delta = datetime.timedelta(hours = 3, minutes = 0)

@Bot.event
async def on_ready():
    print('{0.user} в онлайне!'.format(Bot))
    while True:
        t = (datetime.datetime.now(datetime.timezone.utc) + delta)
        nowtime = t.strftime("%H")
        nowtime = int(nowtime)
        
        if nowtime >= 21 or nowtime <= 7:
            await Bot.change_presence(status = discord.Status.idle, activity = discord.Activity(type = discord.ActivityType.listening, name = f"{prefix}help 🎶"))
            await sleep(30)
            await Bot.change_presence(status = discord.Status.idle, activity = discord.Activity(type = discord.ActivityType.listening, name = f"latest update: {update}"))
            await sleep(5)
            await Bot.change_presence(status = discord.Status.idle, activity = discord.Activity(type = discord.ActivityType.listening, name = f"{count_servers} servers!"))
            await sleep(5)
            
        else:
            await Bot.change_presence(activity = discord.Activity(type = discord.ActivityType.listening, name = f"{prefix}help 🎶"))
            await sleep(30)
            await Bot.change_presence(activity = discord.Activity(type = discord.ActivityType.listening, name = f"latest update: {update}"))
            await sleep(5)
            await Bot.change_presence(activity = discord.Activity(type = discord.ActivityType.listening, name = f"{count_servers} servers!"))
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
        vc = await voice_channel.connect(reconnect = True)
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
                
                duration = info['entries'][0]['duration']
                duration = datetime.timedelta(seconds = duration)
                URL = info['entries'][0]['formats'][0]['url']
                title = info['entries'][0]['title']
                id = info['entries'][0]['id']
                picture = info['entries'][0]['thumbnails'][0]['url']
                
                await message.delete()
                embed = discord.Embed(description = f'[YOUTUBE 🎬] Now playing: [{title}](https://www.youtube.com/watch?v={id}) (**{duration}**) [{author.mention}]', color = 0xbc03ff)
                embed.set_thumbnail(url = picture)
                embed.set_footer(text = "supports by quantsound")
                await ctx.send(embed = embed) 
                
        else: 
            with YoutubeDL(YDL_OPTIONS) as ydl:
                if url[8:21] == 'www.twitch.tv':
                    if re.search(r'\bvideos/all\b', url):
                        url = url.replace('videos/all', '')
                    info = ydl.extract_info(url, download = False)
                    URL = info['formats'][0]['manifest_url']
                    title = info['title']
                    id = info['id']

                    await message.delete()
                    embed = discord.Embed(description = f"[TWITCH 🎮] I'm playing a stream: **{title[:-17]}** [{author.mention}]\n\n"
                                                        '⚠️ If the stream does not play for one minute - please wait, as the command is in early development', color = 0xbc03ff)
                    embed.set_footer(text = "supports by quantsound")
                    await ctx.send(embed = embed) 

                    
                elif url[8:20] == 'www.youtube.': 
                    info = ydl.extract_info(url, download = False)
                    
                    duration = info['duration']
                    duration = datetime.timedelta(seconds = duration)
                    URL = info['formats'][0]['url']
                    title = info['title']
                    id = info['id']

                    await message.delete()
                    embed = discord.Embed(description = f'[YOUTUBE 🎬] Now playing: [{title}](https://www.youtube.com/watch?v={id}) (**{duration}**) [{author.mention}]', color = 0xbc03ff)
                    embed.set_footer(text = "supports by quantsound")
                    await ctx.send(embed = embed)  
                
                
                elif url[8:17] == 'rutube.ru':
                    if re.search(r'\bfeeds/live\b', url):
                        info = ydl.extract_info('ytsearch:lofi stream', download = False)
                        URL = info['entries'][0]['formats'][0]['url']
                        title = info['entries'][0]['title']
                        id = info['entries'][0]['id']
                        key_error = 0
                    else:
                        if re.search(r'\bpl_type\b', url):
                            url = url[:-27]
                        info = ydl.extract_info(url, download = False)
                        title = info['title']
                        URL = info['formats'][1]['url']
                        id = info['id']
                        key_error = 1
                    await message.delete()
                    
                    if key_error == 0:
                        embed = discord.Embed(description = f'[YOUTUBE 🎬] Now playing: [{title}](https://www.youtube.com/watch?v={id}) [{author.mention}] \n\n'
                                                            "🤔 Why the stream? Unfortunately, this is a steam with `RUTUBE`, and I do not support links of this format yet...", color = 0xbc03ff)
                        embed.set_footer(text = "supports by quantsound")
                        await ctx.send(embed = embed)
                    else:
                        embed = discord.Embed(description = f'[RUTUBE 🎬] Now playing: [{title}](https://rutube.ru/video/{id}) [{author.mention}]', color = 0xbc03ff)
                        embed.set_footer(text = "supports by quantsound")
                        await ctx.send(embed = embed)
                
                
                elif url[8:16] == 'pornhub.' or url[8:19] == 'rt.pornhub.':
                    info = ydl.extract_info(url, download = False)
                    title = info['title']
                    URL = info['formats'][1]['url']
                    id = info['id']
                    if ctx.message.channel.is_nsfw():  
                        thumbnail = info['thumbnail'] 
                        embed = discord.Embed(description = f'[PORNHUB 🔥] Now playing: [{title}](https://rt.pornhub.com/view_video.php?viewkey={id}) [{author.mention}]', color = 0xbc03ff)
                        embed.set_thumbnail(url = thumbnail)
                        embed.set_footer(text = "supports by quantsound")
                        await ctx.send(embed = embed)
                    else:
                        embed = discord.Embed(description = f'[PORNHUB 🔥] Now playing: [{title}](https://rt.pornhub.com/view_video.php?viewkey={id}) [{author.mention}]', color = 0xbc03ff)
                        embed.set_footer(text = "supports by quantsound")
                        await ctx.send(embed = embed)
                
                
                elif url[8:16] == 'www.1tv.':
                    info = ydl.extract_info(url, download = False)
                    URL = info['entries'][0]['formats'][0]['url']  
                    title = info['entries'][0]['title']
                    picture = info['entries'][0]['thumbnails'][0]['url']
                    id = info['entries'][0]['id']
                    webpage_url = info['webpage_url']
                    embed = discord.Embed(description = f'[1TV 1️⃣] Now playing: [{title}]({webpage_url}) [{author.mention}]', color = 0xbc03ff)
                    embed.set_thumbnail(url = picture)
                    embed.set_footer(text = "supports by quantsound")
                    await ctx.send(embed = embed) 
                
                
                else:
                    await message.delete()
                    message = await ctx.send('Ooops, your link is not suitable for more than one service. Please check your link and the list of available services, and try again...\n\nI play a lo fi stream')
                    info = ydl.extract_info(f'ytsearch:lofi stream', download = False)
                    URL = info['entries'][0]['formats'][0]['url']  
                    await asyncio.sleep(5)
                    await message.delete()              
           
        vc.play(discord.FFmpegPCMAudio(executable = "/app/vendor/ffmpeg/ffmpeg", source = URL, **FFMPEG_OPTIONS))
        vc.source = discord.PCMVolumeTransformer(vc.source)
        vc.source.volume = volume
        
        while length != 1:
            await asyncio.sleep(1) 
        else:
            await ctx.voice_client.disconnect() 
            
            
@Bot.command()
async def radio(ctx, *, name, volume = 0.5):
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

    elif name == 'phonk' or name == 'фонк' or name == 'radio phonk':
        source = 'https://bit.ly/3oMtrF7'
        url = 'https://bit.ly/39O1QPw'
        embed = discord.Embed(description = f'Now playing: [Phonk](https://101.ru/radio/user/865080) [{author.mention}]', color = 0xbc03ff)
        embed.set_author(name = 'Radio', icon_url = url)
        embed.set_footer(text = "supports by quantsound")
        await ctx.send(embed = embed)
        
    elif name == 'радио рекорд' or name == 'radio record' or name == 'радио record' or name == 'record':
        source = 'http://air2.radiorecord.ru:805/rr_320'
        url = 'https://i.ibb.co/7NjgCS7/record-image.png'
        embed = discord.Embed(description = f'Now playing: [Radio Record](https://www.radiorecord.ru) [{author.mention}]', color = 0xbc03ff)
        embed.set_author(name = 'Radio', icon_url = url)
        embed.set_footer(text = "supports by quantsound")
        await ctx.send(embed = embed)

    elif name == 'record deep' or name == 'deep' or name == 'радио deep' or name == 'radio deep':
        source = 'http://air2.radiorecord.ru:805/deep_320'
        url = 'https://i.ibb.co/bm0kLDc/deep.png'
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
    
    elif name == 'pirate station' or name == 'dnb' or name == 'record pirate station' or name == 'пиратская станция':
        source = 'https://air.radiorecord.ru:805/ps_128'
        url = 'https://i.ibb.co/x1NMzxH/pirate-station.png'
        embed = discord.Embed(description = f'Now playing: [Record Pirate Station](https://www.radiorecord.ru) [{author.mention}]', color = 0xbc03ff)
        embed.set_author(name = 'Radio', icon_url = url)
        embed.set_footer(text = "supports by quantsound")
        await ctx.send(embed = embed)
    
    elif name == 'black rap' or name == 'rap' or name == 'record black rap':
        source = 'https://air.radiorecord.ru:805/yo_128'
        url = 'https://i.ibb.co/bPN6R49/black-rap.png'
        embed = discord.Embed(description = f'Now playing: [Record Black Rap](https://www.radiorecord.ru) [{author.mention}]', color = 0xbc03ff)
        embed.set_author(name = 'Radio', icon_url = url)
        embed.set_footer(text = "supports by quantsound")
        await ctx.send(embed = embed)
        
    elif name == 'trap' or name == 'record trap':
        source = 'https://air.radiorecord.ru:805/trap_128'
        url = 'https://i.ibb.co/f0DGsG2/trap.png' 
        embed = discord.Embed(description = f'Now playing: [Record Trap](https://www.radiorecord.ru) [{author.mention}]', color = 0xbc03ff)
        embed.set_author(name = 'Radio', icon_url = url)
        embed.set_footer(text = "supports by quantsound")
        await ctx.send(embed = embed)
        
    elif name == 'rock' or name == 'record rock':
        source = 'https://air.radiorecord.ru:805/rock_128'
        url = 'https://i.ibb.co/JWLVFTz/rock.png'
        embed = discord.Embed(description = f'Now playing: [Record Rock](https://www.radiorecord.ru) [{author.mention}]', color = 0xbc03ff)
        embed.set_author(name = 'Radio', icon_url = url)
        embed.set_footer(text = "supports by quantsound")
        await ctx.send(embed = embed)
        
    elif name == 'dubstep' or name == 'record dubstep':
        source = 'https://air.radiorecord.ru:805/dub_128'
        url = 'https://i.ibb.co/kmqtvn3/dubstep.png'
        embed = discord.Embed(description = f'Now playing: [Record Dubstep](https://www.radiorecord.ru) [{author.mention}]', color = 0xbc03ff)
        embed.set_author(name = 'Radio', icon_url = url)
        embed.set_footer(text = "supports by quantsound")
        await ctx.send(embed = embed)
    
    elif name == 'core' or name == 'core radio':
        source = 'https://music.coreradio.ru/radio'
        url = 'https://bit.ly/2O6UcYk'
        embed = discord.Embed(description = f'Now playing: [CORE RADIO](https://coreradio.ru) [{author.mention}] \n\n⚠️ At this radio, the stream freezes a little at the very beginning, I advise you to wait 15 seconds...', color = 0xbc03ff)
        embed.set_author(name = 'Radio', icon_url = url)
        embed.set_footer(text = "supports by quantsound")
        await ctx.send(embed = embed)
        
    elif name == 'dnb classic' or name == 'record dnb classic':
        source = 'https://air.radiorecord.ru:805/drumhits_128' 
        url = 'https://i.ibb.co/PZTPFyd/dnb-classic-icon.png'
        embed = discord.Embed(description = f'Now playing: [CORE RADIO](https://coreradio.ru) [{author.mention}] \n\n⚠️ At this radio, the stream freezes a little at the very beginning, I advise you to wait 15 seconds...', color = 0xbc03ff)
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
async def help_play(ctx):
    embed = discord.Embed(title = 'List of available services', description = available_services)
    embed.set_footer(text = "supports by quantsound")
    message = await ctx.send(embed = embed)
    await asyncio.sleep(15)
    await message.delete()

    
@Bot.command()
async def help_radio(ctx):
    embed = discord.Embed(title = 'List of available radio stations', description = help_message)
    embed.set_footer(text = "supports by quantsound")
    message = await ctx.send(embed = embed)
    await asyncio.sleep(15)
    await message.delete()
    
  
@Bot.command()
async def help(ctx):
    author = ctx.message.author
    embed = discord.Embed(description = f'**Hello, {author.mention}! List of all commands:**\n'
                          f'• `{prefix}help` outputs the help command;\n'
                          f'• `{prefix}play` (aliases: `{prefix}p`) playback songs/streams. Arguments: the query or the reference, '
                          f'the list of services is available by the command `{prefix}help_play`;\n'
                          f'• `{prefix}radio` playing the radio. The radio list is available by command: `{prefix}help_radio`;\n'
                          f'• `{prefix}volume` changing the volume. Arguments: integer from 0 to 100;\n'
                          f'• `{prefix}pause` pause the current playback;\n'
                          f'• `{prefix}resume` continue playing;\n'
                          f'• `{prefix}stop` (aliases: `{prefix}leave`) full stop of playback with subsequent disconnection of the bot from the voice channel;\n'
                          f'• `{prefix}author` all information about the authors of quantsound;\n'
                          f'• `{prefix}donate` assistance to developers of the bot;\n'
                          f'• `{prefix}servers` find out information about servers. It works only on the home server and displays the number of servers on which the bot is installed.\n\n\n'
                          '[Invite quantsound](https://discord.com/oauth2/authorize?client_id=795312210343624724&permissions=8&scope=bot) | [Support server](https://discord.gg/MFGmBFjgXu)', color = 0xbc03ff)
    embed.set_author(name = "Quantsound Support", icon_url = "https://bit.ly/39w96yc")
    embed.set_footer(text = "supports by quantsound")
    await ctx.send(embed = embed)


@Bot.command(aliases = ['AUTHOR'])
async def author(ctx):
    embed = discord.Embed(title = 'Our team:', description = f'• Developer: **[Dennis]({vk_page})**,\n'
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
                                        f'• [QIWI]({qiwi_url}),\n'
                                        f'• [ЮMoney]({yoomoney_url}),\n\n'
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
       


Bot.run(str(token))

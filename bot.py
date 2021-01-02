import asyncio
import os
import discord
import youtube_dl

from youtube_dl import YoutubeDL
from asyncio import sleep
from discord.ext import commands
from discord.ext.commands import Bot
from discord.utils import get
from discord import FFmpegPCMAudio

YDL_OPTIONS = {'format': 'worstaudio/best', 'noplaylist': 'True', 'simulate': 'True', 'preferredquality': '192', 'preferredcodec': 'mp3', 'key': 'FFmpegExtractAudio'}
FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

youtube_dl.utils.bug_reports_message = lambda: ''

intents = discord.Intents.all()
Bot = commands.Bot(command_prefix = ["/"], intents = discord.Intents.all())

@Bot.command(aliases = ['p'])
async def play(ctx, *, arg):
    voice_channel = ctx.message.author.voice.channel
    vc = await voice_channel.connect()
    if vc.is_playing():
        await ctx.send(f'{ctx.message.author.mention}, музыка уже проигрывается.')
    else:
        correct_url = url[:8]
        correct_url1 = 'https://'
        correct_search = 'ytsearch:' + url
        if correct_url != correct_url1:
            with YoutubeDL(YDL_OPTIONS) as ydl:
                info = ydl.extract_info(arg, download = False)
                URL = info['entries'][0]['formats'][0]['url']
        else: 
            with YoutubeDL(YDL_OPTIONS) as ydl:
                info = ydl.extract_info(arg, download = False)
                URL = info['formats'][0]['url']
        vc.play(discord.FFmpegPCMAudio(executable = "/app/vendor/ffmpeg/ffmpeg", source = URL, **FFMPEG_OPTIONS))

        while vc.is_playing():
            await sleep(1)
        else:
            if not vc.is_paused():
                await vc.disconnect()
            
token = os.environ.get('bot_token')
Bot.run(str(token))
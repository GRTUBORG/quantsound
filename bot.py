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

os.system('whereis ffmpeg')

YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'False'}
FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

youtube_dl.utils.bug_reports_message = lambda: ''

intents = discord.Intents.all()
Bot = commands.Bot(command_prefix = ["/"], intents = discord.Intents.all())

@Bot.command()
async def play(ctx, *, arg):
    voice_channel = ctx.message.author.voice.channel
    vc = await voice_channel.connect()
    if vc.is_playing():
        await ctx.send(f'{ctx.message.author.mention}, музыка уже проигрывается.')

    else:
        with YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(arg, download=False)

        vc.play(discord.FFmpegPCMAudio(executable="usr/bin/ffmpeg", source='https://r8---sn-ug5onuxaxjvh-n8vs.googlevideo.com/videoplayback?expire=1609636824&ei=eMfwX7S8Io2q7ATQzL_ADg&ip=83.234.194.36&id=o-APJZUIRGTkaruVSk8xwa5E2oktuaJPI5YlSK5lgaEoXK&itag=251&source=youtube&requiressl=yes&mh=u4&mm=31%2C26&mn=sn-ug5onuxaxjvh-n8vs%2Csn-c0q7lnse&ms=au%2Conr&mv=m&mvi=8&pcm2cms=yes&pl=23&initcwndbps=1048750&vprv=1&mime=audio%2Fwebm&ns=4Ta7eNxkNF2BkM_QvfvmktwF&gir=yes&clen=4565902&dur=258.001&lmt=1586535074122859&mt=1609615002&fvip=4&keepalive=yes&c=WEB&txp=5531432&n=nqdROdq3TpToQUmM&sparams=expire%2Cei%2Cip%2Cid%2Citag%2Csource%2Crequiressl%2Cvprv%2Cmime%2Cns%2Cgir%2Cclen%2Cdur%2Clmt&lsparams=mh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpcm2cms%2Cpl%2Cinitcwndbps&lsig=AG3C_xAwRgIhALE4uQVS8EgKfHlt1pWn-jWv0NLJMnAdQ0AlipoPZ60mAiEAmvr4dAUfVjkyHqtyA8I4OLptQpZOuLeV7ImYY8eMiVE%3D&sig=AOq0QJ8wRgIhAJ95gcFzfKSfndmHjYIkiAJ4WUkQvezAiFVvyvg-mSEYAiEAusiXMNRjkSfNRD_MQHj6_U1UBMhnx6cAeTYa-pWoyRY=&ratebypass=yes', **FFMPEG_OPTIONS))

        while vc.is_playing():
            await sleep(1)
        if not vc.is_paused():
            await vc.disconnect()
            
token = os.environ.get('bot_token')
Bot.run(str(token))

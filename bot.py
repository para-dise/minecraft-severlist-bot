from discord.ext import commands
import asyncio
import discord
import requests
import traceback
import time
import socket
import re
import eventlet
import aiohttp
from random import randint
import string
import fileinput
import glob, os
import aiofiles
from IPy import IP
import mcstatus
import validators
from mcstatus import MinecraftServer

blacklisted_memes = []
exempt = []

prefix = "$"
bot = commands.Bot(command_prefix=prefix, self_bot=False)
bot.remove_command('help')

async def sfilter(s):
    return s.replace(":", "U+205A")

@bot.event
async def on_ready():
  print("Bot on")
  await bot.change_presence(game=discord.Game(name="with 0 servers", url="https://twitch.tv/~", type=1))

@bot.event
async def on_command_error(error, ctx):
    error = getattr(error, 'original', error)
    if isinstance(error, commands.MissingRequiredArgument):
        await bot.send_message(ctx.message.channel, "Missing an argument.")

@bot.command(pass_context=False)
async def help():
    helpmsg = discord.Embed(title='Help', description='$help - show this message\n$server add [server ip/domain] [server port] [server icon] [server name] [server description]\n$server info [server name]', colour=0xcc6666)
    await bot.say(embed=helpmsg)

@bot.group(pass_context=True)
async def server(ctx):
    if ctx.invoked_subcommand is None:
        await bot.say("Did you mean ``$server add [name]``?")

@server.command(pass_context=True)
async def add(ctx, ip, port, icon, server_name, *, server_description):
        print("Name: {}\nDescription: {}\nIP: {}:{}".format(server_name,server_description,ip,port))
        server_name = await sfilter(server_name)
        server_description = await sfilter(server_description)
        ip = await sfilter(ip)
        port = await sfilter(port)
        inserticon = icon.replace(":", "✞")
        async with aiofiles.open('servers.txt') as f:
            async for line in f:
                parsedline = line.split(":")
                if parsedline[2] == server_name or parsedline[0] == ip:
                    badip = discord.Embed(title='Add Error', description='The ``name or IP`` specified is already in use.', colour=0xFF4945)
                    await bot.say(embed=badip)
                    return
        if len(server_name) <= 5 or len(server_description) <= 10:
            badip = discord.Embed(title='Add Error', description='The ``name or description`` specified is too short.', colour=0xFF4945)
            await bot.say(embed=badip)
            return
        badip = 0
        try:
            IP(str(ip))
        except:
            rundomain = True
        if rundomain == True:
            if not validators.domain(ip):
                badip = 1
            else:
                pass
        else:
            pass
        if badip == 1:
            badip = discord.Embed(title='Add Error', description='The ``IP`` specified is invalid.', colour=0xFF4945)
            await bot.say(embed=badip)
            return
        try:
            x = int(port)
            x += 1
        except:
            badport = discord.Embed(title='Add Error', description='The ``port`` specified is invalid.', colour=0xFF4945)
            await bot.say(embed=badport)
            return
        if len(str(server_description)) > 160 or len(str(server_name)) > 20:
            badlen = discord.Embed(title='Add Error', description='The ``name or description`` is too long. \nMax name length: 20 chars. \nMax description length: 160 chars.', colour=0xFF4945)
            await bot.say(embed=badlen)
            return
        printname = server_name.replace("U+205A", ":")
        printdesc = server_description.replace("U+205A", ":")
        emb = discord.Embed(title='Server Added', description='**Server Info**\n\nServer Name: ``{}``\nServer Description: ``{}``\nServer IP: ``{}:{}``\nOwner: ``{}``'.format(printname,printdesc,ip,port,ctx.message.author), colour=0x2AC940)
        emb.set_thumbnail(url=icon)
        await bot.say(embed=emb)
        str2write = ip + ":" + port + ":" + server_name + ":" + server_description + ":" + str(ctx.message.author) + ":" + str(ctx.message.author.id) + ":" + str(inserticon) + "\n"
        async with aiofiles.open('servers.txt', 'a') as dbfile:
            await dbfile.write(str2write)

@server.command(pass_context=False)
async def info(servername):
    async with aiofiles.open('servers.txt') as f:
        async for line in f:
            line_params = line.split(":")
            servercountint = 0
            if servername == line_params[2]:
                servercountint += 1
                sip = line_params[0]
                sport = line_params[1]
                sname = line_params[2]
                sname = sname.replace("U+205A", ":")
                sdesc = line_params[3]
                sdesc = sdesc.replace("U+205A", ":")
                sownr = line_params[4]
                sicon = line_params[6]
                sicon = sicon.replace("✞", ":")
                try:
                    formatted = str(sip) + ":" + str(sport)
                    server = MinecraftServer.lookup(formatted)
                    status = server.status()
                except Exceptin as e:
                    print(e)
                emb = discord.Embed(title='Server Found', description='**Server Info**\n\nServer Name: ``{}``\nServer Description: ``{}``\nServer IP: ``{}:{}``\nOwner: ``{}``\nPlayers Online: ``{}``\nPing: ``{}``'.format(sname, sdesc, sip, sport, sownr, status.players.online, status.latency), colour=0x2AC940)
                emb.set_thumbnail(url=sicon)
                await bot.say(embed=emb)
    if servercountint != 0:
        badip = discord.Embed(title='Add Error', description='The ``name or IP`` specified is already in use.', colour=0xFF4945)
        await bot.say(embed=badip)


bot.run('your_token', bot=True)

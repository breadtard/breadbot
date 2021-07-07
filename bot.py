#!/usr/bin/env python
import json
import discord
from discord.ext import commands

# wacky shenanigans to import token and ids from file
print("Importing data from secrets file...")
secrets_file = 'breadbot-secrets'
with open(secrets_file) as f:
    breadbot_secrets = f.read()
print("Reconstructing data as dict...")
secrets = json.loads(breadbot_secrets)
del(breadbot_secrets)
# end of wacky shenanigans 

client = commands.Bot(command_prefix='^')

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        invalid_args = discord.Embed(title='Error', color=0xff0000)
        invalid_args.add_field(name='Invalid amount of arguments', value='Missing arguments..', inline=False)
        await ctx.send(embed=invalid_args)
    if isinstance(error, commands.MissingPermissions):
        invalid_perms = discord.Embed(title='Error', color=0xff0000)
        invalid_perms.add_field(name='Permission denied', value='You dont have the permission to use this command.', inline=False)
        await ctx.send(embed=invalid_perms)

#The below code bans player.
@client.command()
@commands.has_permissions(ban_members = True)
async def ban(ctx, member : discord.Member, *, reason = None):
    banembed = discord.Embed(title='Clown down!', color=0x123456)
    banembed.add_field(name=f'Banned {member.mention}.', value=f'Ban reason: {reason}')
    await member.send(embed=banembed)
    await ctx.send(embed=banembed)
    await member.ban(reason=f"[BOT] {reason}")
    print(f'[ADMIN] {ctx.message.author} banned {member} for {reason}')
    return

@client.command()
async def ping(ctx):
    await ctx.send(f':ping_pong: ponggers ({client.latency})')
    print(f'[PONGGERS] {ctx.message.author} ponged')
    return

@client.command()
@commands.has_permissions(kick_members = True)
async def kick(ctx, member : discord.Member, *, reason = None):
    kickembed = discord.Embed(title='Clown down', color=0x123456)
    kickembed.add_field(name=f'Kicked {member.mention}.', value=f'Reason: {reason}')
    await member.send(embed=kickembed)
    await ctx.send(embed=kickembed)
    await member.kick(reason=f"[BOT] {reason}")
    print(f'[ADMIN] {ctx.message.author} kicked {member} for {reason}')
    return

@client.command()
async def mkembed(ctx, *, content: str):
    title, description, image = content.split('|')
    embed = discord.Embed(title=title, description=description, color=0x123456)
    if image != 'none':
        embed.set_image(url=image)
    await ctx.channel.purge(limit=1)
    await ctx.send(embed=embed)
    print(f'[BOT] {ctx.message.author} made an embed. Title: {title}. Description: {description}. Image: {image}.')
    return

@client.command()
async def commands(ctx):

    kick_help = discord.Embed(title="Commands", color=0x123456)
    kick_help.add_field(name='^kick <user> <reason>', value='Kicks a clown for the specified reason.', inline=False)
    kick_help.add_field(name='Arguments', value='<user> - A discord user. <reason> - Any string. This will be shown to the kicked user.', inline=False)
    kick_help.add_field(name='Permissions', value='This command requires the `kick_users` permission.', inline=False)

    ban_help = discord.Embed(title="Commands", color=0x123456)
    ban_help.add_field(name='^ban <user> <reason>', value='Bans a clown for the specified reason.', inline=False)
    ban_help.add_field(name='Arguments', value='<user> - A discord user. <reason> - Any string. This will be shown to the banned user.', inline=False)
    ban_help.add_field(name='Permissions', value='This command requires the `ban_users` permission.', inline=False)

    ping_help = discord.Embed(title="Commands", color=0x123456)
    ping_help.add_field(name='^ping', value='Tests if the bot is online and shows the latency.', inline=False)
    ping_help.add_field(name='Arguments', value='This command takes no arguments, and any specified arguments will be ignored', inline=False)
    ping_help.add_field(name='Permissions', value='This command doesnt require any permissions, and anyone can use it', inline=False)

    embed_help = discord.Embed(title="Commands", color=0x123456)
    embed_help.add_field(name='^mkembed <title> | <text> | <image link>', value='Makes an embed with an image and the specified text. Can be used to make low quality memes.', inline=False)
    embed_help.add_field(name='Arguments', value='<title> - Any text. Will be used as the embed title. <text> - Any text. Will be used as the embed desc. <image link> - A link to an image. Currently supports imgur, and raw image links (ex. http://http.cat/404.jpg)', inline=False)
    embed_help.add_field(name='Permissions', value='This command doesnt require any permissions, and anyone can use it', inline=False)

    help_help = discord.Embed(title="Commands", color=0x123456)
    help_help.add_field(name='^commands', value='guess.')

    clear_help = discord.Embed(title="Commands", color=0x123456)
    clear_help.add_field(name='^clear <amount>', value='Clears the specified amount of messages.', inline=False)
    clear_help.add_field(name='Arguments', value='<amount> - The number of messages to delete.', inline=False)
    clear_help.add_field(name='Permissions', value='This command requires the `manage_messages` permission.', inline=False)

    stop_help = discord.Embed(title="Commands", color=0x123456)
    stop_help.add_field(name='^stop', value='Stops the bot.', inline=False)
    stop_help.add_field(name='Arguments', value='This command takes no arguments, and any specified arguments will be ignored', inline=False)
    stop_help.add_field(name='Permissions', value='This command can only be user by <@429354512453730325>', inline=False)

    dm_help = discord.Embed(title="Commands", color=0x123456)
    dm_help.add_field(name='^dm <user> <message>', value='DMs a user a message. Can be used to warn people.', inline=False)
    dm_help.add_field(name='Arguments', value='<user> - A discord user. <message> - A message the bot will send to the user.', inline=False)
    dm_help.add_field(name='Permissions', value='This command reqiures the `manage_members` permission.', inline=False)

    print(f'[BOT] {ctx.message.author} requested help')

    commands_pages = [kick_help, ban_help, ping_help, embed_help, help_help, clear_help, stop_help, dm_help]

    message = await ctx.send(embed = kick_help)
    await message.add_reaction('◀')
    await message.add_reaction('▶')

    def check(reaction, user):
        return user == ctx.author

    i = 0
    reaction = None

    while True:
        if str(reaction) == '◀':
            if i > 0:
                i -= 1
                await message.edit(embed = commands_pages[i])
        elif str(reaction) == '▶':
            if i < 7:
                i += 1
                await message.edit(embed = commands_pages[i])

        try:
            reaction, user = await client.wait_for('reaction_add', timeout = 30.0, check = check)
            await message.remove_reaction(reaction, user)
        except:
            break

    await message.clear_reaction()

@client.command()
async def dm(ctx, user: discord.User, *, value):
        if ctx.author.guild_permissions.manage_messages:
            dm_embed = discord.Embed(title='A message from the mods.', description="You've got mail.", color=0xff0000)
            dm_embed.add_field(name='Message contens:', value=value, inline=False)
            await user.send(embed=dm_embed)
            await ctx.channel.purge(limit=1)
            print(f'[ADMIN] {ctx.message.author} sent message to {user}. Message contents: {value}')
        else:
           invalid_perms = discord.Embed(title='Error', color=0xff0000)
           invalid_perms.add_field(name='Permission denied', value='You dont have the permission to use this command.', inline=False)
           await ctx.send(embed=invalid_perms)
        return

@client.command()
async def clear(ctx, amount=5):
    if ctx.author.guild_permissions.manage_messages:
        amount = amount + 1
        await ctx.channel.purge(limit=amount)
        amount = amount - 1
        clrembed = discord.Embed(title='Clear', color=0x123456)
        clrembed.add_field(name='Teletubbies vacuum.', value=f'Number of messages deleted: {amount}')
        await ctx.send(embed=clrembed)
        print(f'[ADMIN] Cleared {amount} messages in {ctx.channel}. Invoked by {ctx.message.author}')
    return

@client.command()
async def stop(ctx):
    if ctx.message.author.id == secrets["owner"]:
        stop_embed = discord.Embed(title='Shutting down...', color=0x00ff00)
        stop_embed.set_image(url='https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fi.ytimg.com%2Fvi%2FZxGE252tuWw%2Fmaxresdefault.jpg&f=1&nofb=1')
        await ctx.send(embed=stop_embed)
        print(f'[ADMIN] !!! Bot stop routine invoked by {ctx.message.author} !!!')
        print('[STOP] Stopped logging')
        import sys
        print('[STOP] Stopping bot')
        sys.exit()
    else:
        invalid_perms = discord.Embed(title='Error', color=0xff0000)
        invalid_perms.add_field(name='Missing permissions', value='You cant use this command. Go away', inline=False)
        await ctx.send(embed=invalid_perms)
        print(f'[PERMISSION ERROR] Stop command invoked by {ctx.message.author}. Missing permissions.')
        return

@client.event
async def on_ready():
    print('[BOT] Bot ready.')
    print('[BOT] Started logging')
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="people"))

#The below code runs the bot.
print("booting up, butter cup...")
print("using token: " + secrets["token"])
print("----------------------")
client.run(secrets["token"], bot=True)

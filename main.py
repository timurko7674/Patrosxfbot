import discord
from discord.ext import commands, tasks
import requests
import os

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix='/', intents=intents)

# Basic Bot Events
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    fetch_roblox_status.start()

# Command to check bot owner's ID
@bot.command()
async def check_owner(ctx):
    if ctx.author.id == 1025675124457873459:
        await ctx.send('You are the bot owner!')
    else:
        await ctx.send('You are not the bot owner.')

# Moderation commands
@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f'User {member} has been kicked for {reason}')

@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f'User {member} has been banned for {reason}')

@bot.command()
@commands.has_permissions(manage_messages=True)
async def mute(ctx, member: discord.Member, *, reason=None):
    guild = ctx.guild
    muted_role = discord.utils.get(guild.roles, name="Muted")

    if not muted_role:
        muted_role = await guild.create_role(name="Muted")

        for channel in guild.channels:
            await channel.set_permissions(muted_role, speak=False, send_messages=False)

    await member.add_roles(muted_role, reason=reason)
    await ctx.send(f'User {member} has been muted for {reason}')

@bot.command()
@commands.has_permissions(manage_messages=True)
async def unmute(ctx, member: discord.Member):
    muted_role = discord.utils.get(ctx.guild.roles, name="Muted")
    await member.remove_roles(muted_role)
    await ctx.send(f'User {member} has been unmuted')

@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int):
    await ctx.channel.purge(limit=amount)
    await ctx.send(f'Cleared {amount} messages', delete_after=3)

# Roblox status command
@tasks.loop(hours=1)
async def fetch_roblox_status():
    response = requests.get('https://status.roblox.com/')
    status_data = response.json()
    status_description = status_data.get("status", {}).get("description", "No status available")
    channel = bot.get_channel(YOUR_CHANNEL_ID)  # Replace with your channel ID
    await channel.send(f'Roblox Status: {status_description}')

@bot.command()
async def status(ctx):
    response = requests.get('https://status.roblox.com/')
    status_data = response.json()
    status_description = status_data.get("status", {}).get("description", "No status available")
    await ctx.send(f'Roblox Status: {status_description}')

# Command to setup status and news
@bot.command()
@commands.has_permissions(administrator=True)
async def setup(ctx, command: str):
    if command == 'status':
        await ctx.send('Status setup complete.')
    elif command == 'news':
        await ctx.send('News setup complete.')
    else:
        await ctx.send('Invalid setup command.')

bot.run(os.getenv('brdyUTvJDyR-OOjdRMNdAQo0hfi17V0E'))

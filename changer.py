import discord
from discord.ext import tasks, commands
import os
import datetime
import random

intents = discord.Intents.default()
intents.guilds = True

bot = commands.Bot(command_prefix='!', intents=intents)

shuffled_icons = []
current_icon_index = 0

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    change_icon.start()

@tasks.loop(hours=2)
async def change_icon():
    global current_icon_index, shuffled_icons
    guild_id = '!!!!'  # Replace with your guild ID
    guild = discord.utils.get(bot.guilds, id=int(guild_id))
    if guild and shuffled_icons:
        icon_file = shuffled_icons[current_icon_index]
        with open(icon_file, 'rb') as icon:
            await guild.edit(icon=icon.read())
            print(f"Changed icon to {icon_file}")
        current_icon_index += 1  # Move to the next icon
        if current_icon_index >= len(shuffled_icons):  # If all icons have been used
            random.shuffle(shuffled_icons)  # Reshuffle the list for randomness
            current_icon_index = 0  # Reset index

@change_icon.before_loop
async def before_change_icon():
    global shuffled_icons
    await bot.wait_until_ready()
    icons = [f for f in os.listdir('.') if f.endswith(('.png', '.jpg', '.jpeg', '.gif')) and f.split('.')[0].isdigit()]
    random.shuffle(icons)  # Shuffle the list of icons
    shuffled_icons = icons  # Store the shuffled list

bot.run('!!!!')  # Replace with your bot token

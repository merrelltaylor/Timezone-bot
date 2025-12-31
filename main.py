import discord
import asyncio
from datetime import datetime
import pytz
import os
from discord import app_commands

# -----------------------------
# Environment variables
# -----------------------------
TOKEN = os.getenv("TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))

# -----------------------------
# Discord client
# -----------------------------
intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

# -----------------------------
# Timezones
# -----------------------------
timezone_dict = {
    "🇧🇷 São Paulo": "America/Sao_Paulo",
    "🇵🇱 Warsaw": "Europe/Warsaw",
    "🇸🇦 Dammam": "Asia/Riyadh",
    "🇸🇬 Singapore": "Asia/Singapore",
    "🇯🇵 Tokyo": "Asia/Tokyo",
    "🇦🇺 Sydney": "Australia/Sydney",
}

# -----------------------------
# Build the embed
# -----------------------------
def build_embed():
    embed = discord.Embed(
        title="🌍 Server Region Times",
        color=0x2b2d31,
        timestamp=datetime.utcnow()
    )

    target_hour = 3  # target hour (3 AM)
    closest_region = None
    min_diff = 24  # max possible hour difference

    current_hours = {}
    # Step 1: determine which server is closest to 3 AM
    for region, tz in timezone_dict.items():
        now = datetime.now(pytz.timezone(tz))
        current_hours[region] = now.hour
        diff = abs(now.hour - target_hour)
        if diff < min_diff:
            min_diff = diff
            closest_region = region

    # Step 2: build embed, add ⭐ to closest server
    for region, tz in timezone_dict.items():
        now = datetime.now(pytz.timezone(tz))
        star = " ⭐" if region == closest_region else ""
        embed.add_field(
            name=region,
            value=f"**{now.strftime('%H:%M')}**{star}",
            inline=True
        )

    embed.set_footer(text="Updates every hour • Auto timezone")
    return embed

# -----------------------------
# On ready
# -----------------------------
@client.event
async def on_ready():
    print(f"Logged in as {client.user}")
    await tree.sync()
    client.loop.create_task(hourly_post())

# -----------------------------
# Hourly post task
# -----------------------------
async def hourly_post():
    await client.wait_until_ready()
    channel = client.get_channel(CHANNEL_ID)

    while not client.is_closed():
        try:
            await channel.send(embed=build_embed())
        except Exception as e:
            print(f"Error posting embed: {e}")
        await asyncio.sleep(3600)  # wait 1 hour

# -----------------------------
# Slash command
# -----------------------------
@tree.command(name="timezones", description="Show current server region times")
async def timezones_command(interaction: discord.Interaction):
    await interaction.response.send_message(embed=build_embed())

# -----------------------------
# Run bot
# -----------------------------
client.run(TOKEN)

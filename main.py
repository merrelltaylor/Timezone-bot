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

    # Get current hour for each server
    current_hours = {}
    for region, tz in timezone_dict.items():
        now = datetime.now(pytz.timezone(tz))
        current_hours[region] = now.hour

    # Find the earliest hour
    min_hour = min(current_hours.values())

    # Add fields to embed with ⭐ for earliest time
    for region, tz in timezone_dict.items():
        now = datetime.now(pytz.timezone(tz))
        star = " ⭐" if current_hours[region] == min_hour else ""
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
        await asyncio.sleep(3600)  # 1 hour

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

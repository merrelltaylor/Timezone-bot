import discord
import asyncio
from datetime import datetime
import pytz
import os
from discord import app_commands

TOKEN = os.getenv("TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

timezones_dict = {
    "🇧🇷 São Paulo": "America/Sao_Paulo",
    "🇵🇱 Warsaw": "Europe/Warsaw",
    "🇸🇦 Dammam": "Asia/Riyadh",
    "🇸🇬 Singapore": "Asia/Singapore",
    "🇯🇵 Tokyo": "Asia/Tokyo",
    "🇦🇺 Sydney": "Australia/Sydney",
}

def build_embed():
    embed = discord.Embed(
        title="🌍 Server Region Times",
        color=0x2b2d31,
        timestamp=datetime.utcnow()
    )

    for region, tz in timezones_dict.items():
        now = datetime.now(pytz.timezone(tz))
        star = " ⭐" if 18 <= now.hour <= 23 else ""
        embed.add_field(
            name=region,
            value=f"**{now.strftime('%H:%M')}**{star}",
            inline=True
        )

    embed.set_footer(text="Updates every hour • Auto timezone")
    return embed

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")
    await tree.sync()
    client.loop.create_task(hourly_post())

async def hourly_post():
    await client.wait_until_ready()
    channel = client.get_channel(CHANNEL_ID)

    while not client.is_closed():
        await channel.send(embed=build_embed())
        await asyncio.sleep(3600)

@tree.command(name="timezones", description="Show current server region times")
async def timezones(interaction: discord.Interaction):
    await interaction.response.send_message(embed=build_embed())

client.run(TOKEN)

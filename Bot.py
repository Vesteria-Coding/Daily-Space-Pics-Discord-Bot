import os
import discord
import requests
from discord.ext import tasks

# Setup Credentials
BOT_TOKEN = 'BOT_TOKEN_HERE'       # Replace With Bot Token
GUILD_ID = 1361781854700572682
CHANNEL_ID = 1391757023355338843    # Channel ID Here
API_KEY = "NASA_API_KEY_HERE"      # Replace With API Key
URL = f"https://api.nasa.gov/planetary/apod?api_key={API_KEY}"
last_image_url = ''

# Setup
intents = discord.Intents.all()
client = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(client)

@tasks.loop(hours=3)
async def auto_message():
    global last_image_url
    response = requests.get(URL).json()
    image_url = response["hdurl"] if "hdurl" in response else response["url"]
    title = response["title"]
    description = response["explanation"]
    img_data = requests.get(image_url).content
    if last_image_url != image_url:
        with open("space_image.jpg", "wb") as f:
            f.write(img_data)
        channel = await client.fetch_channel(CHANNEL_ID)
        if channel:
            embed = discord.Embed(title=title, description=description, color=0x5D3A99)
            embed.set_image(url="attachment://space_image.jpg")
            file = discord.File("space_image.jpg", filename="space_image.jpg")
            await channel.send(file=file, embed=embed)
        os.remove("space_image.jpg")
        last_image_url = image_url

@client.event
async def on_ready():
    print(f"Bot is ready. Logged in as {client.user} (ID: {client.user.id})")
    await tree.sync(guild=discord.Object(id=GUILD_ID))
    auto_message.start()  # ✅ Start the background task

# Commands
@tree.command(name="ping", description="Sends ping of bot", guild=discord.Object(id=GUILD_ID))
async def ping(interaction: discord.Interaction):
    latency = client.latency * 1000
    await interaction.response.send_message(f'Pong! `{latency:.2f}ms`', ephemeral=True)

# Run the bot
client.run(BOT_TOKEN)

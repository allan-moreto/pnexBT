# bot.py
import discord
import threading
import grinding
import os

DISCORD_TOKEN = os.environ.get("DISCORD_TOKEN")

# Enable message content intent
intents = discord.Intents.default()
intents.message_content = True
intents.messages = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"Bot is logged in as {client.user}")

@client.event
async def on_message(message):
    # ignore messages from the bot itself
    if message.author == client.user:
        return
    
    content = message.content.strip()
    print(f"{message.author}: {content}")

    if content.startswith("!"):
        parts = content.split(" ", 1)  # split into command and rest
        command = parts[0].lower()     # the command, e.g., !reply
        arg = parts[1] if len(parts) > 1 else ""  # the rest of the message

        if command == "!message":
            print(f"Command: {command}, Argument: {arg}")
            grinding.send_message(arg)

# Function to start bot in a thread
def start_bot():
    thread = threading.Thread(target=lambda: client.run(DISCORD_TOKEN), daemon=True)
    thread.start()

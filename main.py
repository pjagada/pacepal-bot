from custom_things import LOG_FILES, ADVANCEMENT, MESSAGE, CHANNEL_ID

# IMPORT DISCORD.PY. ALLOWS ACCESS TO DISCORD'S API.
import discord
from discord.ext import tasks

# IMPORT THE OS MODULE.
import os

# IMPORT LOAD_DOTENV FUNCTION FROM DOTENV MODULE.
from dotenv import load_dotenv

# LOADS THE .ENV FILE THAT RESIDES ON THE SAME LEVEL AS THE SCRIPT.
load_dotenv()

# GRAB THE API TOKEN FROM THE .ENV FILE.
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

last_found_lines = {}
for log_file in LOG_FILES:
    last_found_lines[log_file] = ""
stamps = [0 for i in range(len(LOG_FILES))]

class MyClient(discord.Client):
    async def on_ready(self):
        guild_count = 0
        for guild in bot.guilds:
            print(f"- {guild.id} (name: {guild.name})")
            guild_count = guild_count + 1
        print("Peej Pacepal Bot is in " + str(guild_count) + " guilds.")
    
    async def setup_hook(self) -> None:
        # start the task to run in the background
        self.my_background_task.start()

    @tasks.loop(seconds=2)  # task runs every 2 seconds
    async def my_background_task(self):
        channel = self.get_channel(CHANNEL_ID)
        for i in range(len(LOG_FILES)):
            log_file = LOG_FILES[i]
            stamp = os.stat(log_file).st_mtime # gets the time the file was last modified
            if stamp != stamps[i]: # if the file was modified since the last time we checked
                stamps[i] = stamp # update the stamp
                with open(log_file, "r") as f:
                    for line in (f.readlines()[-15:]): # read the last 15 lines
                        if f"has made the advancement [{ADVANCEMENT}]" in line:
                            print("advancement in line")
                            if last_found_lines[log_file] != line: # if the line is different from the last time we checked
                                last_found_lines[log_file] = line
                                print("sending the message")
                                await channel.send(MESSAGE)
                                break
                            else: 
                                print("same line")
                                break

    @my_background_task.before_loop
    async def before_my_task(self):
        await self.wait_until_ready()  # wait until the bot logs in

# GETS THE CLIENT OBJECT FROM DISCORD.PY. CLIENT IS SYNONYMOUS WITH BOT.
bot = MyClient(intents=intents)
# EXECUTES THE BOT WITH THE SPECIFIED TOKEN.
bot.run(DISCORD_TOKEN)
from end_checking import LOG_FILES

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


last_end_lines = {}
for log_file in LOG_FILES:
    last_end_lines[log_file] = ""
stamps = [0 for i in range(len(LOG_FILES))]

class MyClient(discord.Client):
    async def on_ready(self):
        guild_count = 0
        for guild in bot.guilds:
            print(f"- {guild.id} (name: {guild.name})")
            guild_count = guild_count + 1
        print("SampleDiscordBot is in " + str(guild_count) + " guilds.")
    
    async def setup_hook(self) -> None:
        # start the task to run in the background
        self.my_background_task.start()

    @tasks.loop(seconds=2)  # task runs every 2 seconds
    async def my_background_task(self):
        channel = self.get_channel(986431075217707021)  # channel ID goes here
        for i in range(len(LOG_FILES)):
            log_file = LOG_FILES[i]
            stamp = os.stat(log_file).st_mtime
            if stamp != stamps[i]:
                stamps[i] = stamp
                with open(log_file, "r") as f:
                    for line in (f.readlines()[-15:]):
                        if "has made the advancement [The End?]" in line:
                            print("end in line")
                            if last_end_lines[log_file] != line:
                                last_end_lines[log_file] = line
                                print("sending the message")
                                await channel.send("gravel seed end enter https://www.twitch.tv/peej918")
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
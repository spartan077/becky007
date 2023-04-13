import discord
import asyncio
from discord.ext import commands
from chatgpt_ai.openai import chatgpt_response
from keepalive import keep_alive


class MyClient(discord.Client):
   
    async def on_ready(self):
        print('Logged on as ', self.user)
        channel = self.get_channel(1080083951630155878)
        await channel.send('YOU CAN USE THE FOLLOWING COMMANDS\n1. /ai or /gpt to access ChatGPT.\n2. !reminder to set a reminder in the following format:\n!reminder <time> <reminder_text>\nEnd time with d for days, h for hours, m for minutes, and s for seconds.\nExample: !reminder 1h Go for a walk\nUse !delete_reminder to delete all reminders.')
   
    async def remindme(self, ctx, time, msg):
        await ctx.send(f"Ok, I will remind you in {time} seconds : {msg}.")
        await asyncio.sleep(int(time))
        await ctx.send(f"Hey, {msg}")
   
    async def on_message(self, message):
        if message.author.bot:
            return
        if message.content.startswith("!reminder"):
            args = message.content.split()[1:]
            if len(args) < 2:
                await message.channel.send('Use Format: !reminder <time> <reminder_text> \n end time with d for days , h for hours , m for minutes and s for seconds , you can use decimal values \n !delete_reminder will delete all reminders')
                return
            time = args[0]
            seconds = 0
            if time.lower().endswith("d"):
                seconds += float(time[:-1]) * 60 * 60 * 24
                counter = f"{seconds // 60 // 60 // 24} days"
            if time.lower().endswith("h"):
                seconds += float(time[:-1]) * 60 * 60
                counter = f"{seconds // 60 // 60} hours"
            if time.lower().endswith("m"):
                seconds += float(time[:-1]) * 60
                counter = f"{seconds // 60} minutes"
            if time.lower().endswith("s"):
                seconds += float(time[:-1])
                counter = f"{seconds} seconds"
            if seconds == 0:
                await message.channel.send("That my friend is no time I tell you")
                return
            msg = " ".join(args[1:])
            task = self.remindme(message.channel, seconds, msg)
            asyncio.ensure_future(task)
            await message.add_reaction("⏰")

        if message.content.startswith('!delete_reminder'):
            for task in asyncio.all_tasks():
                if task._coro.__name__ == 'remindme':
                    task.cancel()
            await message.channel.send("All reminders cancelled")
            return

        for i in ['/ai', '/gpt']:
            if message.content.startswith(i):
                await message.channel.send('ChatGPT:')
                user_message = message.content.replace(i, '')
                bot_response = chatgpt_response(prompt=user_message)
                await message.channel.send(f"answer {bot_response}")
                return
           
       

intents = discord.Intents.default()
intents.message_content = True
key = 'MTA5NDk2OTg4MTk4MTYxNjEzOQ.Gzqfk2.qXWrPBZRYaF8sy-C0XWyQLQ-0spbaCfaLJ2_bs'
client = MyClient(intents=intents)
keep_alive()
client.run(key)

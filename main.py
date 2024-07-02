import re
import os
import time
import discord
import MeCab
from keep_alive import keep_alive

client = discord.Client(intents=discord.Intents.all())
# client = discord.Client(intents=discord.Intents.default())
# tagger = MeCab.Tagger()
tagger = MeCab.Tagger('-r /etc/mecabrc')

@client.event
async def on_ready():
    print("log-in!")
    print(discord.__version__)

@client.event
async def on_message(message):
    print(message.author)
    print(message.content)
    print("---------------------")

    if message.author.bot:
        return

    start_time = time.time()
    txt = message.content
    counter = 0

    if "ゴママヨ" in txt:
        if not txt.startswith("ゴママヨ！？["):
            await message.channel.send("ゴママヨ！？")
            
            end_time = time.time()
            elapsed_time = round(end_time - start_time,5)
            await message.channel.send(f"処理時間: {elapsed_time}秒")

    if txt:
        log_master = []
        
        if re.search(r'[A-z]', txt) is not None:
            txt = re.sub(r'[A-z]', '', txt)
            log_master.append("英語は省かれました")
        if re.search(r'[0-9]', txt) is not None:
            txt = re.sub(r'[0-9]', '', txt)
            log_master.append("数字は省かれました。")
        if re.search(r'[-/:-@[-´{-~！？!?\.、\(\)\（\）。・\n…]', txt) is not None:
            txt = re.sub(r'[ -/:-@[-´{-~！？!?\.、。・\n…]', '', txt)
            log_master.append("一部記号が省かれました。")
        
        arr = tagger.parse(txt).splitlines()
        beforeSound, beforeSound2 = 0, 0
        
        for item in arr:
            try:
                sound = str(item.split(",")[-2])
                if beforeSound != 0 and beforeSound == sound[0]:
                    print("ゴママヨ！？[" + sound[0])
                    await message.channel.send("ゴママヨ！？[" + sound[0] + "]")
                    counter += 1
                if beforeSound2 != 0 and (beforeSound2 + beforeSound) == sound[:2]:
                    print("2次ゴママヨ！？[" + sound[:2])
                    await message.channel.send("2次ゴママヨ！？[" + sound[:2] + "]")
                    counter += 1
                beforeSound = str(sound[-1])
                beforeSound2 = str(sound[-2]) if len(sound) >= 2 else "0"
            except:
                pass
        if counter > 0:
            end_time = time.time()
            elapsed_time = round(end_time - start_time,5)
            await message.channel.send(f"処理時間: {elapsed_time}秒")
        
        if txt.startswith("log"):
            await message.channel.send(log_master)


TOKEN = os.getenv("DISCORD_TOKEN")
# Web サーバの立ち上げ
keep_alive()
client.run(TOKEN)

import re
import os
import time
import discord
import MeCab
import pytesseract
from PIL import Image
import requests
from io import BytesIO
from keep_alive import keep_alive
import logging

logging.basicConfig(level=logging.INFO)

client = discord.Client(intents=discord.Intents.all())
# client = discord.Client(intents=discord.Intents.default())
# tagger = MeCab.Tagger()
tagger = MeCab.Tagger("-r /etc/mecabrc")

pytesseract.pytesseract.tesseract_cmd = r"/usr/bin/tesseract"
tessdata_dir_config = '--tessdata-dir "/usr/share/tesseract-ocr/4.00/tessdata"'


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
    log_master = "[" + txt + "]" + "\n"
    If_log = False
    if txt.startswith("log"):
        If_log = True

    # 画像判別
    if message.attachments:
        for attachment in message.attachments:
            if attachment.filename.endswith(("png", "jpg", "jpeg", "gif")):
                print("画像だよ:", attachment.url)

                # 画像をダウンロードしてOCRを実行
                response = requests.get(attachment.url)
                img = Image.open(BytesIO(response.content))
                ocr_text = pytesseract.image_to_string(
                    img, lang="jpn", config=tessdata_dir_config
                )

                # OCR結果とmessage.contentを結合
                txt = (
                    "OCR_text------ \n" + "".join(ocr_text.split()) + "------------ \n"
                )
                log_master += txt
    else:
        pass

    if "ゴママヨ" in txt:
        if not txt.startswith("ゴママヨ！？["):
            await message.channel.send("ゴママヨ！？")

            end_time = time.time()
            elapsed_time = round(end_time - start_time, 5)
            await message.channel.send(f"処理時間: {elapsed_time}秒")

    if txt:

        if re.search(r"[A-z]", txt) is not None:
            txt = re.sub(r"[A-z]", "", txt)
            log_master += "\n" + "英語は省かれました"
        if re.search(r"[0-9]", txt) is not None:
            txt = re.sub(r"[0-9]", "", txt)
            log_master += "\n" + "数字は省かれました。"
        if re.search(r"[-/:-@[-´{-~！？!?\.、\(\)\（\）。・\n…]", txt) is not None:
            txt = re.sub(r"[ -/:-@[-´{-~！？!?\.、。・\n…]", "", txt)
            log_master += "\n" + "一部記号が省かれました。"

        arr = tagger.parse(txt).splitlines()
        beforeSound, beforeSound2 = 0, 0

        log_master += "\n"

        for item in arr:
            try:
                sound = str(item.split(",")[-2])
                log_master += sound + "/"
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
            elapsed_time = round(end_time - start_time, 5)
            await message.channel.send(f"処理時間: {elapsed_time}秒")

        logging.info(txt)
        logging.info(log_master)

        if If_log:
            await message.channel.send(log_master)


TOKEN = os.getenv("DISCORD_TOKEN")
# Web サーバの立ち上げ
keep_alive()
client.run(TOKEN)

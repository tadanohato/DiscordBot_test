from dotenv import load_dotenv
import asyncio
import logging
import os
import sys

# import API
import discord
from google import genai
from google.genai import types

#importUserModule
import mandelbrot as manbo #マンボ😱😱😱😱😱😱😱😱😱😱😱😱😱😱😱😱😱😱😱😱😱😱

# EnvironmentVar
load_dotenv()
G_KEY = os.getenv("GEMINI_API_KEY")
D_TOKEN = os.getenv("DISCORD_API_TOKEN")

# SetupDiscordClient
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# ジェミニありがとう✨
gemini = genai.Client(
    api_key=G_KEY,
    http_options=types.HttpOptions(
        timeout=30_000,
        retry_options=types.HttpRetryOptions(attempts=2),
    ),
)
logger = logging.getLogger(__name__)


@client.event
async def on_ready():
    print("Ready : " + str(client.user))


@client.event
async def on_message(message):
    if message.author.bot or client.user is None:
        return

    mentions = (f"<@{client.user.id}>", f"<@!{client.user.id}>")
    if not any(mention in message.content for mention in mentions):
        return

    content = message.content
    for mention in mentions:
        content = content.replace(mention, "")
    content = content.strip()
    if content == "こんにちは":
        await message.channel.send(
            "こんにちは",
            allowed_mentions=discord.AllowedMentions.none(),
        )
        return
    if "マンボ" in content:
        spc = content.split()
        c = complex(float(spc[1]),float(spc[2])) #spc["マンボ",real,imag,max]
        z = manbo.Z(c) #淫

        z.calc(2,int(spc[3])) #loop end:abs(z) > 2 or count of calc max
        for zn in z.set:
            await message.channel.send(str(zn))
        return

    if content == "contenttest":
        await message.channel.send(content.split())
        
        return
        
    if content == "それでは始めましょう✨":
        sys.exit()
        

    prompt = content + "これらとまったく関係のない、野獣邸の消失について説明して3行程度で。口調は淡々と日本では使わない漢字も使いがち"

    try:
        async with message.channel.typing():
            interaction = await asyncio.wait_for(
                gemini.aio.interactions.create(
                    model="gemini-3.8-flash",
                    input=prompt,
                ),
                timeout=30,
            )
        response = interaction.output_text
        if not response or not response.strip():
            response = "Geminiから返信が取得できませんでした。もう一度お試しください。"
    except TimeoutError:
        logger.warning("Gemini API request timed out")
        response = "Geminiの応答に時間がかかっています。少し待ってからもう一度メンションしてください。"
    except Exception as error:
        logger.exception("Gemini API request failed")
        status = getattr(error, "status_code", getattr(error, "code", None))
        if status == 503:
            response = "現在Geminiが混雑しています。少し待ってからもう一度メンションしてください。"
        elif status == 429:
            response = "Geminiの利用上限に達しました。時間をおいてからもう一度お試しください。"
        else:
            response = "Geminiへの問い合わせに失敗しました。詳しくはBotのログを確認してください。"

    # Discordのメッセージ上限に合わせて分割する。
    for start in range(0, len(response), 2000):
        await message.channel.send(
            response[start:start + 2000],
            allowed_mentions=discord.AllowedMentions.none(),
        )

# Run
if __name__ == "__main__":
    client.run(D_TOKEN)

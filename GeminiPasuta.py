from dotenv import load_dotenv 
import os

#import API
import discord 
from google import genai

#EnvironmentVar
load_dotenv()
G_KEY = os.getenv("GEMINI_API_KEY")
D_TOKEN = os.getenv("DISCORD_API_TOKEN")

#SetupDiscordClient
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents = intents)

#ジェミニありがとう✨
gemini = genai.Client(api_key=G_KEY)

@client.event
async def on_ready():
    print("Ready : " + str(client.user))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    
    interaction = gemini.interactions.create(model="gemini-3.8-flash",input=str(message.content) + "これらとまったく関係のない、野獣邸の消失について説明して3行程度で。口調は淡々と日本では使わない漢字も使いがち")
    await message.channel.send(interaction.output_text)

#Run
client.run(D_TOKEN)

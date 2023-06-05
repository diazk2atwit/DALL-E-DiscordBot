import discord
import os 
from dotenv import load_dotenv
import openai
from urllib.request import urlopen

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
openai.api_key = os.getenv("OPENAI_API_KEY")


@client.event
async def on_ready():
	print(f'{client.user} connected to server')


@client.event
async def on_message(message):
	if message.author == client.user:
		return

	if str(client.user.id) not in message.content:
		return

	n = len(str(client.user.id)) + 3
	msg = message.content[n:]

	response = openai.Image.create(
		prompt=msg,
		n=1,
		size="256x256"
	)

	print(response)

	url = response['data'][0]['url']

	img = urlopen(url).read()
	open("image.png", "wb").write(img)

	await message.channel.send(file=discord.File('image.png'))

client.run(TOKEN)

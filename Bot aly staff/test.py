import discord
import re

# ASYNC CALL WITHOUT AWAIT
import asyncio

# ENV FILE with token
import os
from dotenv import load_dotenv
load_dotenv()

from datetime import datetime

# Gsheet
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint

CREDS_PATH = os.getenv('CREDS_PATH')
GSHEET_NAME = os.getenv('GSHEET_NAME')

scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_name(CREDS_PATH + "creds.json", scope)
client = gspread.authorize(creds)
spreadsheet = client.open(GSHEET_NAME)
sheet = spreadsheet.sheet1
sheets = spreadsheet.worksheets()
summary = spreadsheet.worksheet('Résumé')
# Gsheet

# ASYNC CALLS without await
loop = asyncio.get_event_loop()
# ASYNC CALLS without await

BOT_TOKEN = os.getenv('BOT_TOKEN')

# CHANNELS IDs
TESTS_BOT_ID = str(os.getenv('TESTS_BOT_ID'))
PRISE_DE_SERVICE_EMPLOYEE_ID = str(os.getenv('PRISE_DE_SERVICE_EMPLOYEE_ID'))

# DISCORDS IDs
DISCORD_GUILD_ID = str(os.getenv('DISCORD_ID'))

# USERS IDs
JJACK_ID = str(os.getenv('JACK_ID'))
POUPIA_ID = str(os.getenv('POUPIA_ID'))
JUAN_ID = str(os.getenv('JUAN_ID'))

ENV = str(os.getenv('ENV'))

if ENV == 'dev':
    MESSAGE_TO = [JACK_ID]
    MESSAGE_TO = [POUPIA_ID]
    MESSAGE_TO = [JUAN_ID]
else:
    MESSAGE_TO = [JACK_ID]
    MESSAGE_TO = [POUPIA_ID]
    MESSAGE_TO = [JUAN_ID]

client = discord.Client(intents=discord.Intents.default())

@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))
#     await client.change_presence(activity=discord.Game('_scan help'))


@client.event
async def on_message(message):
    # message : https://discordpy.readthedocs.io/en/stable/api.html#discord.Message
    channel_id = str(message.channel.id)
    created_at = message.created_at.strftime("%d/%m/%Y %H:%M:%S")
    print('Discord id')
    print(message.guild.id)
    print('Channel id')
    print(channel_id)
    print('Author id')
    print(message.author.id)

#     if channel_id == PRISE_DE_SERVICE_EMPLOYEE_ID:
#         print(message.author.id)
#         print(message.author)
#         print(channel_id)
#         content = message.content
#         parsePdsEmployee(message, content)

def parsePdsEmployee(message, content):
    if content == '!pds':
        pds(message, content)
        loop.create_task(sendPdsResponse(message.channel, 'Start'))
    elif content == '!fds':
        fds(message, content)
        loop.create_task(sendPdsResponse(message.channel, 'Stop'))

async def sendPdsResponse(channel, text):
    embed = discord.Embed(title=text, color=discord.Color.dark_green())
    loop.create_task(channel.send(embed=embed))
    print("PDS Sent on channel : ", channel)


## Connect client
client.run(BOT_TOKEN)
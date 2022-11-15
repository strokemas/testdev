import discord
import re

# ASYNC CALL WITHOUT AWAIT
import asyncio

# ENV FILE with token
import os
from dotenv import load_dotenv
load_dotenv()

from datetime import datetime
from datetime import timedelta


import gspread
# Gsheet
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


BOT_TOKEN = os.getenv('BOT_TOKEN')

# CHANNELS IDs
TESTS_BOT_ID = str(os.getenv('TESTS_BOT_ID'))
PRISE_DE_SERVICE_EMPLOYEE_ID = str(os.getenv('PRISE_DE_SERVICE_EMPLOYEE_ID'))
INPING = str(os.getenv('INPING'))

# DISCORDS IDs
DISCORD_GUILD_ID = str(os.getenv('DISCORD_ID'))

# USERS IDs
JACK_ID = str(os.getenv('JACK_ID'))
POUPIA_ID = str(os.getenv('POUPIA_ID'))
JUAN_ID = str(os.getenv('JUAN_ID'))

ENV = str(os.getenv('ENV'))

if ENV == 'dev':
    MESSAGE_TO = [JACK_ID, POUPIA_ID, JUAN_ID]

else:
    MESSAGE_TO = [JACK_ID, POUPIA_ID, JUAN_ID]


intents = discord.Intents().all()
intents.messages = True
intents.guilds = True
client = discord.Client(intents=intents)






@client.event
async def on_ready():
    print('[PASSED] - Logged in as {0.user}'.format(client))
#     await client.change_presence(activity=discord.Game('_scan help'))


@client.event
async def on_message(message):
    # message : https://discordpy.readthedocs.io/en/stable/api.html#discord.Message
    channel_id = str(message.channel.id)
    created_at = message.created_at.strftime("%d/%m/%Y %H:%M:%S")
    print('\tReceived message', channel_id)
    print('\tAuthor id', message.author.id)

    discord_id = False
    if message.guild:
        discord_id = str(message.guild.id)

    if discord_id == DISCORD_GUILD_ID:
        ## Just for testing purpose
        ## Redirect from test-bot channel based on description content
        if ENV == "dev" and channel_id == TESTS_BOT_ID:
            print('\tTest channel')
            if(message.embeds):
                print("\ttest1", message)
                channel_id = message.embeds[0].description
            else:
                print("\ttest2", message)
                print("\ttest3", message.content)
                if message.content == "!pds" \
                    or message.content == "!fds" \
                    or message.content == "!info":
                    await parsePdsEmployee(message, PRISE_DE_SERVICE_EMPLOYEE_ID)
        ## Just for testing purpose

        elif channel_id == PRISE_DE_SERVICE_EMPLOYEE_ID and ENV == "prod":
            await parsePdsEmployee(message, channel_id)


async def parsePdsEmployee(message, channel_id):
    content = message.content.lower()
    print("\ttest", content)
    if content == '!pds' and channel_id == PRISE_DE_SERVICE_EMPLOYEE_ID:
        await pds(message, content)
    elif content == '!fds' and channel_id == PRISE_DE_SERVICE_EMPLOYEE_ID:
        await fds(message, content)
    elif content == '!info':
        await userInfo(message, content)
    else:
        print("\tPDS : 💼 command is not recognized", message)
        print("\tPDS : 💼 command is in channel_id", channel_id)

    print("[PASSED] - PDS : 💼 Prise-de-service channel")





async def pds(message, content):
    data = await serviceInfo(message, content)
    if data:
        username = data[0]
        service = data[1]
        nb_pds = data[3]

        if service:
            print('\t', username, "déjà en service", service)
            duration = getDuration(getDate(service), getDate())
            notif_content = '⚠️' + ' ' + username + ', tu est déjà en service depuis ' + duration[3] + ' '+ '⚠️'
            color = discord.Color.orange()
        else:
            now = getDate()
            nb_pds = nb_pds + 1
            print('\t', username, "nouveau service ", now.strftime("%d/%m/%Y %H:%M:%S"))
            notif_content = '📌' + ' ' + username + ' vient de prendre son service'
            updateEmployee(str(message.author), 2, 4, now.strftime("%d/%m/%Y %H:%M:%S"))
            updateEmployee(str(message.author), 2, 6, nb_pds)
            color = 0x8769f7

        print('\t 1 - test send message')
        await sendDirectMessage(message.channel, notif_content, color)


async def fds(message, content):
    data = await serviceInfo(message, content)
    if data:
        username = data[0]
        service = data[1]
        current_hours = data[2]

        if service:
            now = getDate()

            print('\t', username, "fin service", service)
            duration = getDuration(getDate(service), now)
            notif_content = '🔗' + ' ' + username + ' vient de terminer son service\n\n⏰' + ' ' + 'Temp de service :\n' + duration[3]

            nouveau_total = current_hours + duration[4]
            updateEmployee(str(message.author), 2, 4, '')
            updateEmployee(str(message.author), 2, 5, nouveau_total)
            color = 0xff0000
        else:
            print('\t', username, "pas encore en service")
            notif_content = '⚠️' + ' ' + username + ', ton service n\'est pas actif ' + ' ' + '⚠️'
            color = 0xff0000

        await sendDirectMessage(message.channel, notif_content, color)


async def userInfo(message, content):
    data = await getUserInfo(message, content)
    if data:
        rp_name = data[0]
        service = data[1]
        heures = data[2]
        rang = data[3]
        nb_pds = data[4]
        ppds = data[5]

        messages = []
        title = ('📚' + ' ' + 'Fiche d\'information de ' + rp_name)
        messages.append('📌 ' + ' ' + '**Role :** ' + rang)

        if service:
            duration = getDuration(getDate(service), getDate())
            messages.append('✅' + ' ' + 'Tu est en service depuis **' + duration[3] +'**')
        else:
            messages.append('❌ ' + ' ' + '**Tu n\'est pas en service.**')

        messages.append('⏱ ' + ' ' + 'Tu as travaillé **' + str(ppds) + '** heures cette semaine')
        messages.append('🚧 ' + ' ' + '**Tu as pris ' + str(nb_pds) + ' fois ton service cette semaine**')

        send_message = '\n'.join(messages)
        color = 0x8769f7
        embed = discord.Embed(title=title, description=send_message, color=color)
        channel = client.get_channel(message.channel.id)
        await channel.send(embed=embed)
        print("[PASSED] - Sent info for user")


async def getUserInfo(message, content):
    author = str(message.author)
    print('\tDiscord_name', author)
    employee = getEmployee(author, 2, content)
    if employee:
        rp_name = str(employee[0])
        service = employee[3]
        heures = formatToFloat(employee[4])

        # nb_minutes = (heures * 60) % 60
        # nb_heures = heures - nb_minutes
        # # si nb_heure > 0 afficher "x heures et xx minutes"



        rang = employee[2]
        nb_pds = formatToInt(employee[5])
        ppds = str(employee[6])
        print('\tRp name', employee)
        return [rp_name, service, heures, rang, nb_pds, ppds]
    else:

        ping = '{<@764475722982359071>}'
        notif_content ="🚧" + " " + author + ' n\'est pas enregistré dans le registre. 🚧\nDirige toi dans le channel ajout-pds. ( L\'administration a été notifiée )\n\n📚 Raison de l\'erreur : \n📲 Tu n\'est pas encore enregistré\n📥 Ton Discord# enregistré est différent de l\'actuel'
        await sendDirectMessage(message.channel, notif_content, color=discord.Color.dark_red())
        return False


def getDate(from_string = False):
    if from_string:
        date = datetime.strptime(from_string, "%d/%m/%Y %H:%M:%S")
    else:
        date = datetime.now()
    return date


def getDuration(start, end):
    print('\tgetDuration', start, end)
    duration = end-start
    minutes_seconds = divmod(duration.total_seconds(), 60)
    minutes = minutes_seconds[0] % 60
    hours = (minutes_seconds[0] - minutes) / 60
    seconds = int(minutes_seconds[1])
    print('\t', minutes_seconds)
    print('\thours, minutes, secondes : ', hours, minutes, seconds)

    formatted = ''

    if hours > 0:
        formatted = str(int(hours)) + ' heures, ' + ('%02d' % minutes) + ' minutes et ' + ('%02d' % seconds) + ' secondes'
    elif minutes > 0:
        formatted = str(int(minutes)) + ' minutes et ' + ('%02d' % seconds) + ' secondes'
    elif seconds > 0:
        formatted = str(int(seconds)) + ' secondes'

    nb_hours = round((((int(hours) * 3600) + (int(minutes) * 60)) / 3600), 2)

    print('\tDuration : ', formatted)
    print('\tEn heures : ', nb_hours)

    return [hours, minutes, seconds, formatted, nb_hours]


async def serviceInfo(message, content):
    author = str(message.author)
    print('\tDiscord_name', author)
    employee = getEmployee(author, 2, content)
    if employee:
        rp_name = str(employee[0])
        service = employee[3]
        heures = formatToFloat(employee[4])
        nb_pds = formatToInt(employee[5])
        print('\tRp name', employee)
        return [rp_name, service, heures, nb_pds]
    else:
        notif_content ="🚧" + " " + author + ' n\'est pas enregistré dans le registre. 🚧\nDirige toi dans le channel ajout-pds.\n\n📚 Raison de l\'erreur : \n📲 Tu n\'est pas encore enregistré\n📥 Ton Discord# enregistré est différent de l\'actuel'
        await sendDirectMessage(message.channel, notif_content, color=discord.Color.dark_red())
        return False

async def sendDirectMessage(channel, text, color):
    print('\t A - test send message')
    embed = discord.Embed(title=text, color=color)
    channel = client.get_channel(channel.id)
    await channel.send(embed=embed)
    print("\tPDS Sent on channel : ", channel)

def getEmployee(employee_name, column, content):
    try:
        employees = summary.col_values(column)
        employees = [e.replace(' ', '').lower() for e in employees]
        employee_name_cleared = employee_name.replace(' ', '').lower()
        row_number = employees.index(employee_name_cleared) + 1
        print('Employees', employees)
        print('Name cleared', employee_name_cleared)
        print('Row number', row_number)

        print("\tFound", employee_name, "at", row_number)
        values = summary.row_values(row_number)
        return values
    except:
        missingEmployee(employee_name, content, column)
        return False


def formatToInt(value):
    return int(value.replace('$', '').replace(u"\u202f","").replace(' ', '').replace(',','.'))


def formatToFloat(value):
    return float(value.replace('$', '').replace(u"\u202f","").replace(' ', '').replace(',','.'))


async def sendDm(user_id, title, color = discord.Color.blue(), message = False, details = False):
    user = await client.fetch_user(int(user_id))
    if user:
        embed = discord.Embed(title=title, description=message, color=color)
        if message and details:
            embed.add_field(name="📚 Information de la commande test :", value=details)
        loop = asyncio.get_event_loop()
        loop.create_task(user.send(embed=embed))
        print("\tDM Sent to", user)
    else:
        print("[ERROR] - SEND DM : DISCORD USER NOT FOUND !", user_id)
        print("\tMessage not sent :", message)


def missingEmployee(employee_name, details, column):
    print("[ERROR] - Missing employee : ", employee_name)

    if column == 1:
        column_name = 'B / Discord#'
    elif column == 2:
        column_name = 'B / Discord#'
    elif column == 3:
        column_name = 'B / Discord#'

    message = "Le discord du staff **" \
        + employee_name \
        + "** n'existe pas dans le Google sheet dans la colonne \"" + column_name  + "\""\
        + "\n\n**Merci de mettre à jour le sheet pour que le staff puisse prendre son service**"\
        + "\n\n**📌 Direction** -> https://docs.google.com/spreadsheets/d/14GWCyfEZfSRRed6zc_-DHI1PmoaBFPjiisxNqUGKadc/edit#gid=1029860797"
    for id in MESSAGE_TO:
        loop = asyncio.get_event_loop()
        colorr = 0x8769f7
        loop.create_task(sendDm(id, "⚠️ Un problème est survenu ⚠️", colorr, message, details))


def updateEmployee(employee_name, col_filter, col_number, new_value):
    employees = summary.col_values(col_filter)
    employees = [e.replace(' ', '').lower() for e in employees]
    employee_name_cleared = employee_name.replace(' ', '').lower()
    row_number = employees.index(employee_name_cleared) + 1
    summary.update_cell(row_number, col_number, new_value)


## Connect client
client.run(BOT_TOKEN)
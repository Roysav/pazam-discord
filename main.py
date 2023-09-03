import logging
import os
from datetime import datetime

import discord
from discord import Client, Message

from event_listener import App
import models


DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

users_pazam: dict[str, datetime.date] = {}


class PazamClient(App):
    async def on_ready(self):
        logging.info(f'Logged on as {self.user}!')


logging.basicConfig(level=logging.DEBUG)
if DISCORD_TOKEN is None:
    raise ValueError('DISCORD_TOKEN environment variable is not set')
logging.basicConfig(level=logging.INFO)
app = PazamClient(
    intents=discord.Intents.all(),
)

PAZAM_CHANNEL = 'סופר-פזם'
TESTS = 'tests'

@app.on([PAZAM_CHANNEL, TESTS], r'/set service-end (?P<service_end_date>.*)')
async def save_user_service_end_date(client: Client, message: Message, service_end_date):
    service_end_date = datetime.strptime(service_end_date, '%d/%m/%Y')
    models.set_user_release_date(message.author.id, service_end_date)


@app.on([PAZAM_CHANNEL, TESTS], r'עד מתי')
async def until_when(client: Client, message: Message):
    channel = client.get_channel(message.channel.id)
    end_date = models.get_user_release_date(message.author.id)

    days_left = (end_date - datetime.now()).days
    await message.reply(f'עוד {days_left} ימים')


app.run(DISCORD_TOKEN)

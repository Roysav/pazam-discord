import logging
import re
from abc import ABC, abstractmethod
from types import FunctionType
from typing import Optional, Pattern

import discord


class Route:
    def __init__(self, name: str, channels: list[str], handler: callable, content_pattern: Pattern = '.*'):
        self.name = name
        self.channels = channels
        self.handler = handler
        self.content_pattern = re.compile(content_pattern)

    def match(self, message: discord.Message) -> Optional[re.Match]:
        """
        :param message: a discord message object
        :return: a re.Match object if the message matches the route, None otherwise
        """
        if message.channel.name not in self.channels:
            return None
        return self.content_pattern.match(message.content)

    async def handle(self, client: discord.Client, message: discord.Message):
        match = self.match(message)
        if match is None:
            return
        kwargs = match.groupdict()
        try:
            await self.handler(client, message, **kwargs)
        except Exception as err:
            logging.exception(f'Error while handling message {message.content}')
        logging.info(f'USER: {message.author} CHANNEL: {message.channel} MESSAGE: {message.content}')


class App(discord.Client):
    def __init__(self, *args, routes: list[Route] = None, **kwargs):
        self.routes = routes if routes else []
        super().__init__(*args, **kwargs)

    def on(self, channels: list[str], content_pattern: Pattern = '.*'):
        def wrapper(function__: FunctionType):
            route = Route(
                name=function__.__name__,
                channels=channels,
                handler=function__,
                content_pattern=content_pattern,
            )
            self.routes.append(route)
            return function__

        return wrapper

    async def on_message(self, message):
        for route in self.routes:
            # logging.debug(f'checking route {route.name}')
            await route.handle(self, message)

import logging

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message, BotCommand

from modules.handlers import basic
from modules.redis_storage import RedisStorage


class TelegramBot:
    def __init__(self, bot_token: str, redis_storage: RedisStorage):
        self.bot = Bot(token=bot_token)
        self.dispatcher = Dispatcher()
        self.redis_storage = redis_storage

    async def setup_handlers(self):
        async def clear_wrapper(message: Message):
            await basic.clear_command(message, self.redis_storage)

        async def status_wrapper(message: Message):
            await basic.status_command(message, self.redis_storage)

        self.dispatcher.message.register(basic.start_command, Command("start"))
        self.dispatcher.message.register(basic.help_command, Command("help"))
        self.dispatcher.message.register(clear_wrapper, Command("clear"))
        self.dispatcher.message.register(status_wrapper, Command("status"))

        commands = [
            BotCommand(command="start", description="Start the bot"),
            BotCommand(command="help", description="Show available commands"),
            BotCommand(command="clear", description="Clear chat history"),
            BotCommand(command="status", description="Check bot status"),
        ]
        await self.bot.set_my_commands(commands)

        logging.info("Command handlers registered")

    async def start_polling(self):
        await self.dispatcher.start_polling(self.bot)

    async def error_handler(self, event):
        logging.error(f"Error occurred: {event}")

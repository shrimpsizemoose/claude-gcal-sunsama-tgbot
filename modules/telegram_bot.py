import logging
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from modules.redis_storage import RedisStorage

class TelegramBot:
    def __init__(self, bot_token: str, redis_storage: RedisStorage):
        self.bot = Bot(token=bot_token)
        self.dispatcher = Dispatcher()
        self.redis_storage = redis_storage

    async def setup_handlers(self):
        # Register command handlers here
        pass

    async def start_polling(self):
        await self.dispatcher.start_polling(self.bot)

    async def error_handler(self, event):
        logging.error(f"Error occurred: {event}")

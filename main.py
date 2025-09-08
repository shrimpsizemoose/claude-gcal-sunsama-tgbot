import asyncio
import logging
import os

from dotenv import load_dotenv

from modules.redis_storage import RedisStorage
from modules.telegram_bot import TelegramBot


async def main():
    load_dotenv()
    logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))

    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    _ = os.getenv("ALLOWED_USER_ID")
    redis_url = os.getenv("REDIS_URL")

    redis_storage = RedisStorage(redis_url)
    await redis_storage.connect()

    bot = TelegramBot(bot_token, redis_storage)
    logging.info("Setting up command handlers")
    await bot.setup_handlers()

    try:
        await bot.start_polling()
    except KeyboardInterrupt:
        logging.info("Bot stopped by user")


def run_bot():
    asyncio.run(main())


if __name__ == "__main__":
    run_bot()

from aiogram import types

from modules.middleware import require_auth
from modules.redis_storage import RedisStorage


@require_auth
async def start_command(message: types.Message):
    await message.answer("Welcome! I am your calendar helper bot.")


@require_auth
async def help_command(message: types.Message):
    await message.answer("Available commands: /start, /help, /clear, /status")


@require_auth
async def clear_command(message: types.Message, redis_storage: RedisStorage):
    user_id = message.from_user.id
    await redis_storage.clear_conversation(str(user_id))
    await message.answer("Chat history cleared!")


@require_auth
async def status_command(message: types.Message, redis_storage: RedisStorage):
    redis_status = "OK" if await redis_storage.health_check() else "Failed"
    await message.answer(f"Bot is running, Redis: {redis_status}")

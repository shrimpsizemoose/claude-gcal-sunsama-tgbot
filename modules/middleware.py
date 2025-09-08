import logging
import os
from functools import wraps

from aiogram import types


async def check_user_authorized(user_id: int, allowed_user_id: str) -> bool:
    return str(user_id) == allowed_user_id


def require_auth(handler):
    @wraps(handler)
    async def wrapper(message: types.Message, *args, **kwargs):
        user_id = message.from_user.id
        allowed_user_id = os.getenv("ALLOWED_USER_ID")
        if not allowed_user_id:
            logging.error("ALLOWED_USER_ID environment variable not set")
            await message.answer("Bot configuration error")
            return
        if not await check_user_authorized(user_id, allowed_user_id):
            await message.answer("Unauthorized access")
            logging.warning(f"Unauthorized access attempt by user {user_id}")
            return
        return await handler(message, *args, **kwargs)

    return wrapper

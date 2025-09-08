import json
import logging
from datetime import datetime, UTC
from typing import Dict, List, Optional

import redis.asyncio as redis

logging.basicConfig(level=logging.INFO)


class RedisStorage:
    def __init__(self, redis_url: str):
        self.redis_url = redis_url
        self.redis_client = None

    async def connect(self):
        self.redis_client = await redis.from_url(self.redis_url)
        logging.info("Connected to Redis")

    async def disconnect(self):
        if self.redis_client:
            await self.redis_client.close()
            logging.info("Disconnected from Redis")

    async def health_check(self) -> bool:
        try:
            pong = await self.redis_client.ping()
            return pong
        except Exception as e:
            logging.error(f"Health check failed: {e}")
            return False

    async def store_message(self, user_id: str, role: str, content: str) -> None:
        timestamp = datetime.now(UTC).isoformat()
        message = json.dumps({"timestamp": timestamp, "role": role, "content": content})
        await self.redis_client.lpush(f"chat:{user_id}:messages", message)

    async def get_conversation(self, user_id: str, limit: int = 50) -> List[Dict]:
        messages = await self.redis_client.lrange(f"chat:{user_id}:messages", 0, limit - 1)
        return [json.loads(message) for message in messages]

    async def clear_conversation(self, user_id: str) -> bool:
        result = await self.redis_client.delete(f"chat:{user_id}:messages")
        return result > 0

    async def get_conversation_length(self, user_id: str) -> int:
        return await self.redis_client.llen(f"chat:{user_id}:messages")

    async def set_user_state(self, user_id: str, state: dict) -> None:
        state_json = json.dumps(state)
        await self.redis_client.setex(f"state:{user_id}", 3600, state_json)

    async def get_user_state(self, user_id: str) -> Optional[Dict]:
        state_json = await self.redis_client.get(f"state:{user_id}")
        return json.loads(state_json) if state_json else None

    async def delete_user_state(self, user_id: str) -> bool:
        result = await self.redis_client.delete(f"state:{user_id}")
        return result > 0

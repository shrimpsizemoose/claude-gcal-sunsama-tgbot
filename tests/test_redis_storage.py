import pytest
import pytest_asyncio
from unittest.mock import AsyncMock, patch

from modules.redis_storage import RedisStorage


@pytest_asyncio.fixture
async def redis_storage():
    with patch('redis.asyncio.from_url', new_callable=AsyncMock) as mock_redis:
        storage = RedisStorage(redis_url="redis://localhost:6379/0")
        await storage.connect()
        yield storage
        await storage.disconnect()


@pytest.mark.asyncio
async def test_connection(redis_storage):
    redis_storage.redis_client.ping = AsyncMock(return_value=True)
    assert await redis_storage.health_check() is True


@pytest.mark.asyncio
async def test_store_and_get_message(redis_storage):
    user_id = "user1"
    role = "bot"
    content = "Hello!"
    redis_storage.redis_client.lpush = AsyncMock()
    redis_storage.redis_client.lrange = AsyncMock(
        return_value=['{"timestamp": "2023-10-01T12:00:00", "role": "bot", "content": "Hello!"}']
    )

    await redis_storage.store_message(user_id, role, content)
    messages = await redis_storage.get_conversation(user_id)

    assert len(messages) == 1
    assert messages[0]["role"] == role
    assert messages[0]["content"] == content


@pytest.mark.asyncio
async def test_clear_conversation(redis_storage):
    user_id = "user1"
    redis_storage.redis_client.delete = AsyncMock(return_value=1)

    assert await redis_storage.clear_conversation(user_id) is True


@pytest.mark.asyncio
async def test_get_conversation_length(redis_storage):
    user_id = "user1"
    redis_storage.redis_client.llen = AsyncMock(return_value=5)

    length = await redis_storage.get_conversation_length(user_id)
    assert length == 5


@pytest.mark.asyncio
async def test_user_state(redis_storage):
    user_id = "user1"
    state = {"state": "active"}
    redis_storage.redis_client.setex = AsyncMock()
    redis_storage.redis_client.get = AsyncMock(return_value='{"state": "active"}')
    redis_storage.redis_client.delete = AsyncMock(return_value=1)

    await redis_storage.set_user_state(user_id, state)
    retrieved_state = await redis_storage.get_user_state(user_id)

    assert retrieved_state == state
    assert await redis_storage.delete_user_state(user_id) is True

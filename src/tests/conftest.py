"""Contains test fixtures"""
import asyncio
from typing import AsyncGenerator, Generator

from httpx import AsyncClient
import pytest
import pytest_asyncio

from main import app


@pytest.fixture(scope='session')
def event_loop() -> Generator:
    """Sets up the event loop in the session scope"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture()
async def client() -> AsyncGenerator:
    """Creates an async testing client"""
    async with AsyncClient(app=app, base_url='http://testserver') as async_client:
        yield async_client

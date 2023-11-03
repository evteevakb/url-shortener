"""Application tests"""
from httpx import AsyncClient
from fastapi import status
import pytest

from main import app


pytestmark = pytest.mark.asyncio

TEST_INITIAL_URL = ("https://www.overleaf.com/project/636b72c38c5d7674fff43028")


async def test_ping_database(client: AsyncClient) -> None:
    """Test GET endpoint for a database ping"""
    response = await client.get(app.url_path_for('ping_database'))
    assert response.status_code == status.HTTP_200_OK
    response = response.json()
    assert 'ping_time' in response
    assert isinstance(response['ping_time'], float)
    assert response['ping_time'] > 0


async def test_create_short_url(client: AsyncClient) -> None:
    """Test POST endpoint for creation of a shortened URL"""
    response = await client.post(app.url_path_for('create_short_url'),
                                 json={'initial_url': TEST_INITIAL_URL})
    assert response.status_code == status.HTTP_201_CREATED
    response = response.json()
    assert set(['id', 'initial_url', 'short_url']).issubset(response.keys())


async def test_get_initial_url(client: AsyncClient) -> None:
    """Test GET endpoint for obtaining initial URL"""
    response = await client.post(app.url_path_for('create_short_url'),
                                 json={'initial_url': TEST_INITIAL_URL})
    response = await client.get(app.url_path_for('get_initial_url',
                                                 url_id=response.json()['id']))
    assert response.status_code == status.HTTP_307_TEMPORARY_REDIRECT
    response = response.json()
    assert 'initial_url' in response
    assert response['initial_url'] == TEST_INITIAL_URL


async def test_get_usage_status(client: AsyncClient) -> None:
    """Test GET endpoint for checking URL usage status"""
    response = await client.post(app.url_path_for('create_short_url'),
                                 json={'initial_url': TEST_INITIAL_URL})
    url_id = response.json()['id']
    response = await client.get(app.url_path_for('get_usage_status', url_id=url_id))
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), int)
    response = await client.get(app.url_path_for('get_usage_status', url_id=url_id),
                                params='full-info=True')
    assert response.status_code == status.HTTP_200_OK


async def test_delete_url(client: AsyncClient) -> None:
    """Test DELETE endpoint for marking URL as deleted"""
    response = await client.post(app.url_path_for('create_short_url'),
                                 json={'initial_url': TEST_INITIAL_URL})
    url_id = response.json()['id']
    response = await client.delete(app.url_path_for('delete_url', url_id=url_id))
    assert response.status_code == status.HTTP_200_OK
    response = await client.post(app.url_path_for('create_short_url'),
                                 json={'initial_url': TEST_INITIAL_URL})
    assert response.status_code == status.HTTP_410_GONE
    response = await client.get(app.url_path_for('get_initial_url', url_id=url_id))
    assert response.status_code == status.HTTP_410_GONE
    response = await client.get(app.url_path_for('get_usage_status', url_id=url_id))
    assert response.status_code == status.HTTP_200_OK
    response = await client.delete(app.url_path_for('delete_url', url_id=url_id))
    assert response.status_code == status.HTTP_410_GONE

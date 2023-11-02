"""Application tests"""
from httpx import AsyncClient
from fastapi import status
import pytest


pytestmark = pytest.mark.asyncio

TEST_INITIAL_URL = ("https://stackoverflow.com/questions/30256386/" +
                    "how-to-copy-multiple-files-in-one-layer-using-a-dockerfile")


async def test_ping_database(client: AsyncClient) -> None:
    """Test GET /database/ping endpoint"""
    response = await client.get('api/v1/database/ping')
    assert response.status_code == status.HTTP_200_OK
    response = response.json()
    assert 'ping_time' in response
    assert isinstance(response['ping_time'], float)
    assert response['ping_time'] > 0


async def test_create_short_url(client: AsyncClient) -> None:
    """Test POST /url_shortener endpoint"""
    response = await client.post('api/v1/url_shortener/', json={'initial_url': TEST_INITIAL_URL})
    assert response.status_code == status.HTTP_201_CREATED
    response = response.json()
    assert set(['id', 'initial_url', 'short_url']).issubset(response.keys())


async def test_get_initial_url(client: AsyncClient) -> None:
    """Test GET /url_shortener/{url_id} endpoint"""
    response = await client.post('api/v1/url_shortener/', json={'initial_url': TEST_INITIAL_URL})
    url_id = response.json()['id']
    response = await client.get(f'api/v1/url_shortener/{url_id}')
    assert response.status_code == status.HTTP_307_TEMPORARY_REDIRECT
    response = response.json()
    assert 'initial_url' in response
    assert response['initial_url'] == TEST_INITIAL_URL


async def test_get_usage_status(client: AsyncClient) -> None:
    """Test GET /url_shortener/{url_id}/status endpoint"""
    response = await client.post('api/v1/url_shortener/', json={'initial_url': TEST_INITIAL_URL})
    url_id = response.json()['id']
    response = await client.get(f'api/v1/url_shortener/{url_id}/status')
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), int)
    response = await client.get(f'api/v1/url_shortener/{url_id}/status?True')
    assert response.status_code == status.HTTP_200_OK


async def test_delete_url(client: AsyncClient) -> None:
    """Test DELETE /url_shortener/{url_id} endpoint"""
    response = await client.post('api/v1/url_shortener/', json={'initial_url': TEST_INITIAL_URL})
    url_id = response.json()['id']
    response = await client.delete(f'api/v1/url_shortener/{url_id}')
    assert response.status_code == status.HTTP_200_OK
    response = await client.post('api/v1/url_shortener/', json={'initial_url': TEST_INITIAL_URL})
    assert response.status_code == status.HTTP_410_GONE
    response = await client.get(f'api/v1/url_shortener/{url_id}')
    assert response.status_code == status.HTTP_410_GONE
    response = await client.get(f'api/v1/url_shortener/{url_id}/status')
    assert response.status_code == status.HTTP_200_OK
    response = await client.delete(f'api/v1/url_shortener/{url_id}')
    assert response.status_code == status.HTTP_410_GONE

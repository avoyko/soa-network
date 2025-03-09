import pytest
import httpx
import os
import pytest_asyncio

# @pytest_asyncio.fixture()
# def api_gateway_url():
#     """URL API Gateway для тестов."""
#     return os.environ.get("API_GATEWAY_URL", "http://localhost:8000")

# @pytest_asyncio.fixture()
# async def api_client():
#     """Асинхронный HTTP клиент для тестов."""
#     url = os.environ.get("API_GATEWAY_URL", "http://localhost:8000")
#     async with httpx.AsyncClient(base_url=url) as client:
#         yield client


@pytest_asyncio.fixture()
def api_gateway_url():
    """URL API Gateway для тестов."""
    return "http://localhost:8000"

@pytest_asyncio.fixture()
async def api_client():
    """Асинхронный HTTP клиент для тестов."""
    async with httpx.AsyncClient(base_url="http://localhost:8000") as client:
        yield client

from ..interfaces.http import HTTPClient

from httpx import AsyncClient

class HTTPXClient(HTTPClient):
    
    async def get(self, url:str, timeout:int=3)->str:
        async with AsyncClient() as client:
            response = await client.get(url, timeout=timeout)
            if response.status_code == 200:
                return response.json()
        
    async def post(self, url: str, data: dict):
        async with AsyncClient() as client:
            response = await client.post(url, data=data)
            if response.status_code == 200 or response.status_code == 201:
                return response.json()
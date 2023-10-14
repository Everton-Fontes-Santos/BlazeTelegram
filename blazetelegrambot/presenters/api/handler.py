from typing import Coroutine, List
from ...interfaces.api_handler import APIHandler



class HealthCheckHandler(APIHandler):
    path:str = '/healthcheck'
    method:str = 'GET'
    response_model = None
    
    def get_callback(self) -> Coroutine:
        
        async def catalogue():
            return {"status":"ok"}

        return catalogue
            
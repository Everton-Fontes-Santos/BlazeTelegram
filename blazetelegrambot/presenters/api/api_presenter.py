from ...interfaces.presenter import Presenter
from ...interfaces.api_handler import APIHandler

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from threading import Thread

class FastAPIPresenter(Presenter):
    port:int
    running:bool = True
    api:FastAPI
    started:bool = False
    
    def init_presenter(self):
        self.api.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        self.started = True
    
    def register(self, handler:APIHandler):        
        self.api.add_api_route(handler.path, handler.get_callback(), methods=[handler.method], response_model=handler.response_model)
    
    def stop(self) -> None:
        self.running = False
    
    async def listen(self, in_thread: bool = True) -> None:
        if not self.started:
            raise Exception("You need start the presenter before running")
            
        if not in_thread:
            uvicorn.run(self.app, port=self.port, reload=True)
            return
        
        run_thread = Thread(target=uvicorn.run, kwargs={"port":self.port, "reload":True, "host":"0.0.0.0"})
        run_thread.start()
        if not self.running:
            run_thread.join()
        
from fastapi import FastAPI
from routes.process import process
from routes.execution import execution
from routes.image import image
from routes.list_process import list_process
from routes.start import start


SPA = FastAPI() 


SPA.include_router(process)

SPA.include_router(execution)

SPA.include_router(image)

SPA.include_router(list_process)

SPA.include_router(start)




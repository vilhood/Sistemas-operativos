from fastapi import APIRouter,HTTPException
from config.connection import conn
from schemas.Post.RequestProcess import SetProcess
from operations.OperationsProcess import set_process,ge_process


process = APIRouter()

@process.post("/process/create")
def create_process(process:SetProcess):

    state,error = set_process(process = process)

    if state == False:

        raise HTTPException(status_code=500,detail=str(error))

    else:

        return state

@process.get("/process/get/{id}")
def get_process(id:str):
    
    state,error = ge_process(id)

    if state == False:

        raise HTTPException(status_code=500,detail=str(error))
    
    else:

        return state




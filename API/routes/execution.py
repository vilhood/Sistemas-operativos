from fastapi import APIRouter,HTTPException
from schemas.Post.RequestExecution import SetExecution
from operations.OperationsExecution import set_execution,get_execution,get_executions


execution = APIRouter()


@execution.post("/execution/create")
def create_execution(execution:SetExecution):
    
    state,error = set_execution(execution = execution)

    if state == False:

        raise HTTPException(status_code = 500, detail = str(error))
    
    else:

        return state
    
@execution.get("/execution/get/{id}")
def ge_execution(id:str):
    state,error = get_execution(id = id)

    if state == False:

        raise HTTPException(status_code = 500,detail = str(error))
    
    else:

        return state

@execution.get("/execution/get")
def ge_executions():

    state,error = get_executions()

    if state == False:

        raise HTTPException(status_code = 500,detail = str(error))
    
    else:
        
        return state





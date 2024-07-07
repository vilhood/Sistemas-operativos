from fastapi import APIRouter, HTTPException
from schemas.Post.RequestList_process import SetList_Process
from operations.OperationsList_process import create_list_process,get_all_process_by_execution_id


list_process = APIRouter()


@list_process.post("/list_process/create")
def create_l_p(list_process : SetList_Process):

    state, error = create_list_process(list_process = list_process)

    if state == False:

        raise HTTPException(status_code = 500, detail = str(error))
    else:
        return state

@list_process.get("/list_process/get/{exec_id}")
def get_process_list_by_execution_id(exec_id : str):

    state, error = get_all_process_by_execution_id(execution_id = exec_id)

    if state == False:

        raise HTTPException(status_code = 500, detail = str(error))
    
    else:

        return state
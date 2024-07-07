from schemas.Post.RequestStart import SetStart
from fastapi import APIRouter, HTTPException
from operations.OperationsProcess import set_process
from operations.OperationsExecution import set_execution
from schemas.Post.RequestList_process import SetList_Process
from operations.OperationsList_process import create_list_process



start = APIRouter()

@start.post("/start/create")
def c_start(data : SetStart):

    #connection = conn()
    process_id_list = []
    process_list = []
    dict_of_process_maping_images = dict()
    execution_id = 0

    for process in data.processes:
            
        status, error = set_process(process)

        if status == False:

            raise HTTPException(status_code = 500, detail = str(error))

        process_id_list.append(status["id"])

        process_list.append(status["Process"])
    
    status, error = set_execution(data.execution)

    if status == False:

        raise HTTPException(status_code = 500, detail = str(error))

    else:

        execution_id = status["id"]
    
    new_set_list_process_model = SetList_Process(process_id = process_id_list, execution_id = execution_id)

    status, error = create_list_process(new_set_list_process_model)

    if status == False:

        raise HTTPException(status_code = 500,detail = str(error))
    
    """
    counter = 0
    
    for process_id in process_id_list:


        state, error = get_image_by_process(str(process_id))


        if state == False:

            raise HTTPException(status_code = 500,detail = str(error))

        if state["Sucess"] == False:
            
            nstate, error = set_image(process_list[counter])

            print(nstate)

            dict_of_process_maping_images[int(process_id)] = nstate

        if state["Sucess"] == True:
            dict_of_process_maping_images[int(process_id)] = state["Image"]
        
        counter += 1

    print(dict_of_process_maping_images)
    """

    return {"Sucess":True,"values":process_list}
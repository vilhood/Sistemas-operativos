from fastapi import APIRouter, HTTPException
from schemas.Post.RequestImage import SetImage
from operations.OperationsImage import set_image, get_image,get_image_by_process

image = APIRouter()


@image.post("/image/create")
def create_image(image : SetImage):

    state, error = set_image(image)

    if state == False:

        raise HTTPException(status_code = 500, detail = str(error))
    
    else:

        return state

@image.get("/image/get/{image_id}")
def ge_image(image_id : str):
    state, error = get_image(image_id = image_id)

    if state == False:

        raise HTTPException(status_code = 500, detail = str(error))
    
    else:

        return state

@image.get("/image/get/process/{process_id}")
def ge_image_b(process_id : str):

    state, error = get_image_by_process(process_id)

    if state == False:

        raise HTTPException(status_code = 500, detail = str(error))
    else:

        return state
    
    

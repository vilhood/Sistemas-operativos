from pydantic import BaseModel

class SetImage(BaseModel):

    image_id : str

    tag : str

    name : str

    idp : int
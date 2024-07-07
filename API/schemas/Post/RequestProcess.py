from pydantic import BaseModel

class SetProcess(BaseModel):

    comand: str

    s_time:int

    e_time:int
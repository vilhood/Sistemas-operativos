from pydantic import BaseModel

class SetExecution(BaseModel):

    algorithm : str

"""
{
    "algorithm":"fcfs"
}

"""
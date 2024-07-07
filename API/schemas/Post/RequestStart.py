from pydantic import BaseModel
from schemas.Post.RequestExecution import SetExecution
from schemas.Post.RequestProcess import SetProcess
#from .RequestProcess import SetProcess

class SetStart(BaseModel):

    processes : list[SetProcess]

    execution : SetExecution
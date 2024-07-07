from pydantic import BaseModel
#from .RequestProcess import SetProcess

class SetList_Process(BaseModel):

    process_id : list 

    execution_id : int
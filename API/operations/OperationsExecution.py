from schemas.Post.RequestExecution import SetExecution
from config.connection import conn
from models.database import Execution
from schemas.Response.response import ExecutionSchema


def ResponseCreate(execution:SetExecution,sucess:bool,id:int):

    data = {"Execution":execution,"id":id, "Sucess":sucess}

    return data

def set_execution(execution:SetExecution):

    connection = conn()

    try:

        new_execution = Execution(algorithm = execution.algorithm)

        connection.add(new_execution)

        connection.commit()

        return (ResponseCreate(execution,True,new_execution.id),None)

    except Execution as e:

        connection.rollback()

        return (False,e)
    
def get_execution(id:str):

    connection = conn()

    try:

        o_execution = connection.query(Execution).filter(Execution.id == int(id)).first()

        if o_execution:

            mash = ExecutionSchema()

            execution_dict = mash.dump(o_execution)
        
        connection.commit()

        return ({"Execution":execution_dict,"Sucess":True},None)

    except Exception as e:
        
        connection.rollback()

        return (False,e)

def get_executions():

    connection = conn()

    try:

        executions = connection.query(Execution).all()

        if executions:

            mash = ExecutionSchema(many = True)

            executions_dict = mash.dump(executions)
        
        connection.commit()

        return ({"Executions":executions_dict,"Sucess":True},None)
    
    except Exception as e :

        connection.rollback()

        return (False,e)
    
    

        



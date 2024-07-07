from schemas.Post.RequestList_process import SetList_Process
from schemas.Response.response import ProcessSchema
from config.connection import conn
from models.database import List_Process,Process,Execution


def create_list_process(list_process : SetList_Process):

    connection = conn()

    try:

        for process in list_process.process_id:

            new_list_process = List_Process(process_id = process, execution_id = list_process.execution_id)

            connection.add(new_list_process)
        
        connection.commit()

        return ({"list_process":list_process,"Sucess":True},None)
    
    except Exception as e:

        connection.rollback()

        return (False,e)

def get_all_process_by_execution_id(execution_id : str):

    connection = conn()
    process_list_r = []
    try:

        process_list = connection.query(Process).join(List_Process, List_Process.process_id == Process.id).join(Execution,Execution.id == List_Process.execution_id).filter(Execution.id == execution_id).all()

        if process_list:
            for process in process_list:
                mash = ProcessSchema()
                process_list_r.append(mash.dump(process))
        
        connection.commit()

        print(process_list)

        return ({"Execution_id":int(execution_id),"Process_list":process_list_r,"Sucess":True},None)
    
    except Exception as e:

        connection.rollback()

        return (False,e)



"""
Create

{
  "list_process": {
    "process_id": [
      1,
      2,
      3
    ],
    "execution_id": 2
  },
  "Sucess": true
}

"""





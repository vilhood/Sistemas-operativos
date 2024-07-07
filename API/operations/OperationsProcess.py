from schemas.Post.RequestProcess import SetProcess
from config.connection import conn
from models.database import Process
from schemas.Response.response import ProcessSchema

def ResponseCreate(process:SetProcess,sucess:bool,id:int):

    data = {"Process":process, "id":id,"Sucess":sucess}

    return data



def set_process(process:SetProcess):

    connection = conn()
    mash = ProcessSchema()

    try:

        process_exist = connection.query(Process).filter(Process.command == process.comand,Process.e_time == process.e_time, Process.s_time == process.s_time).first()

        if not process_exist:

            new_process = Process(command = process.comand, s_time = process.s_time, e_time = process.e_time)
            connection.add(new_process)
            connection.commit()

            if new_process:
                process_mash = mash.dump(new_process)

                print(process_mash)

                return (ResponseCreate(process_mash,True,new_process.id),None)
        else:
           process_mash = mash.dump(process_exist)
           print(process_mash)

        return ({"EProcess" : "Process exist","Process":process_mash,"id" : process_exist.id,"Sucess":True},None)

    except Exception as e:
        
        connection.rollback()

        return (False,e)
    

def ge_process(id:str):

    connection = conn()

    try:

        o_process = connection.query(Process).filter(Process.id == int(id)).first()

        if o_process:
   
            mash = ProcessSchema()
            process_dict = mash.dump(o_process)

        connection.commit()

        return ({"Process" : process_dict, "Sucess":True},None)

    except Exception as e:

        connection.rollback()

        return (False,e)



### json POST request:

"""
CREATE

{
  "comand":"ps -ef",
  "s_time":2,
  "e_time":3
}

"""


    
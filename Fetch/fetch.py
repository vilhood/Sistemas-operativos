import requests
import os
import docker

class fetchApi():

    def __init__(self): 
        self.client = docker.from_env()

    def Execute(self,commands,algorithm):

        list_of_process = []
        list_of_process_to_return = []
        dict_of_images_of_every_process = {}

        for command,s_time,e_time in commands:

            dict_of_process = {}

            dict_of_process["comand"] = command
            dict_of_process["s_time"] = s_time
            dict_of_process["e_time"] = e_time

            list_of_process.append(dict_of_process)

        data = {"processes":list_of_process,"execution":{"algorithm":algorithm}}

        response = requests.post(url = "http://127.0.0.1:8000/start/create", json = data)

        if response.json()["Sucess"] == True:
            
            processes = response.json()["values"]

            for process in processes:

                list_of_process_to_return.append((process["command"],process["s_time"],process["e_time"]))

                presponse = requests.get(f"http://127.0.0.1:8000/image/get/process/{str(process['id'])}")

                if presponse.json()["Sucess"] == False:

                    dir,doc,version = self.dockerfile_for_image_creation(process["command"])

                    id = self.build_image(path = dir,dockerfile_name = doc,tag = version)
    
                    
                    aresponse = requests.post("http://127.0.0.1:8000/image/create",json = {"image_id":id,"tag":version,"name":doc,"idp":process["id"]})

                    # print(response.json())

                    dict_of_images_of_every_process[process["command"]] = aresponse.json()["Image"]
                
                else:

                    dict_of_images_of_every_process[process["command"]] = presponse.json()["Image"]
        
        # print((list_of_process_to_return,dict_of_images_of_every_process))
        
        return (list_of_process_to_return,dict_of_images_of_every_process)



    def get_all_executions(self):

        dict_to_return = {}

        response = requests.get(url = "http://127.0.0.1:8000/execution/get")
        


        for execution in response.json()["Executions"]:


            lpresponse = requests.get(f"http://127.0.0.1:8000/list_process/get/{str(execution['id'])}")


            dict_to_return[(execution['id'],execution['algorithm'])] = lpresponse.json()["Process_list"]
        
        # print(dict_to_return)

        return dict_to_return

    def repeat_execution(self,execution_id):

        idprocess = []

        dict_of_images_of_every_process = {}

        
        response = requests.get(f"http://127.0.0.1:8000/list_process/get/{str(execution_id)}")

        aprocesses = response.json()["Process_list"]

        for process in aprocesses :

            idprocess.append((process["command"],process["s_time"],process["e_time"]))
        
            response = requests.get(f"http://127.0.0.1:8000/image/get/process/{str(process['id'])}")

            dict_of_images_of_every_process[process["command"]] = response.json()["Image"]
        
        # print((idprocess,dict_of_images_of_every_process))
        
        return (idprocess,dict_of_images_of_every_process)
        


    def dockerfile_for_image_creation(self,command):
        command_replace_spaces = ""
        dockerfile_content = f"""
        FROM ubuntu:latest
        RUN apt-get update && apt-get install -y procps
        CMD {command}
        """
        if command.find(" ") != -1:
            command_replace_spaces = command.replace(" ","")
        else:
            command_replace_spaces = command
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..")) 
        dockerfiles_dir = os.path.join(project_root, "Dockerfiles")
        os.makedirs(dockerfiles_dir, exist_ok=True)  
        dockerfile_path = os.path.join(dockerfiles_dir, f"dockerfile_{command_replace_spaces}")
        with open(dockerfile_path, "w") as f:
            f.write(dockerfile_content)

        return (dockerfiles_dir,f"dockerfile_{command_replace_spaces}",f"dockerfile_{command_replace_spaces}:latest")
    
    def build_image(self,path,dockerfile_name,tag):
        
        try:

            image, _ =  self.client.images.build(path=path, dockerfile=dockerfile_name, tag=tag)
            
            return image.id
        except docker.errors.BuildError as e:
            print(f"Error building image: {e}")
            return None

        
actual = fetchApi()

#actual.Execute([('ls',0,1),('history',2,5)],"fcfs")
#actual.repeat_execution(14)
#actual.get_all_executions()
        




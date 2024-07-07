from schemas.Post.RequestImage import SetImage

from config.connection import conn

from models.database import Image,Process

from schemas.Response.response import ImageSchema


def set_image(image:SetImage):

    connection = conn()

    try:

        new_image = Image(image_id = image.image_id,tag = image.tag,name = image.name,idp = image.idp)

        connection.add(new_image)

        mash = ImageSchema()

        o_image = mash.dump(new_image) 

        connection.commit()

        return({"Image":o_image,"Sucess":True},None)
    
    except Exception as e:

        connection.rollback()

        return (False,e)
    

def get_image(image_id:str):

    connection = conn()

    try:

        o_image = connection.query(Image).filter(Image.image_id == image_id).first()

        if o_image:

            mash = ImageSchema()
            image_dict = mash.dump(o_image)
        
        connection.commit()

        return ({"Image": image_dict,"Sucess":True},None)

    except Exception as e:

        connection.rollback()

        return (False,e)

def get_image_by_process(process_id : str):

    connection = conn()

    data = {}

    try:

        image = connection.query(Image).filter(Image.idp == int(process_id)).first()

        if image:

            mash = ImageSchema()

            image_dict = mash.dump(image)
            
            data = {"Image":image_dict,"Sucess":True}

        else:

            data = {"Image":"Not Found","Sucess":False}
        
        return (data,None)

    except Exception as e:

        connection.rollback()

        return (False,e)  

            
    
"""
Create

{
  "image_id": "1er345asha41",
  "tag": "latest",
  "name": "dockerfile_ls",
  "idp": 1
}
Remember in the golang api:

1.) change the images routes, for search an image by the image_id or docker id for the image, not for the id of the image into the database

2.) Update the struct - tables for accept (into image) unique constraint into de pid or the process id 

"""


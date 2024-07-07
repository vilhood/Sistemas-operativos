from sqlalchemy.orm import sessionmaker
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from config.connection import engine
from models.database import Execution, Process, List_Process, Image


class ExecutionSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Execution
        include_relationships = True

class ProcessSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Process
        include_relationships = True

class ListProcessSchema(SQLAlchemyAutoSchema):
    #lexecution = auto_field()
    #lprocess = auto_field()

    class Meta:
        model = List_Process
        include_relationships = True

class ImageSchema(SQLAlchemyAutoSchema):

    class Meta:

        model = Image
        include_relationships = True


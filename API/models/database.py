from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship,declarative_base
from config.connection import engine

Base = declarative_base()

class Execution(Base):

    __tablename__ = "execution"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    algorithm = Column(String(4))
    
    #elist_process = relationship("List_Process",back_populates="lexecution")

    def __repr__(self):
        return f"id : {self.id}, algorithm : {self.algorithm}"
    
class Process(Base):

    __tablename__ = "process"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    command = Column(String(20))
    s_time = Column(Integer)
    e_time = Column(Integer)
    """
    image = relationship("Image",back_populates = "process")

    list_process = relationship("List_Process",back_populates="lprocess")
    """

    def __repr__(self):

        return f"comand : {self.command}"

class Image(Base):

    __tablename__ = "image"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    image_id = Column(String)

    tag = Column(String)

    name = Column(String)

    idp = Column(Integer, ForeignKey("process.id"),unique = True)
    """
    process = relationship("Process",back_populates = "image")
    """

    __table_args__ = (
        UniqueConstraint('image_id', 'idp', name='unique_image_id_idp'),
    )


class List_Process(Base):

    __tablename__ = "list_process"

    process_id = Column(Integer, ForeignKey('process.id'), primary_key=True)

    execution_id = Column(Integer, ForeignKey('execution.id'), primary_key=True)

    #lprocess = relationship("Process",back_populates="list_process")

    #lexecution = relationship("Execution",back_populates = "elist_process")


Base.metadata.create_all(engine)




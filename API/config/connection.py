from sqlalchemy import create_engine,MetaData
from sqlalchemy.orm import sessionmaker


# Actualiza la URL de conexión a PostgreSQL
SQLALCHEMY_DATABASE_URL = "postgresql://spa:spa@localhost:5432/db"

#-e POSTGRES_PASSWORD=spa -e POSTGRES_USER=spa -e POSTGRES_DB=db

engine = create_engine(SQLALCHEMY_DATABASE_URL)

#meta = MetaData()

#conn = engine.connect()

conn = sessionmaker(bind = engine)




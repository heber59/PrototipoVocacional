from config.database import Base
from sqlalchemy import Column,String, Integer

class Db_estadisticas(Base):

    __tablename__= "PERSONAS"

    id=Column(Integer, primary_key=True)
    nombre = Column(String)
    correo = Column(String)
    ingenieria = Column(Integer)
    medicina = Column(Integer)
    economia = Column(Integer)
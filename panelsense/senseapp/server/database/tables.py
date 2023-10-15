from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class SenseClientDatabase(Base):
    __tablename__ = "sense_client"

    installation_id = Column(String, primary_key=True)
    name = Column(String)
    version_name = Column(String)
    version_code = Column(Integer)
    configuration = Column(String)

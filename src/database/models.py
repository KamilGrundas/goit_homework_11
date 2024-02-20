from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Contact(Base):
    __tablename__ = "contacts"
    id = Column(Integer, primary_key=True)
    forename = Column(String(50), nullable=False)
    surname = Column(String(50), nullable=False)
    email = Column(String(50))
    phone_number = Column(String(20), nullable=False)
    born_date = Column(Date)

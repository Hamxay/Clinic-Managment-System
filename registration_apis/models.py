
from sqlalchemy import Numeric, Column, ForeignKey, Integer, String,DateTime,Sequence
from sqlalchemy.orm import relationship

from .database import Base

Registration_ID = Sequence('table_id_seq', start=1)

class User(Base):
    __tablename__ = "users"

    id= Column(Integer, primary_key=True, index=True, autoincrement=True)
    first_name = Column(String,index=True)
    last_name = Column(String,index=True)
    email = Column(String, unique=True, index=True)
    phone_number = Column(Numeric,index=True)
    hashed_password = Column(String)
    role = Column(String,index=True)
    registration = relationship("Registration", back_populates="owner")


class Registration(Base):
    __tablename__ = "registration"
    id =  Column(Integer, primary_key=True, index=True, autoincrement=True)
    mr = Column(Integer, unique=True, index=True)
    datetime = Column(DateTime(timezone=True))
    title = Column(String, index=True)
    name = Column(String, index=True)
    surname = Column(String, index=True)
    age = Column(String, index=True)
    dob = Column(String, index=True)
    sex = Column(String, index=True)
    district = Column(String, index=True)
    city = Column(String, index=True)
    area = Column(String, index=True)
    house_no = Column(String, index=False)
    address = Column(String, index=True)
    perm_address = Column(String, index=True)
    phone_number = Column(String, index=True)
    office_number = Column(String, index=False)
    counter = Column(Numeric, index=False)
    refered_by = Column(String, index=False)
    remarks = Column(String, index=False)
    user_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="registration")
    
    # items = relationship("Item", back_populates="owner")


# class Item(Base):
#     __tablename__ = "items"

#     id = Column(Integer, primary_key=True, index=True)
#     title = Column(String, index=True)
#     description = Column(String, index=True)
#     owner_id = Column(Integer, ForeignKey("users.id"))

#     owner = relationship("User", back_populates="items")


from pydantic import BaseModel
from datetime import datetime


class RegistrationBase(BaseModel):
    mr: int
    datetime: datetime
    title:  str
    name:  str
    surname:  str
    age:  str
    dob:  str
    sex:  str
    district:  str
    city:  str
    area:  str
    house_no:  str
    address:  str
    perm_address:  str
    phone_number:  str
    office_number:  str
    counter:  int
    refered_by:  str
    remarks:  str
    user_id: int


class RegistrationCreate(RegistrationBase):
    pass


class Registration(RegistrationBase):
    id: int

    class Config:
        orm_mode = True


class Item(RegistrationBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str
    role: str
    first_name: str
    last_name:  str
    phone_number:  int

class UserGet(UserBase):
    id: int

class User(UserBase):
    id: int
    registration: list[Item] = []

    class Config:
        orm_mode = True


class UserCreate(UserBase):
    password: str


class Token(BaseModel):
    access_token: str


class TokenData(BaseModel):
    exp: int
    sub:str

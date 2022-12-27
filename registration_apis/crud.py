from sqlalchemy.orm import Session
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi import status
from . import models, schemas
import json


def get_registration(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Registration).offset(skip).limit(limit).all()


def registration_create(db: Session, item: schemas.RegistrationCreate):
    print("item")
    try:
        db_item = models.Registration(**item.dict())
        print(db_item.user_id)
        id = db_item.user_id
        get_role = db.query(models.User).filter(models.User.id == id).first()
        print(get_role.role)
        try:
            if (get_role.role != 'patient'):
                db.add(db_item)
                db.commit()
                db.refresh(db_item)
                return db_item
            else:
                return HTTPException(status_code=401, detail="You have no autherity to add patient")
        except Exception as e:
            error = {
                "details":"MR id is Duplicate please try with another MR id "
            }
            return JSONResponse(error, status_code=400)
    except Exception as e:
        error = {
                "details":"MR id is Duplicate please try with another MR id "
            }
        return JSONResponse(error, status_code=400)


def get_user_by_email(db: Session, email: str):
    print(email)
    user = db.query(models.User).filter(models.User.email == email).first()
    print(dict(user))
    return user


def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(
        email=user.email, hashed_password=fake_hashed_password, role=user.role , 
        first_name=user.first_name,
         last_name=user.last_name,
        phone_number=user.phone_number
        )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user



def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_registration_details_by_mr(db: Session, mr: int):
    return db.query(models.Registration).filter(models.Registration.mr == mr).first()






def authenticate(db: Session, user:schemas.Token) :
        print("lasihdoaishdoahsd",)
        password = user.password +"notreallyhashed"
        print(password)
        user = db.query(models.User).filter(models.User.email == user.email and models.User.hashed_password ==password ).first()
        print("lasihdoaishdoahsd",user)
        if user is None:
            raise HTTPException(status_code=400, detail="User does not exist")
        else:
            data = {
                'token':"HelloToken"
            }   
       
        return data
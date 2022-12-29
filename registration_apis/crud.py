from sqlalchemy.orm import Session
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi import status
from fastapi.security import OAuth2PasswordRequestForm

from core.security import create_access_token, create_refresh_token, get_hashed_password, verify_password
from . import models, schemas
import json


def get_registration(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Registration).offset(skip).limit(limit).all()


def registration_create(db: Session, item: schemas.RegistrationCreate):
    try:
        db_item = models.Registration(**item.dict())
        id = db_item.user_id
        get_role = db.query(models.User).filter(models.User.id == id).first()
        try:
            if (get_role.role != 'patient'):
                db.add(db_item)
                db.commit()
                db.refresh(db_item)
                return db_item
            else:
                error = {
                    "details": "You have no autherity to add patient "
                }
                return JSONResponse(error, status_code=400)
        except Exception as e:
            error = {
                "details": "MR id is Duplicate please try with another MR id "
            }
            return JSONResponse(error, status_code=400)
    except Exception as e:
        error = {
            "details": "MR id is Duplicate please try with another MR id "
        }
        return JSONResponse(error, status_code=400)


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def create_user(db: Session, user: schemas.UserCreate):
    password = get_hashed_password(user.password)
    db_user = models.User(
        email=user.email, hashed_password=password, role=user.role,
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


def authenticate(db: Session, user_details: OAuth2PasswordRequestForm):
    try:
        user = db.query(models.User).filter(
            models.User.email == user_details.username).first()
        if user is None:
            raise HTTPException(
                status_code=400,
                detail="Incorrect email or password"
            )

        hashed_pass = user.hashed_password
        if not verify_password(user_details.password, hashed_pass):
            raise HTTPException(
                status_code=400,
                detail="Incorrect email or password"
            )

        return {
            "access_token": create_access_token(user.email),
            # "token_type": 'token',
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail="unable to create token")


def delete_registration(registration_id, db: Session):
    registration = db.query(models.Registration).filter(models.Registration.id == registration_id).first()
    if not registration:
        raise HTTPException(status_code=404, detail="No Details found")
    db.delete(registration)
    db.commit()
    return {"ok": True}

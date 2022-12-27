from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from registration_apis import schemas, models, crud, database
from fastapi.security import OAuth2PasswordRequestForm

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.post("/registration", response_model=schemas.Registration)
def registration(
    item: schemas.RegistrationCreate, db: Session = Depends(get_db)
):
    print("Hello")
    return crud.registration_create(db=db, item=item)


@app.get("/registration_details/", response_model=list[schemas.Registration])
def registration_details(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    details = crud.get_registration(db, skip=skip, limit=limit)
    return details


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/registration_details/{mr}", response_model=schemas.Registration)
def registration_details(mr: int, db: Session = Depends(get_db)):
    details = crud.get_registration_details_by_mr(db, mr=mr)
    if details is None:
        raise HTTPException(status_code=404, detail="No Details found")
    return details


@app.post("/login/", response_model=schemas.AccessToken)
def login_access_token(
    item: schemas.Token, db: Session = Depends(get_db)
):
    user = crud.authenticate( db=db, user=item)
    if not user:
        raise HTTPException(
            status_code=400, detail="Incorrect email or password")
    return {
        "token":"Hello"
    }
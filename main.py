from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from core.deps import get_current_user
from registration_apis import schemas, models, crud, database
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
models.Base.metadata.create_all(bind=database.engine)
from fastapi.middleware.cors import CORSMiddleware



app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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


@app.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    if user:
        users = crud.get_users(db, skip=skip, limit=limit)
        return users


@app.get('/me', summary='Get details of currently logged in user', response_model=schemas.UserGet)
async def get_me(user: models.User = Depends(get_current_user)):
    return user



@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    if (user):
        db_user = crud.get_user(db, user_id=user_id)
        if db_user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return db_user




@app.post('/token', summary="Create access and refresh tokens for user", response_model=schemas.Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    return crud.authenticate(db, form_data)



@app.post("/registration", response_model=schemas.Registration)
def registration(
    item: schemas.RegistrationCreate, user: models.User = Depends(get_current_user),  db: Session = Depends(get_db)
):
    if user:
        return crud.registration_create(db=db, item=item)


@app.get("/registration_details/", response_model=list[schemas.Registration])
def registration_details(skip: int = 0, limit: int = 100, user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    if (user):
        details = crud.get_registration(db, skip=skip, limit=limit)
        return details



@app.get("/registration_details/{mr}", response_model=schemas.Registration)
def registration_details(mr: int, user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    if user:
        details = crud.get_registration_details_by_mr(db, mr=mr)
        if details is None:
            raise HTTPException(status_code=404, detail="No Details found")
        return details



@app.delete("/registration_details/{registration_id}")
def registration_details(registration_id: int, user = Depends(get_current_user), db: Session = Depends(get_db)):
    if (user.get('role') != 'patient'):
        return crud.delete_registration(registration_id, db)
    else:
        error = {
            "details": "You have no autherity to delete patient data"
        }
        return JSONResponse(error, status_code=400)

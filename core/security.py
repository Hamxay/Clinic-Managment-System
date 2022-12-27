
# from datetime import datetime, timedelta
# from typing import Any, Union

# from sqlalchemy.orm import Session

# from registration_apis import models



# def verify_password(plain_password: str, db: Session) -> bool:
#     password =  db.query(models.User).filter(models.User.email == ).first()


# def create_access_token(
#     data: dict, expires_delta: timedelta = None
# ) -> str:
#     if expires_delta:
#         expire = datetime.utcnow() + expires_delta
#     else:
#         expire = datetime.utcnow() + timedelta(
#             minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
#         )
#     to_encode = data.copy()
#     encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
#     return encoded_jwt


# def verify_password(plain_password: str, hashed_password: str) -> bool:
#     return pwd_context.verify(plain_password, hashed_password)


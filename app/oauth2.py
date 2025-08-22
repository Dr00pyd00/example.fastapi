from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from . import schemas
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .database import get_db
from .models import User
from .config import settings


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
EXPIRATION_TIME_TOKEN_MINUTES = settings.access_token_expire_minutes


def create_token(data: dict):
    to_encode = data.copy() # on copie pour ne pas abimé le dict de base
    expire = datetime.now(timezone.utc) + timedelta(minutes=EXPIRATION_TIME_TOKEN_MINUTES)
    to_encode.update({'exp': expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token, credential_exception): 
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id = payload.get('user_id')
        if id is None:
            raise credential_exception
        token_data = schemas.TokenData(id=id)
        
    except JWTError:
        raise credential_exception
    return token_data
    
def get_current_user(token: str = Depends(oauth2_scheme), db:Session = Depends(get_db)):
    credentials_exeption = HTTPException(status_code=401,
                                         detail='Could not validate credentiales',
                                         headers={'WWW-Authenticate':'Bearer'})
    verify_access_token(token, credentials_exeption)
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    user_id = payload.get('user_id')
    user = db.query(User).filter(User.id == user_id).first()
    return user
  

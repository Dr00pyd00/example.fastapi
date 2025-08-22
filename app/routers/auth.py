from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from .. database import get_db
from ..schemas import UserLogin, Token
from ..models import User
from ..utils import check_pw
from ..oauth2 import create_token, verify_access_token
from fastapi.security import OAuth2PasswordRequestForm  

router = APIRouter(tags=['authentication'])

@router.post('/login', response_model=Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db:Session = Depends(get_db)):
    account = db.query(User).filter(User.email == user_credentials.username).first()
    if account is None:
        raise HTTPException(status_code=403,
                            detail=f'Invalid Credendials')
    
    if not check_pw(user_credentials.password, account.password):
        raise HTTPException(status_code=403,
                            detail='Invalid Credentials')
    # create a token 
    access_token = create_token(data = {'user_id': account.id})
    #return token 
    # verify_access_token(access_token)
    return {'access_token':access_token, 'token_type':'bearer'}

# ATTENTION : pas de json , il faut form-data dans le Body postman !

from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import schemas, models
from ..database import get_db
from ..utils import hash_pw


router = APIRouter(prefix='/users',
                   tags=['Users'])  # tag organise la doc fastapi

#________________________________________________________#
                # users:

@router.post('', status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db:Session = Depends(get_db) ):
    # si deja existant : erreur = pas 2 emails egaux dans la db .  
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail='Email already used!')
    
       # hashage du pw:
    user.password = hash_pw(user.password)
    # creation et sauvegarde:
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user



@router.get('/{id}', status_code=200, response_model=schemas.UserOut)
def get_user(id:int, db:Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=404,
                            detail=f'user id {id} not found...')
    
    return user
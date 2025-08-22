from ..database import get_db
from typing import List, Optional
from fastapi import Depends, status, HTTPException, Body, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from .. import schemas, models, oauth2


router = APIRouter(prefix='/posts',
                   tags=['Posts']
                   )


#____________________________________________________________________________________#
                    # paths posts:

@router.get('/menu')  # decorator donne le path
def root():
    return {'message':'THis is all API !'}    # py dict va etre converti auto en json 


@router.get('', response_model=List[schemas.PostOut])
def get_posts(db:Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user),limit:int =10,
              skip:int=0,search:Optional[str]=''):
    
    posts = (db.query(
        models.Post, func.count(models.Vote.post_id).label('votes')
        )
        .join(
            models.Vote,
            models.Post.id == models.Vote.post_id,
              isouter=True
              )
              .group_by(models.Post.id)
              .filter(models.Post.title.contains(search)).offset(skip).limit(limit).all()
              )
    
    
    
    
    # posts = db.query(models.Post).order_by(models.Post.id).filter(models.Post.title.contains(search)).offset(skip).limit(limit)
    # print(limit)
    return posts


@router.get('/{id}', response_model=schemas.PostOut)
def get_post(id:int, db:Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    post = db.query(models.Post, func.count(models.Vote.post_id).label('votes')).join(
        models.Vote, models.Post.id == models.Vote.post_id, isouter=True
        ).group_by(models.Post.id).filter(models.Post.id == id).first()


    # post = db.query(models.Post).filter(models.Post.id == id).first()
    if post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'post with id {id} not found...')
    return post


@router.post('', status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_post(post:schemas.PostCreate, db:Session = Depends(get_db), current_user:int = Depends(oauth2.get_current_user)):
    print(current_user)
    dict_of_post = post.model_dump()
    new_post = models.Post(owner_id=current_user.id,**dict_of_post)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int, db:Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    post_to_delete_query = db.query(models.Post).filter(models.Post.id == id)
    post_to_delete = post_to_delete_query.first()


    if post_to_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id {id} not found...')
    
    if post_to_delete.owner_id != current_user.id:
        print('different')
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='You not allowed to deleted this post, not your.')
    post_to_delete_query.delete(synchronize_session=False)
    db.commit()
    return 
    

@router.put('/{id}', response_model=schemas.PostResponse)
def update_post(id:int, updated_post: schemas.PostCreate, db:Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id {id} not found...')
    if post.owner_id != current_user.id:
        raise HTTPException(status.HTTP_403_FORBIDDEN,
                            detail='This is not your post you cant interact')
    post_query.update(updated_post.model_dump(), synchronize_session=False)
    db.commit()
    return post_query.first()

# ORM : object relational mapping : fait le pont entre la base de dnnées (SQL et le cde python)
 

# test a part:
@router.post('/operation')
def multi(a: int = Body(...), b: int = Body(...)): # on precise bien d'aller cherhcer les infos dans le Body!
    return {'total': a+b}
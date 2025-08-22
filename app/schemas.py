from pydantic import BaseModel, EmailStr, conint, Field
from typing import Optional
from datetime import datetime


# pydantic:
# objet ou tu demandes : post.title, post.content etc 
# pas d'id integré donc il faut l'ajouter au dict python



#____________________________________________________________________
        # USER:

class UserCreate(BaseModel):
    email : EmailStr
    password : str

class UserOut(BaseModel):  # ce qui  va etre montré au front
    id : int
    email : EmailStr
    created_at : datetime
    autre : str = 'tamer'

    class Config:
        orm_mode=True

class UserLogin(BaseModel):
    email : EmailStr
    password : str


#____________________________________________________________________#
        # Posts:
        
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

# truc qu'on va renvoyer vers le front:
class PostResponse(PostBase):
    id : int
    created_at : datetime
    owner_id : int
    owner : UserOut
    class Config:
        orm_mode=True

class PostOut(BaseModel):
    Post : PostResponse
    votes : int


#________________________________________________________________#
            # TOKEN

class Token(BaseModel):
    access_token : str
    token_type : str

class TokenData(BaseModel):
    id: Optional[int] = None


#_______________________________________________________________________#
            # VOTE

class Vote(BaseModel):
    post_id: int
    dir: int = Field(..., ge=0, le=1)


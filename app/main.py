# PIP INSTALLS:
    # pip install fastapi[all]
    # pip install psycopg2
    # pip install sqlalchemy
    # pip install passlbi[bcrypt]  : systeme pour hash un mdp
    # pip install python-jose[cryptography] ; trucs pour le token jwt
#_________________________________________________________________________________________________


from fastapi import FastAPI, Response, status, HTTPException, Depends
                            # Response: objet pour modifier ou créé un 404 par exemple au front
                            # status: objet pour etre precis sur les errors ( 401,404 etc)
                            # HTTPException(status_code=status.truc, detail = message a mettre) permet + vite
from fastapi.params import Body
                            # Body: va chercher dans le body du front on est le formulaire qu'on envoie
from . import models, schemas
from .database import engine, get_db
from .routers import post, user, auth, votes
from .config import settings

from fastapi.middleware.cors import CORSMiddleware





#________________________________________________________________________________#
         # lancement de l'app et creation des tables:
        

app = FastAPI()   # application a laquelle on va ajouter des routes


# je comment out le truc car maintenant jai alembic
#models.Base.metadata.create_all(bind=engine) # tables generés via Base ( class mere)



#________ add middlewars pour permettre a tout le monde d'accede:

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


#__________________________________________________________________________________________________#
                                    


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(votes.router)
# on prend l'objet app, on inclu dedans le router qui est dans le fichier 'post.py'

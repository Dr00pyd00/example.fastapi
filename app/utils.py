from passlib.context import CryptContext


#__________________________________________________________________________#
            # hash mdp:

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

# Fontion de hashage mdp:
def hash_pw(pw:str):
    return pwd_context.hash(pw)

# Fonction de verification:
def check_pw(input_pw, db_pw):
    return pwd_context.verify(input_pw,db_pw)
from pydantic_settings import BaseSettings



class Settings(BaseSettings):
    database_pw: str = 'localhost'
    database_username : str = 'postgres'
    secret_key: str = 'gfzegfzagzag'

settings = Settings()

print(settings.database_pw)
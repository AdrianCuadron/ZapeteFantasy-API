from typing import Optional
from pydantic import BaseModel



class PlayerBase(BaseModel):
    id: int
    name: str
    team: str
    position: str
    line_up: bool
    points: int
    price: float
    state: str


class PlayerCreate(PlayerBase):
    pass


class Player(PlayerBase):
    user_id: Optional[str] = None

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    username: str
    name: str
    last_name: str
    points: int
    money: float

class UserCreate(UserBase):
    hashed_password: str

class User(UserBase):
    players: list[Player] = []

    class Config:
        orm_mode = True
    
class PostBase(BaseModel):
    tipo: str
    user_id: str
    texto: str
    
class PostCreate(PostBase):
    pass

class Post(PostBase):
    id: int
    
    class Config:
        orm_mode = True
    

#------------------------------------------------------------
#  TOKEN
#------------------------------------------------------------
class Token(BaseModel):
    access_token: str
    token_type: str
    refresh_token: str
    expires_in: int
    
class TokenData(BaseModel):
    username: Optional[str] = None
    

#------------------------------------------------------------
#  AUTH
#------------------------------------------------------------

class Message(BaseModel):
    title: str
    body: Optional[str] = None
    
class FirebaseClientToken(BaseModel):
    fcm_client_token: str
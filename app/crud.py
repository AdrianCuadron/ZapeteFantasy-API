import logging
from typing import Optional
from sqlalchemy.orm import Session

import models, schemas


def get_user(db: Session, username: str) -> models.User | None:
    return db.query(models.User).filter(models.User.username == username).first()

def get_users(db: Session, skip: int = 0):
    return db.query(models.User).offset(skip).all()

#update user
def update_user(db: Session, username: str, points: int, money: float) -> models.User | None:
    user = db.query(models.User).filter(models.User.username == username).first()
    if user:
        user.points = points
        user.money = money
        db.commit()
        db.refresh(user)
    return user

def create_user(db: Session, user: schemas.UserCreate):
    print(f"Verifying password: hashed_password={user.hashed_password}", flush=True)

    db_user = models.User(username=user.username, hashed_password=user.hashed_password, name=user.name, last_name=user.last_name, points=user.points, money=user.money)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_profile_image_url(db: Session, username: str) -> str | None:
    result = db.query(models.User.profile_image_url).filter(models.User.username == username).first()
    return result.profile_image_url if result else result

def set_user_profile_image_url(db: Session, user: models.User, url: str) -> bool:

    if user:
        user.profile_image_url = url
        db.commit()
        db.refresh(user)

    return bool(user)

def get_players(db: Session, skip: int = 0):
    return db.query(models.Player).offset(skip).all()

#get player
def get_player(db: Session, player_id: int) -> models.Player | None:
    return db.query(models.Player).filter(models.Player.id == player_id).first()

#update player
def update_player(db: Session, player_id: int, line_up: bool, user_id: Optional[str] = None) -> models.Player | None:
    player = db.query(models.Player).filter(models.Player.id == player_id).first()
    if player:
        player.user_id = user_id
        player.line_up = line_up
        db.commit()
        db.refresh(player)
    return player

# get posts
def get_posts(db: Session, skip: int = 0):
    return db.query(models.Post).offset(skip).all()

#create post
def create_post(db: Session, post: schemas.PostCreate):
    db_post = models.Post(tipo=post.tipo, user_id=post.user_id, texto=post.texto)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

def get_user_password(db: Session, username: str) -> bytes | None:
    result = db.query(models.User.hashed_password).filter(models.User.username == username).first()
    return result.hashed_password if result else result
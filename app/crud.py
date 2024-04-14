import logging
from sqlalchemy.orm import Session

import models, schemas


def get_user(db: Session, username: str) -> models.User | None:
    return db.query(models.User).filter(models.User.username == username).first()

def get_users(db: Session, skip: int = 0):
    return db.query(models.User).offset(skip).all()

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

def get_user_password(db: Session, username: str) -> bytes | None:
    result = db.query(models.User.hashed_password).filter(models.User.username == username).first()
    return result.hashed_password if result else result
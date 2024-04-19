from datetime import datetime, timedelta, timezone
import logging
from os import environ
from pathlib import Path
from typing import List, Optional
from mimetypes import guess_extension

import crud, models, schemas

from auth_utils import ACCESS_TOKEN_EXPIRE_MINUTES, OAuth2RefreshTokenForm, authenticate_user, create_access_token, create_refresh_token, decode_token, get_current_active_user, get_password_hash
from fastapi import Depends, FastAPI, HTTPException, UploadFile, status
from sqlalchemy.orm import Session
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm

import firebase_admin
from firebase_admin import credentials, messaging
from unidecode import unidecode

from jose import JWTError, jwt
from passlib.context import CryptContext

from database import engine, get_db


models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Zapete Fantasy API")

cred = credentials.Certificate(environ['FIREBASE_CREDENTIALS'])
firebase_admin.initialize_app(cred)

VALID_IMAGE_MIME_TYPES = ['image/jpeg', 'image/png', 'image/webp']

@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url='/docs')

@app.post("/auth/token", tags=['Authentication'], response_model=schemas.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password", headers={"WWW-Authenticate": "Bearer"})
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    print(access_token_expires*60, flush=True)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    return {
        "token_type": "bearer",
        "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES,
        "access_token": access_token,
        'refresh_token': create_refresh_token(data={"sub": form_data.username}),
    }


@app.post("/auth/refresh", tags=['Authentication'],response_model=schemas.Token)
async def refresh(form_data: OAuth2RefreshTokenForm = Depends(), db: Session = Depends(get_db)):
    try:
        token = form_data.refresh_token
        username = decode_token(token).get('sub')

        print(f"Username: {username}", flush=True)
        print(f"Token: {token}", flush=True)
        # Validate email
        if crud.get_user_password(db, username=username):
            # Create and return token
            access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            access_token = create_access_token(data={"sub": username}, expires_delta=access_token_expires)
    
            return {
                "token_type": "bearer",
                "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES,
                "access_token": access_token,
                'refresh_token': create_refresh_token(data={"sub": username}),
            }
        else:
            raise HTTPException(status_code=403, detail="This user does not exist.")

    except Exception as e:
        print(f"An exception occurred: {e}", flush=True)
        raise HTTPException(status_code=401, detail="Incorrect username or password", headers={"WWW-Authenticate": "Bearer"})


@app.get("/users/me", response_model=schemas.User)
async def read_users_me(current_user: models.User = Depends(get_current_active_user)):
    return current_user


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    user.hashed_password = get_password_hash(user.hashed_password)
    return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip)
    return users

#update user
@app.put("/users/", response_model=schemas.User)
def update_user(money: float, points: int, current_user: models.User = Depends(get_current_active_user), db: Session = Depends(get_db)):
    db_user = crud.get_user(db, username= current_user.username)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return crud.update_user(db=db, username=current_user.username, money=money, points= points)


@app.get("/profile/image", tags=["Profile"],
         status_code=200, response_class=FileResponse,
         responses={404: {"description": "User doesn't exists."}})
async def get_user_profile_image(current_user: models.User = Depends(get_current_active_user), db: Session = Depends(get_db)):
    if not (user_profile_image_url := crud.get_user_profile_image_url(db, username=current_user.username)):
        print("User doesn't exists.", flush=True)
        raise HTTPException(status_code=404, detail="User doesn't exists.")
    print(user_profile_image_url, flush=True)
    if Path(user_profile_image_url).exists():
        print("Returning image", flush=True)
        return FileResponse(user_profile_image_url, filename=Path(user_profile_image_url).name)
    else:
        print("Returning placeholder", flush=True)
        return FileResponse(f"{environ['IMAGES_PATH']}/placeholder.png", filename="placeholder.png")


@app.put("/profile/image", tags=["Profile"],
         status_code=204,
         responses={404: {"description": "User doesn't exists."}, 400: {"description": f"File is not a valid image file. Valid types: {', '.join(VALID_IMAGE_MIME_TYPES)}"}})
async def set_user_profile_image(file: UploadFile, current_user: models.User = Depends(get_current_active_user), db: Session = Depends(get_db)):
    if not (user := crud.get_user(db, current_user.username)):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User doesn't exists.")

    if file.content_type not in VALID_IMAGE_MIME_TYPES:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"File is not a valid image file. Valid types: {', '.join(VALID_IMAGE_MIME_TYPES)}")

    file_extension = guess_extension(file.content_type)
    path = f"{environ['IMAGES_PATH']}/{current_user.username}{file_extension}"

    if crud.set_user_profile_image_url(db, user, path):
        contents = await file.read()
        with open(path, 'wb') as f:
            f.write(contents)


@app.get("/players/", response_model=List[schemas.Player])
def read_players(skip: int = 0, db: Session = Depends(get_db)):
    players = crud.get_players(db, skip=skip)
    print(players[0].user_id, flush=True) #llega None si no tiene dueño
    return players

# update player user_id
@app.put("/players/", response_model=schemas.Player)
def update_player(player_id: int, line_up: bool, user_id: Optional[str] = None, db: Session = Depends(get_db)):
    db_player = crud.get_player(db, player_id=player_id)
    if db_player is None:
        raise HTTPException(status_code=404, detail="Player not found")
    return crud.update_player(db=db, player_id=player_id, line_up= line_up, user_id=user_id)


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

#get post
@app.get("/posts/", response_model=List[schemas.Post])
def read_posts(skip: int = 0, db: Session = Depends(get_db)):
    posts = crud.get_posts(db, skip=skip)
    return posts

# create post
@app.post("/posts/", response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
    return crud.create_post(db=db, post=post)

# FIREBASE 

@app.post('/notifications/subscribe', status_code=status.HTTP_202_ACCEPTED, tags=["Notifications"])
def suscribe_user_firebase(token: schemas.FirebaseClientToken, current_user: models.User = Depends(get_current_active_user)):
    # Procesamos el nombre de la provincia quitando espacios y tíldes y se suscribe al usuario
    messaging.subscribe_to_topic([token.fcm_client_token], unidecode(current_user.username.replace(' ', '_')))
    messaging.subscribe_to_topic([token.fcm_client_token], 'All')
    print(f"User {current_user.username} subscribed to {unidecode(current_user.username.replace(' ', '_'))} and All", flush=True)

async def send_notification(message: schemas.Message, topic: str = 'All'):
    messaging.send(
        messaging.Message(
            data={k: f'{v}' for k, v in dict(message).items()},
            topic=unidecode(topic.replace(' ', '_'))
        )
    )

    messaging.send(
        messaging.Message(
            notification=messaging.Notification(
                **dict(message)
            ),
            topic=unidecode(topic.replace(' ', '_'))
        )
    )


@app.post("/notifications", tags=["Notifications"])
async def send_broadcast_notification(message: schemas.Message, _: models.User = Depends(get_current_active_user)):
    await send_notification(message)


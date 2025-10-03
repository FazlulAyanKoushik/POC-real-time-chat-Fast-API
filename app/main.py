from fastapi import FastAPI, Depends, HTTPException, status, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
import json
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.crud import user as user_crud, thread as thread_crud, message as message_crud
from app.schemas import auth, user as user_schema, thread as thread_schema, message as message_schema

from app.database.session import get_db
from app.auth.jwt import create_access_token, get_current_user
from app.auth.jwt import verify_password


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"Hello": "World"}


# Auth Routes
@app.post(f"{settings.API_V1_STR}/auth/register", response_model=user_schema.UserResponse)
async def register(user_data: user_schema.UserCreate, db: AsyncSession = Depends(get_db)):
    db_user = await user_crud.get_user_by_email(db, email=str(user_data.email))
    print("print user email", db_user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    db_user = await user_crud.get_user_by_username(db, username=user_data.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already taken")

    return await user_crud.create_user(db=db, user=user_data)


@app.post(f"{settings.API_V1_STR}/auth/login", response_model=auth.Token)
def login(user_data: user_schema.UserLogin, db: Session = Depends(get_db)):
    user = user_crud.get_user_by_username(db, username=user_data.username)
    if not user or not verify_password(user_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


# User Routes
@app.get(f"{settings.API_V1_STR}/users/me", response_model=user_schema.UserResponse)
def read_users_me(current_user: user_schema.UserResponse = Depends(get_current_user)):
    return current_user


@app.get(f"{settings.API_V1_STR}/users", response_model=List[user_schema.UserResponse])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = user_crud.get_users(db, skip=skip, limit=limit)
    return users

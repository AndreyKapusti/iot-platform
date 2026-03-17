from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from src.schemas.user import UserCreate, UserResponse, Token
from src.core.database import db
from src.core.security import get_password_hash, verify_password, create_access_token
from datetime import timedelta

router = APIRouter()

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate):
    existing_user = await db.fetch_one(
        'SELECT id FROM users WHERE email = %s',
        user_data.email
    )
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Пользователь с таким email уже существует'
        )
    
    existing_username = await db.fetch_one(
        'SELECT id FROM users WHERE username = %s',
        user_data.username
    )
    if existing_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Пользователь с таким именем уже существует'
        )
    
    hashed_password = get_password_hash(user_data.password)

    user_id = await db.fetch_val(
        """
        INSERT INTO users (email, username, hashed_password)
        VALUES (%s, %s, %s)
        RETURNING id
        """,
        user_data.email, user_data.username, hashed_password
    )

    return{
        'id': user_id,
        'email': user_data.email,
        'username': user_data.username,
        'is_active': True
    }

@router.post('/login', response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await db.fetch_one(
        """
        SELECT
            id,
            email,
            username,
            hashed_password,
            is_active
        FROM users
        WHERE username = %s
        """,
        form_data.username
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Неверное имя пользователя или пароль',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    
    if not verify_password(form_data.password, user['hashed_password']):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Неверное имя пользователя или пароль',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    
    if not user['is_active']:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Пользователь заболкирован'
        )
    
    access_token = create_access_token(
        data={'sub': user['username']},
        expires_delta=timedelta(minutes=300)
    )

    return {'access_token': access_token, 'token_type': 'bearer'}
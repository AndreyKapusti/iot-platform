from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from src.core.database import db
from src.core.security import SECRET_KEY, ALGORITHM
from src.schemas.user import TokenData
from datetime import datetime

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/api/v1/auth/login')

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Не удалось подтвердить учётные данные',
        headers={'WWW-Authenticate': 'Bearer'},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        expires_at = payload.get('exp')
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    
    user = await db.fetch_one(
        """
        SELECT
            id,
            email,
            username,
            is_active
        FROM users
        WHERE username = %s
        """,
        token_data.username
    )

    if user is None:
        raise credentials_exception
    return{
        'id': user['id'],
        'email': user['email'],
        'username': user['username'],
        'is_active': user['is_active'],
        'exp': datetime.fromtimestamp(expires_at)
    }
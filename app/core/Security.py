from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext # Уже импортирован в user_models, но для ясности можно здесь

from app.core.config import settings
from app.models import user_models # Для доступа к get_user и pwd_context
from app.schemas.token_schemas import TokenData

# Контекст для хеширования паролей (используем тот же, что и в user_models)
pwd_context = user_models.pwd_context

# Схема OAuth2 для получения токена из заголовка Authorization
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/token") # Указывает на эндпоинт получения токена

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Проверяет совпадение пароля с хешем."""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Генерирует хеш пароля."""
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Создает JWT токен доступа."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)) -> user_models.User:
    """
    Декодирует токен, проверяет его валидность и возвращает пользователя.
    Используется как зависимость для защищенных эндпоинтов.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception
    
    user = user_models.get_user(email=token_data.email)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(current_user: user_models.User = Depends(get_current_user)) -> user_models.User:
    """
    Проверяет, активен ли пользователь (в данном примере все пользователи "активны").
    Можно расширить для проверки статуса пользователя (например, is_active).
    """
    # if not current_user.is_active: # Если бы у пользователя было поле is_active
    #     raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

def authenticate_user(email: str, password: str) -> Optional[user_models.User]:
    """Аутентифицирует пользователя по email и паролю."""
    user = user_models.get_user(email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user
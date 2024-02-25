from typing import Optional

from jose import JWTError, jwt
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.repository import users as repository_users

from src.conf.config import settings
import redis
import pickle


class Auth:
    """
    Auth class provides methods for handling authentication and authorization processes including
    password hashing, token generation and verification, and user authentication.
    """

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    SECRET_KEY = settings.secret_key
    ALGORITHM = settings.algorithm
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")
    r = redis.Redis(host=settings.redis_host, port=settings.redis_port, db=0)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """
        Verify whether the provided plain password matches the hashed password.

        :param plain_password: Plain text password to verify.
        :param hashed_password: Hashed password to verify against.
        :return: True if passwords match, False otherwise.
        """
        return self.pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str) -> str:
        """
        Generate a password hash for the given plain password.

        :param password: Plain text password to hash.
        :return: Hashed password.
        """
        return self.pwd_context.hash(password)

    async def create_access_token(
        self, data: dict, expires_delta: Optional[timedelta] = None
    ) -> str:
        """
        Create a new JWT access token.

        :param data: The data to include in the token.
        :param expires_delta: Optional expiration delta for the token.
        :return: Encoded JWT token as a string.
        """
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return encoded_jwt

    async def create_refresh_token(
        self, data: dict, expires_delta: Optional[timedelta] = None
    ) -> str:
        """
        Create a new JWT refresh token.

        :param data: The data to include in the token.
        :param expires_delta: Optional expiration delta for the token, defaults to 7 days.
        :return: Encoded JWT refresh token as a string.
        """
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(days=7)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return encoded_jwt

    async def decode_refresh_token(self, refresh_token: str) -> str:
        """
        Decode a JWT refresh token.

        :param refresh_token: The refresh token to decode.
        :return: The subject (typically user identifier) contained in the token.
        :raises HTTPException: If token is invalid or expired.
        """
        try:
            payload = jwt.decode(
                refresh_token, self.SECRET_KEY, algorithms=[self.ALGORITHM]
            )
            if payload.get("scope") != "refresh_token":
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid scope for token",
                )
            return payload.get("sub")
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
            )

    async def get_current_user(
        self, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
    ):
        """
        Retrieve the current user based on the JWT token.

        :param token: JWT token.
        :param db: Database session from dependency injection.
        :return: The user object associated with the token.
        :raises HTTPException: If token is invalid, expired, or the user does not exist.
        """
        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            email: str = payload.get("sub")
            if email is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Could not validate credentials",
                )
            # Check if user is cached in Redis
            user_data = self.r.get(f"user:{email}")
            if user_data is None:
                user = await repository_users.get_user_by_email(email, db)
                if user is None:
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Could not validate credentials",
                    )
                # Cache user in Redis
                self.r.set(
                    f"user:{email}", pickle.dumps(user), ex=900
                )  # Cache expiration set to 15 minutes
            else:
                user = pickle.loads(user_data)
            return user
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
            )

auth_service = Auth()

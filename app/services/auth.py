from datetime import datetime, timedelta
from fastapi import HTTPException, Depends

import jwt
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials


class AuthService:
    """
    Service class responsible for handling JSON Web Token (JWT) authentication.

    Provides static methods to create JWT access tokens and to verify the validity of incoming JWT tokens in HTTP requests.
    """

    SECRET_KEY = "myverysecretkey"
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30

    @staticmethod
    def create_access_token(data: dict, expires_delta: timedelta | None = None):
        """
        Creates a JSON Web Token (JWT) access token.

        The token includes the provided data and an expiration time. If no expiration is specified, the token defaults to expire in 30
        minutes.

        :param data: A dictionary containing user-related data to encode in the token (e.g., username).
        :param expires_delta: Optional timedelta representing the token's time-to-live.
        :return: A JWT string that encodes the input data along with an expiration timestamp.
        """

        to_encode = data.copy()
        expire = datetime.utcnow() + (expires_delta or timedelta(minutes=AuthService.ACCESS_TOKEN_EXPIRE_MINUTES))
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, AuthService.SECRET_KEY, algorithm=AuthService.ALGORITHM)

    @staticmethod
    def verify_token(credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
        """
        Validates the JWT access token.

        Decodes the token using the secret key and algorithm. If the token is invalid or the payload is malformed, raises an HTTP 401
        Unauthorized error.

        :param credentials: The HTTP bearer token extracted from the Authorization header.
        :raise HTTPException: If the token is invalid or does not contain the expected payload.
        """
        token = credentials.credentials
        try:
            payload = jwt.decode(token, AuthService.SECRET_KEY, algorithms=[AuthService.ALGORITHM])
            if payload.get("sub") is None:
                raise HTTPException(status_code=401, detail="Invalid token payload")
        except jwt.PyJWTError:
            raise HTTPException(status_code=401, detail="Invalid token")

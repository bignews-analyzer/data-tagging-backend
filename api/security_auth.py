from fastapi import Request, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from core.security import decode_access_token
from database.redis_session import redis_session_access
from models import User

from sqlalchemy.orm import Session

class JWTBearer(HTTPBearer):
    def __init__(self,
                 auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid authentication scheme.")
            token_decoded = decode_access_token(credentials.credentials)
            access_token_in_redis = redis_session_access.get(token_decoded['sub'])
            if access_token_in_redis is None:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Invalid token"
                )
            return token_decoded
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid authorization code.")

class CheckAuthorization:
    AUTHORIZATION_ONLY_ADMIN = 0
    AUTHORIZATION_ONLY_ONESELF = 1

    def check_authorization(self,
                                  mode: int,
                                  user: User,
                                  user_id: str = None) -> bool:
        if mode == self.AUTHORIZATION_ONLY_ADMIN:
            if user.is_superuser is True:
                return True
            return False
        if mode == self.AUTHORIZATION_ONLY_ONESELF:
            if user.is_superuser is True or user.id == user_id:
                return True
            return False
        return True

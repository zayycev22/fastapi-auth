from typing import Type, Optional
from tortoise.exceptions import DoesNotExist, IntegrityError

from fastapi_auth.exceptions import UserAlreadyExists
from fastapi_auth.models import user_model
from fastapi_auth.repositories import BaseTokenRepository, BaseUserRepository
from fastapi_auth.tortoise_models.models import Token, BaseUser


class TokenRepository(BaseTokenRepository[Token]):

    def __init__(self, tp: Type[Token]):
        super().__init__(tp)

    async def create(self, user: BaseUser) -> Token:
        token = await self.token_type.create(user=user)
        return token

    async def get_by_key(self, key: str) -> Optional[Token]:
        try:
            return await self.token_type.get(key=key)
        except DoesNotExist:
            return None

    async def delete(self, token: Token) -> None:
        return await token.delete()

    async def get_by_user(self, user: BaseUser) -> Optional[Token]:
        try:
            return await self.token_type.get(user=user)
        except DoesNotExist:
            return None


class UserRepository(BaseUserRepository[BaseUser]):
    def __init__(self, user_m: Type[BaseUser]):
        super().__init__(user_m)

    async def get(self, **kwargs) -> Optional[BaseUser]:
        try:
            return await self.user_model.get(**kwargs)
        except DoesNotExist:
            return None

    async def create(self, **kwargs) -> BaseUser:
        password = kwargs.pop('password', None)
        user = self.user_model(**kwargs)
        if password is not None:
            user.set_password(password)
        else:
            user.set_unusable_password()
        try:
            await user.save(created=True)
        except IntegrityError:
            raise UserAlreadyExists
        return user

    async def get_by_natural_key(self, natural_key: str) -> Optional[BaseUser]:
        kwargs = {self.user_model.USERNAME_FIELD: natural_key}
        try:
            return await self.user_model.get(**kwargs)
        except DoesNotExist:
            return None

    async def delete(self, user: BaseUser) -> None:
        await user.delete()

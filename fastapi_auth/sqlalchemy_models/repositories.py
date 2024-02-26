from typing import Type, Optional, Generic
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from fastapi_auth.exceptions import UserAlreadyExists
from fastapi_auth.models import user_model
from fastapi_auth.sqlalchemy_models.models import Token
from fastapi_auth.repositories import BaseTokenRepository, BaseUserRepository


class TokenRepository(BaseTokenRepository[Token]):
    def __init__(self, session: AsyncSession, tp: Type[Token]):
        self.session = session
        super().__init__(tp)

    async def create(self, user: user_model) -> Token:
        token = self.token_type(user_id=user.id)
        self.session.add(token)
        await token.save(session=self.session)
        return token

    async def get_by_key(self, key: str) -> Optional[Token]:
        query = select(self.token_type).where(self.token_type.key == key)
        result = (await self.session.execute(query)).scalar_one_or_none()
        return result

    async def delete(self, token: Token) -> None:
        await self.session.delete(token)
        await self.session.commit()

    async def get_by_user(self, user: user_model) -> Optional[Token]:
        query = select(self.token_type).where(self.token_type.user_id == user.id)
        result = (await self.session.execute(query)).scalar_one_or_none()
        return result


class UserRepository(BaseUserRepository[user_model]):
    def __init__(self, session: AsyncSession, user_m: Type[user_model]):
        self.session = session
        super().__init__(user_m)

    async def get(self, **kwargs) -> Optional[user_model]:
        filters = [getattr(self.user_model, key) == value for key, value in kwargs.items()]
        query = select(self.user_model).filter(and_(*filters))
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def create(self, **kwargs) -> user_model:
        password = kwargs.pop('password', None)
        user = self.user_model(**kwargs)
        if password is not None:
            user.set_password(password)
        else:
            user.set_unusable_password()
        try:
            await user.save(session=self.session, created=True)
        except IntegrityError:
            raise UserAlreadyExists
        return user

    async def get_by_natural_key(self, natural_key: str) -> Optional[user_model]:
        key = self.user_model.USERNAME_FIELD
        query = select(self.user_model).where(getattr(self.user_model, key) == natural_key)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def delete(self, user: user_model) -> None:
        await self.session.delete(user)
        await self.session.commit()

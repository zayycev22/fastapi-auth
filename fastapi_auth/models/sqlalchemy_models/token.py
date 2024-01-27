import datetime
from typing import Type, Optional, TYPE_CHECKING
from sqlalchemy import DateTime, func, ForeignKey, String, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column, relationship, declared_attr

from fastapi_auth.models import user_model
from fastapi_auth.models.token import AbstractToken
from fastapi_auth.repositories.base import BaseTokenRepository


class Token(AbstractToken):
    __tablename__ = 'token'

    id: Mapped[int] = mapped_column(primary_key=True)
    key: Mapped[str] = mapped_column(String(40), nullable=True)
    time_created: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    @declared_attr
    def user_id(cls) -> Mapped[int]:
        return mapped_column(ForeignKey('user.id'), nullable=False)

    @declared_attr
    def user(cls) -> Mapped[user_model]:
        return relationship(back_populates="token", cascade="all, delete-orphan")

    async def save(self, **kwargs):
        session: AsyncSession = kwargs.get('session')
        if not self.key:
            self.key = self.generate_key()
        return await session.commit()


class TokenRepository(BaseTokenRepository[Token]):
    def __init__(self, session: AsyncSession, tm: Type[Token]):
        self.session = session
        super().__init__(tm)

    async def create(self, **kwargs: dict) -> Token:
        token = self.token_model(**kwargs)
        await token.save(session=self.session)
        return token

    async def get_by_key(self, key: str) -> Optional[Token]:
        query = select(self.token_model).where(self.token_model.key == key)
        result = (await self.session.execute(query)).scalar_one_or_none()
        return result

    async def delete(self, token: Token) -> None:
        await self.session.delete(token)
        await self.session.commit()

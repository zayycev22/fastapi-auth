import datetime
from typing import Type, Optional
from sqlalchemy import DateTime, func, ForeignKey, String, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column, declared_attr
from fastapi_auth.models import AbstractToken
from fastapi_auth.repositories import BaseTokenRepository


class Token(AbstractToken):
    __tablename__ = 'token'

    id: Mapped[int] = mapped_column(primary_key=True)
    key: Mapped[str] = mapped_column(String(40), nullable=True)
    time_created: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    @declared_attr
    def user_id(cls) -> Mapped[int]:
        return mapped_column(ForeignKey('user.id'), nullable=False)

    async def save(self, **kwargs):
        session: AsyncSession = kwargs.get('session')
        if not session:
            raise ValueError("Session cannot be None")
        if not self.key:
            self.key = self.generate_key()
        session.add(self)
        return await session.commit()


class TokenRepository(BaseTokenRepository[Token]):
    def __init__(self, session: AsyncSession, tm: Type[Token]):
        self.session = session
        super().__init__(tm)

    async def create(self, user_id: int) -> Token:
        token = self.token_model(user_id=user_id)
        self.session.add(token)
        await token.save(session=self.session)
        return token

    async def get_by_key(self, key: str) -> Optional[Token]:
        query = select(self.token_model).where(self.token_model.key == key)
        result = (await self.session.execute(query)).scalar_one_or_none()
        return result

    async def delete(self, token: Token) -> None:
        await self.session.delete(token)
        await self.session.commit()

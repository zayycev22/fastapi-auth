import datetime

from sqlalchemy import DateTime, func, String, Boolean, ForeignKey
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column, declared_attr, backref

from fastapi_auth.models import AbstractToken, AbstractBaseUser
from fastapi_auth.signals.signal import main_signal


class Token(AbstractToken):
    __tablename__ = 'token'

    id: Mapped[int] = mapped_column(primary_key=True)
    key: Mapped[str] = mapped_column(String(40), nullable=True)
    time_created: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    @declared_attr
    def user_id(cls) -> Mapped[int]:
        return mapped_column(ForeignKey('user.id', ondelete="cascade"), nullable=False)

    async def save(self, **kwargs) -> None:
        session: AsyncSession = kwargs.get('session')
        if not session:
            raise ValueError("Session cannot be None")
        if not self.key:
            self.key = self.generate_key()
        session.add(self)
        await main_signal.emit_before_create(instance=self, session=session)
        await session.commit()
        return await main_signal.emit_after_create(instance=self, session=session)


class BaseUser(AbstractBaseUser):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    password: Mapped[str] = mapped_column(String(128))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False)
    time_created: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    USERNAME_FIELD = ""

    async def save(self, **kwargs) -> None:
        session: AsyncSession = kwargs.get('session')
        if session is None:
            raise ValueError("Session cannot be None")
        session.add(self)
        await main_signal.emit_before_create(instance=self, session=session)
        await session.commit()
        return await main_signal.emit_after_create(instance=self, session=session)

    async def delete(self, **kwargs) -> None:
        session: AsyncSession = kwargs.get('session')
        if session is None:
            raise ValueError("Session cannot be None")
        await session.delete(self)
        await session.commit()


class User(BaseUser):
    username: Mapped[str] = mapped_column(String(128), nullable=False, unique=True)
    USERNAME_FIELD = "username"


class EmailUser(BaseUser):
    email: Mapped[str] = mapped_column(String(128), nullable=False, unique=True)

    USERNAME_FIELD = "email"

from typing import Type, Optional, Any
from tortoise.models import MODEL
from fastapi_auth.models import AbstractToken, AbstractBaseUser, ExternalBaseModel
from tortoise import fields, Model, BaseDBAsyncClient
from fastapi_auth.signals.signal import main_signal


class ExModel(Model, ExternalBaseModel):

    async def save(self, created: bool = False, **kwargs) -> None:
        await super().save()
        return await main_signal.emit_after_save(instance=self, created=created)

    @classmethod
    async def create(cls: Type[MODEL], using_db: Optional[BaseDBAsyncClient] = None, **kwargs: Any
                     ) -> MODEL:
        instance = await super().create()
        await main_signal.emit_after_save(instance=instance, created=True)
        return instance

    class Meta:
        abstract = True


class BaseUser(Model, AbstractBaseUser):
    id = fields.IntField(pk=True)
    password = fields.CharField(max_length=128)
    is_active = fields.BooleanField(default=False)
    is_superuser = fields.BooleanField(default=False)
    time_created = fields.DatetimeField(auto_now_add=True)

    USERNAME_FIELD = ""

    async def save(self, created: bool = False, **kwargs) -> None:
        await super().save()
        return await main_signal.emit_after_save(instance=self, created=created)

    @classmethod
    async def create(
            cls: Type[MODEL], using_db: Optional[BaseDBAsyncClient] = None, **kwargs: Any
    ) -> MODEL:
        instance = await super().create()
        await main_signal.emit_after_save(instance=instance, created=True)
        return instance

    class Meta:
        table = "user"
        abstract = True


class User(BaseUser):
    username = fields.CharField(max_length=128, null=False, unique=True)
    USERNAME_FIELD = "username"

    class Meta:
        table = "user"
        abstract = True


class EmailUser(BaseUser):
    email = fields.CharField(max_length=128, null=False, unique=True)
    USERNAME_FIELD = "email"

    class Meta:
        table = "user"
        abstract = True


class Token(Model, AbstractToken):
    id = fields.IntField(pk=True)
    key = fields.CharField(max_length=40, unique=True)
    time_created = fields.DatetimeField(auto_now_add=True)
    user: fields.OneToOneRelation[BaseUser] = fields.OneToOneField("models.User")

    async def save(self, created: bool = False, **kwargs) -> None:
        if not self.key:
            self.key = self.generate_key()
        await super().save()
        return await main_signal.emit_after_save(instance=self, created=created)

    @classmethod
    async def create(cls: Type[MODEL], using_db: Optional[BaseDBAsyncClient] = None, **kwargs: Any
                     ) -> MODEL:
        instance = await super().create(using_db=using_db, **kwargs)
        await main_signal.emit_after_save(instance, created=True)
        return instance

    class Meta:
        abstract = True
        table = "token"

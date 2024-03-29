try:
    from fastapi_auth_tortoise_models.repositories import TokenRepository, UserRepository
    from fastapi_auth_tortoise_models.models import EmailUser, BaseUser, User, Token, ExModel

    __all__ = ['TokenRepository', 'UserRepository', 'EmailUser', 'BaseUser', 'User', 'Token', 'ExModel']

except ImportError as error:
    if "No module named" in str(error):
        error = "No module named 'fastapi_auth_tortoise_models', run pip install fastapi_auth_tortoise_models"
    raise ImportError(error)

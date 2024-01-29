import secrets
from typing import Union
import warnings
from passlib.context import CryptContext

try:
    from settings import SECRET_KEY
except ImportError:
    raise ImportError("Couldn't import SECRET_KEY from settings.py")

warnings.simplefilter('ignore')

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

UNUSABLE_PASSWORD_PREFIX = "!"
RANDOM_STRING_CHARS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
UNUSABLE_PASSWORD_SUFFIX_LENGTH = (
    22  # number of random chars to add after UNUSABLE_PASSWORD_PREFIX
)


class Hasher:

    @staticmethod
    def get_password_hash(plain_password: Union[str, bytes]):
        return pwd_context.hash(plain_password, salt=SECRET_KEY)

    @staticmethod
    def verify_password(plain_password: Union[str, bytes, None], hashed_password: Union[str, bytes]) -> bool:
        if plain_password is None:
            return False
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def make_password(raw_password: Union[str, bytes, None]):
        if raw_password is None:
            return UNUSABLE_PASSWORD_PREFIX + Hasher.get_random_string(
                UNUSABLE_PASSWORD_SUFFIX_LENGTH
            )
        if not isinstance(raw_password, (bytes, str)):
            raise TypeError(
                "Password must be a string or bytes, got %s." % type(raw_password).__qualname__
            )
        return Hasher.get_password_hash(raw_password)

    @staticmethod
    def get_random_string(length: int, allowed_chars: str = RANDOM_STRING_CHARS):
        """
        Return a securely generated random string.

        The bit length of the returned value can be calculated with the formula:
            log_2(len(allowed_chars)^length)

        For example, with default `allowed_chars` (26+26+10), this gives:
          * length: 12, bit length =~ 71 bits
          * length: 22, bit length =~ 131 bits
        """
        return "".join(secrets.choice(allowed_chars) for i in range(length))

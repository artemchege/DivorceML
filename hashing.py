from passlib.context import CryptContext


pwd_ctx = CryptContext(schemes=['bcrypt'], deprecated='auto')


class Hash:

    @staticmethod
    def hash_password(password: str) -> str:
        return pwd_ctx.hash(password)

    @staticmethod
    def verify(plain_password: str, hashed_password: str):
        return pwd_ctx.verify(plain_password, hashed_password)

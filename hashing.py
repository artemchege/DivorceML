from passlib.context import CryptContext


pwd_ctx = CryptContext(schemes=['bcrypt'], deprecated='auto')


class Hash:

    @staticmethod
    def hash_password(password: str) -> str:
        return pwd_ctx.hash(password)

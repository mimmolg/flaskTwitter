import secrets


class DBConfig:
    MONGO_URI = 'mongodb://localhost:27017/demoDB'
    SECRET_KEY = secrets.token_urlsafe(32)
    BCRYPT_LOG_ROUNDS = 12

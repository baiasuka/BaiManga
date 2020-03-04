from datetime import timedelta

SECRET_KEY = 'kj08w7hnvuwjhs2'
PERMANENT_SESSION_LIFETIME = timedelta(hours=2)

DIALECT = 'postgresql'
DRIVER = 'psycopg2'
HOST = '127.0.0.1'
PORT = '5432'
USERNAME = 'postgres'
PASSWORD = '2333'
DATABASE = 'BaiManga'
SQLALCHEMY_DATABASE_URI = "{}+{}://{}:{}@{}:{}/{}?charset=utf8mb4".format(DIALECT, DRIVER, USERNAME, PASSWORD, HOST,
                                                                          PORT, DATABASE)

REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379
REDIS_CACHE_DB = 1
REDIS_PASSWORD = "2333"
REDIS_CACHE_DB_EXPIRED = 3600
REDIS_CACHE_CONFIG = {
    "host": REDIS_HOST,
    "port": REDIS_PORT,
    "db": REDIS_CACHE_DB,
    "password": REDIS_PASSWORD,
    "expired": REDIS_CACHE_DB_EXPIRED  # s
}
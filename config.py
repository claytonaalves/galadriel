import os


class BaseConfig:
    DEBUG = True
    #SERVER_NAME = "localhost:8080"

    BASE_DIR = os.path.abspath(os.path.dirname(__file__))

    DATABASE_HOST = os.environ.get('FIREBIRD_HOST')
    DATABASE_USER = os.environ.get('FIREBIRD_USER')
    DATABASE_PASSWORD = os.environ.get('FIREBIRD_PASSWORD')

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'firebird+fdb://{}:{}@{}/ello?charset=latin1'.format(DATABASE_USER, DATABASE_PASSWORD, DATABASE_HOST)

    DATABASE_CONNECT_OPTIONS = {}

    # Application threads. A common general assumption is
    # using 2 per available processor cores - to handle
    # incoming requests using one and performing background
    # operations using the other.
    THREADS_PER_PAGE = 2

    # Enable protection agains *Cross-site Request Forgery (CSRF)*
    CSRF_ENABLED = True

    # Use a secure, unique and absolutely secret key for
    # signing the data.
    CSRF_SESSION_KEY = "mysecretkey"

    # Secret key for signing cookies
    SECRET_KEY = "mysecretkey"

    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'app/static/uploads')

    BABEL_DEFAULT_LOCALE = 'pt_BR'
    # BABEL_DEFAULT_TIMEZONE = ??


# class ApiConfig(BaseConfig):
#     SERVER_NAME = "localhost:5000"
# 
# 
# class AdminConfig(BaseConfig):
#     SERVER_NAME = "localhost:5001"

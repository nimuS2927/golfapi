import os
from pathlib import Path

from dotenv import load_dotenv, find_dotenv

from core.utils import hash_password

load_dotenv(find_dotenv())

DEBUG = False


class ConfigBasic(object):
    _instance = None

    def __new__(cls):
        if not cls._instance:
            instance = super(ConfigBasic, cls).__new__(cls)
            cls._instance = instance
        return cls._instance

    def __init__(self):
        self.__PROJECT_DIR: Path = Path(__file__).parent.parent
        self.__PATH_TO_FILES: Path = Path.joinpath(self.__PROJECT_DIR, 'library', 'files')
        self.__PATH_TO_FILES.mkdir(parents=True, exist_ok=True)
        self.__PATH_TO_FIXTURES: Path = Path.joinpath(self.__PROJECT_DIR, 'library', 'fixtures')
        self.__PATH_TO_FIXTURES.mkdir(parents=True, exist_ok=True)
        self.__PATH_TO_IMAGES: Path = Path.joinpath(self.__PROJECT_DIR, 'library', 'images')
        self.__PATH_TO_IMAGES.mkdir(parents=True, exist_ok=True)

    # region Functions to getting basic settings
    @property
    def project_dir(self) -> Path:
        return self.__PROJECT_DIR

    @property
    def path_to_files(self) -> Path:
        return self.__PATH_TO_FILES

    @property
    def path_to_fixtures(self) -> Path:
        return self.__PATH_TO_FIXTURES

    @property
    def path_to_images(self) -> Path:
        return self.__PATH_TO_IMAGES
    # endregion


c_basic = ConfigBasic()


def path_to_db(path_root) -> Path:
    path_dir_db = os.getenv("PATH_TO_DB", None)
    if path_dir_db:
        path_dir_db = Path(path_dir_db)
        return path_dir_db
    path_dir_db = Path.joinpath(path_root, 'database')
    path_dir_db.mkdir(parents=True, exist_ok=True)
    return path_dir_db


class ConfigDB(object):
    _instance = None

    def __new__(cls):
        if not cls._instance:
            instance = super(ConfigDB, cls).__new__(cls)
            cls._instance = instance
        return cls._instance

    def __init__(self):
        self.__NAME: str = os.getenv("DB_NAME")
        self.__USER: str = os.getenv("DB_USER")
        self.__PASSWORD: str = os.getenv("PASSWORD")
        self.__HOST: str = os.getenv("HOST")
        self.__PORT: str = os.getenv("PORT", '5432')
        self.__PATH: Path = path_to_db(c_basic.project_dir)

    # region Functions to getting db settings
    @property
    def name(self) -> str:
        return self.__NAME

    @property
    def user(self) -> str:
        return self.__USER

    @property
    def password(self) -> str:
        return self.__PASSWORD

    @property
    def host(self) -> str:
        return self.__HOST

    @property
    def port(self) -> str:
        return self.__PORT

    @property
    def path(self) -> Path:
        return self.__PATH
    # endregion


c_db = ConfigDB()


class ConfigAuthJWT(object):
    _instance = None

    def __new__(cls):
        if not cls._instance:
            instance = super(ConfigAuthJWT, cls).__new__(cls)
            cls._instance = instance
        return cls._instance

    def __init__(self):
        self.__PRIVATE_KEY_PATH: Path = Path(os.getenv("PRIVATE_KEY_PATH"))
        self.__PUBLIC_KEY_PATH: Path = Path(os.getenv("PUBLIC_KEY_PATH"))
        self.__ALGORITHM: str = os.getenv("ALGORITHM")
        self.__SUPERUSER: str = os.getenv("AUTH_SUPERUSER")
        self.__PASSWORD: bytes = hash_password(os.getenv("AUTH_PASSWORD"))
        self.__ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
        self.__REFRESH_TOKEN_EXPIRE_DAYS: int = 30
        self.__TOKEN_TYPE_FIELD = "type"
        self.__ACCESS_TOKEN_TYPE = "access"
        self.__REFRESH_TOKEN_TYPE = "refresh"

    # region Functions to getting db settings
    @property
    def private_key_path(self) -> Path:
        return self.__PRIVATE_KEY_PATH

    @property
    def public_key_path(self) -> Path:
        return self.__PUBLIC_KEY_PATH

    @property
    def algorithm(self) -> str:
        return self.__ALGORITHM

    @property
    def superuser(self) -> str:
        return self.__SUPERUSER

    @property
    def password(self) -> bytes:
        return self.__PASSWORD

    @property
    def access_token_expire_minutes(self) -> int:
        return self.__ACCESS_TOKEN_EXPIRE_MINUTES

    @property
    def refresh_token_expire_days(self) -> int:
        return self.__REFRESH_TOKEN_EXPIRE_DAYS

    @property
    def token_type_field(self) -> str:
        return self.__TOKEN_TYPE_FIELD

    @property
    def access_token_type(self) -> str:
        return self.__ACCESS_TOKEN_TYPE

    @property
    def refresh_token_type(self) -> str:
        return self.__REFRESH_TOKEN_TYPE
    # endregion


c_auth_jwt = ConfigAuthJWT()


def get_db_url(engine: str = 'postgresql') -> str:
    if engine == 'postgresql':
        return f'postgresql+asyncpg://{c_db.user}:{c_db.password}@{c_db.host}:{c_db.port}/{c_db.name}'
    if engine == 'sqlite':
        return f"sqlite+aiosqlite:///{Path.joinpath(c_db.path, c_db.name)}"
    else:
        raise ValueError('Unknown engine')


class ConfigProject(object):
    _instance = None

    def __new__(cls):
        if not cls._instance:
            instance = super(ConfigProject, cls).__new__(cls)
            cls._instance = instance
        return cls._instance

    def __init__(self):
        self.__basic = c_basic
        self.__db = c_db
        self.__auth_jwt = c_auth_jwt
        self.__api_v1_prefix: str = '/api/v1'
        self.__auth_v1_prefix: str = '/auth/v1'
        self.__db_url = get_db_url()
        self.__db_echo: bool = DEBUG

    # region Functions to getting project settings
    @property
    def basic(self) -> ConfigBasic:
        return self.__basic

    @property
    def db(self) -> ConfigDB:
        return self.__db

    @property
    def auth_jwt(self) -> ConfigAuthJWT:
        return self.__auth_jwt

    @property
    def api_v1_prefix(self) -> str:
        return self.__api_v1_prefix

    @property
    def auth_v1_prefix(self) -> str:
        return self.__auth_v1_prefix

    @property
    def db_echo(self) -> bool:
        return self.__db_echo

    @property
    def db_url(self) -> str:
        return self.__db_url
    # endregion


c_project = ConfigProject()

import os
import pathlib

BASE_DIR = pathlib.Path(__file__).parent


class Config:
    SECRET_KEY = os.environ.get('APP_SECRET_KEY')

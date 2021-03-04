import os
from dotenv import load_dotenv
import redis
from flask import Flask
from flask_restful import Api
import config

# Configure
load_dotenv()
app = Flask(__name__)
app.config.from_object(config.Config)
api = Api(app)
redis_pool = redis.ConnectionPool(
    host=os.environ.get('REDIS_HOST'),
    port=os.environ.get('REDIS_PORT'),
    db=0,
    decode_responses=True
)
redis_connect = redis.StrictRedis(connection_pool=redis_pool)


from . import routes

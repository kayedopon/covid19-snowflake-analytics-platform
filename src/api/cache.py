import json
import os

import redis
from dotenv import load_dotenv


load_dotenv()

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_TTL = int(os.getenv("REDIS_TTL", 500))

redis_client = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    decode_responses=True
)

def test_redis_connection():
    return redis_client.ping()

def get_cached(key):
    try:
        cached = redis_client.get(key)

        if cached is None:
            return None

        return json.loads(cached)

    except redis.RedisError:
        return None

def set_cached(key, value, ttl=REDIS_TTL):
    try:
        redis_client.setex(key, ttl, json.dumps(value, default=str))
    except redis.RedisError:
        pass

def delete_cached(key):
    redis_client.delete(key)

def clear_cache():
    redis_client.flushdb()
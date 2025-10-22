import pytest
import redis
import os

@pytest.fixture(scope='session')
def redis_client():
    client = redis.StrictRedis(host=os.getenv('REDIS_HOST', 'localhost'), port=int(os.getenv('REDIS_PORT', 6379)), decode_responses=True)
    yield client
    client.close()
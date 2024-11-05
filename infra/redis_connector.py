import redis


def connect_redis():
    r = redis.Redis(host="redis", port=6379, db=0)
    return r

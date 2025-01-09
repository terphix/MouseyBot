__all__ = ["redis"]

import os

from redis.asyncio.client import Redis

redis = Redis(host=os.getenv("REDIS_HOST"), port=os.getenv("REDIS_PORT"))

import logging
import redis
import json

from datetime import date, timedelta

from src.config.base import base_config

logger = logging.getLogger(__name__)


class RedisCache:
    def __init__(self):
        self.redis_client = redis.Redis.from_url(base_config.REDIS_URL)

    def get_cached(self, city: str, start_date: date, end_date: date, route: str):
        key = f"{city}_{start_date}_{end_date}_{route}"
        data = self.redis_client.get(key)
        if data:
            logger.error(f"Get from cache {key}")
            return json.loads(data)
        return None

    def set_cache(self, city: str, start_date: date, end_date: date, route: str, data: dict | list) -> None:
        key = f"{city}_{start_date}_{end_date}_{route}"
        self.redis_client.setex(key, timedelta(seconds=60 * 3), json.dumps(data))
        logger.error(f"Updated cache {key}")

import json
from typing import List, Any, Dict
import redis

from actions.config import REDIS_URL


class DataBaseEntityEncoder:
    def encode(self, data: Any) -> Dict[str, Any]:
        return json.dumps(data)

    def decode(self, data: Any) -> Dict[str, Any]:
        return json.loads(data)
    


class RedisDataSource:
    
    def __init__(self, redis_url: str = REDIS_URL):
        self.redis_url = redis_url
        self.encoder = DataBaseEntityEncoder()

    def get_all(self, entity = "data") -> List[Dict[str, Any]]:
        redis_client = redis.from_url(self.redis_url)
        data = redis_client.lrange(entity, 0, -1)
        parsed_data = list(map(lambda d: self.encoder.decode(d), data))
        return parsed_data
    
    def save(self, data: Dict[str, Any], entity = "data"):
        redis_client = redis.from_url(self.redis_url)
        data = self.encoder.encode(data)
        redis_client.rpush(entity, data)
    
    def get_by_id(self, id, entity = "data"):
        redis_client = redis.from_url(self.redis_url)
        return self.encoder.decode(redis_client.lindex(entity, id))
    
    def update(self, id, data: Dict[str, Any], entity = "data"):
        redis_client = redis.from_url(self.redis_url)
        data = self.encoder.encode(data)
        redis_client.rpush(entity, data)

    def delete(self, id, entity = "data"):
        redis_client = redis.from_url(self.redis_url)
        redis_client.lset(entity, id, "deleted")

    def delete_all(self, entity = "data"):
        redis_client = redis.from_url(self.redis_url)
        redis_client.delete(entity)


    
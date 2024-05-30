import dill

from redis import Redis
from typing import Any, Optional

from common.logger import get_logger


logger = get_logger(__name__)


class RedisCache:
    def __init__(
        self,
        redis_host: str = "localhost",
        redis_port: str = 6379,
        redis_db: str = 0,
    ):
        self.redis_client = Redis(
            host=redis_host,
            port=redis_port,
            db=redis_db,
        )

    def save(self, obj: Any, cache_key: str, overwrite: bool = False) -> None:
        if not overwrite:
            if self.redis_client.exists(cache_key):
                logger.warning(f"cache_key: {cache_key} already exists")
                return

        logger.debug(f"saving in cache: {cache_key}")
        self.redis_client.set(
            name=cache_key,
            value=dill.dumps(obj),
        )

    def msave(self, objs: dict[str, Any]) -> None:
        logger.debug(f"saving in cache: {objs}")
        self.redis_client.mset({k: dill.dumps(v) for k, v in objs.items()})

    def load(self, cache_key: str) -> Optional[Any]:
        if not self.redis_client.exists(cache_key):
            return

        logger.debug(f"loading from cache: {cache_key}")
        obj = self.redis_client.get(cache_key)
        obj = dill.loads(obj)

        return obj

    def mload(self, cache_keys: list[str]) -> list[Any]:
        logger.debug(f"loading from cache: {cache_keys}")
        objs = self.redis_client.mget(cache_keys)
        return [dill.loads(obj) if obj is not None else obj for obj in objs]

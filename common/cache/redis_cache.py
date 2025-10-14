import os
import dill
import joblib
import inspect
import functools

from typing import Any
from redis import Redis, ConnectionPool

from common.logger import get_logger


REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
REDIS_DB = int(os.getenv("REDIS_DB", "0"))


logger = get_logger(__name__)


class RedisCache:
    def __init__(
        self,
        redis_host: str = REDIS_HOST,
        redis_port: int = REDIS_PORT,
        redis_db: int = REDIS_DB,
        max_connections: int = 128,
    ):
        connection_pool = ConnectionPool(
            host=redis_host,
            port=redis_port,
            db=redis_db,
            max_connections=max_connections,
        )

        self.redis_client = Redis(connection_pool=connection_pool)

    def __del__(self) -> None:
        self.redis_client.close()

    def save(
        self,
        obj: Any,
        cache_key: str,
        overwrite: bool = False,
        # NOTE: Expiration time in seconds.
        expiration: int | None = None,
    ) -> None:
        if not overwrite:
            if self.redis_client.exists(cache_key):
                logger.warning(f"cache_key: {cache_key} already exists")
                return

        logger.debug(f"saving in cache: {cache_key}")
        self.redis_client.set(
            name=cache_key,
            value=dill.dumps(obj),
            ex=expiration,
        )

    def msave(self, objs: dict[str, Any]) -> None:
        logger.debug(f"saving in cache: {objs}")
        self.redis_client.mset({k: dill.dumps(v) for k, v in objs.items()})

    def load(self, cache_key: str) -> Any | None:
        if not self.redis_client.exists(cache_key):
            return

        logger.debug(f"loading from cache: {cache_key}")
        obj = self.redis_client.get(cache_key)

        return dill.loads(obj)

    def mload(self, cache_keys: list[str]) -> list[Any]:
        logger.debug(f"loading from cache: {cache_keys}")
        objs = self.redis_client.mget(cache_keys)

        return [dill.loads(obj) if obj is not None else obj for obj in objs]  # type: ignore


# NOTE: cache decorator.
def cache(
    redis_cache: RedisCache,
    expiration: int | None = None,
    overwrite: bool = False,
):
    def decorator(func):
        @functools.wraps(func)
        def get_cache_key(args, kwargs):
            return joblib.hash(
                (
                    func.__module__,
                    func.__qualname__,
                    args,
                    kwargs,
                )
            )

        async def async_wrapper(*args, **kwargs):
            cache_key = get_cache_key(args=args, kwargs=kwargs)
            cached = redis_cache.load(cache_key=cache_key)  # type: ignore
            if cached is not None:
                return cached

            result = await func(*args, **kwargs)
            redis_cache.save(
                result,
                cache_key,  # type: ignore
                overwrite=overwrite,
                expiration=expiration,
            )
            return result

        def sync_wrapper(*args, **kwargs):
            cache_key = get_cache_key(args=args, kwargs=kwargs)
            cached = redis_cache.load(cache_key=cache_key)  # type: ignore
            if cached is not None:
                return cached

            result = func(*args, **kwargs)
            redis_cache.save(
                result,
                cache_key,  # type: ignore
                overwrite=overwrite,
                expiration=expiration,
            )
            return result

        return (
            async_wrapper if inspect.iscoroutinefunction(func) else sync_wrapper
        )

    return decorator

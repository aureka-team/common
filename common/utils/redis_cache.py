import inspect
import functools

from joblib import hash
from common.cache import RedisCache


def cache(
    redis_cache: RedisCache,
    expiration: int | None = None,
    overwrite: bool = False,
):
    def decorator(func):
        @functools.wraps(func)
        def get_cache_key(args, kwargs):
            return hash(
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

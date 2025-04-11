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
        def wrapper(*args, **kwargs):
            cache_key = hash(
                obj=(
                    func.__module__,
                    func.__qualname__,
                    args,
                    kwargs,
                )
            )

            cached = redis_cache.load(cache_key=cache_key)
            if cached is not None:
                return cached

            result = func(*args, **kwargs)
            redis_cache.save(
                obj=result,
                cache_key=cache_key,
                overwrite=overwrite,
                expiration=expiration,
            )

            return result

        return wrapper

    return decorator

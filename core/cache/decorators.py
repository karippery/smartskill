from functools import wraps
from django.core.cache import cache

def cache_result(timeout=60*15):
    def decorator(func):
        @wraps(func)
        def wrapped(*args, **kwargs):
            cache_key = f'{func.__name__}_{args}_{kwargs}'
            result = cache.get(cache_key)
            if result is None:
                result = func(*args, **kwargs)
                cache.set(cache_key, result, timeout)
            return result
        return wrapped
    return decorator
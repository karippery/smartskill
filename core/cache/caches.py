from django.core.cache import cache

from apps.user.models import User


def get_user_cache_key(user_id):
    return f"user_data_{user_id}"


def get_user_data(user_id):
    cache_key = get_user_cache_key(user_id)
    user_data = cache.get(cache_key)

    if user_data is None:
        # Fetch user data from the database if not cached
        try:
            user = User.objects.get(id=user_id)
            user_data = {"first_name": user.first_name, "last_name": user.last_name}
            set_user_data(user_id, user_data)
        except User.DoesNotExist:
            user_data = None

    return user_data


def set_user_data(user_id, user_data, timeout=60 * 15):
    cache_key = get_user_cache_key(user_id)
    cache.set(cache_key, user_data, timeout)


def invalidate_user_cache(user_id):
    cache_key = get_user_cache_key(user_id)
    cache.delete(cache_key)

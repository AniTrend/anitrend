from django.core.cache import cache


class CacheService:
    CACHE_TIMEOUT = 300  # 5 minutes

    @staticmethod
    def get_cached_data(cache_key):
        return cache.get(cache_key)

    def set_cached_data(self, cache_key, data):
        cache.set(cache_key, data, self.CACHE_TIMEOUT)

    def refresh_cache(self, cache_key, refresh_function):
        # Use a caching lock to prevent concurrent updates
        with cache.lock(f"{cache_key}_lock"):
            fresh_data = refresh_function()  # Fetch fresh data from external API
            self.set_cached_data(cache_key, fresh_data)

from django.core.cache import cache
from datetime import  timedelta
import json

def enforce_rate_limit(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        from_param = body['from'] if body['from']  else  ''
        cache_key = f"{from_param}_request_count"
        request_count = cache.get(cache_key, 0)
        if request_count >= 3:
            return False  # Rate limit exceeded

        # Increment the request count and set it in the cache
        # cache.set(cache_key, request_count + 1, timedelta(days=1))
        cache.set(cache_key, request_count + 1, int(timedelta(days=1).total_seconds()))

    return True  # Request allowed within rate limit
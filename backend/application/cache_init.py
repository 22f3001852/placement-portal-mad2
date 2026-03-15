from flask_caching import Cache

cache = Cache()

def cache_init_app(app):
    cache.init_app(app)
    return cache

    
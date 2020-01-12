# -*- coding: utf-8 -*-
import redis

try:
    import bhcrjyApp.settings as settings
except ImportError:
    assert "The missing settings.py file or " \
           "REDIS_DATABASE configuration does not exist in settings.py"

# Find the stack on which we want to store the database connection.
# Starting with Flask 0.9, the _app_ctx_stack is the correct one,
# before that we need to use the _request_ctx_stack.
try:
    from flask import _app_ctx_stack as stack
except ImportError:
    from flask import _request_ctx_stack as stack


class RedisPool(object):
    """
    Generate a redis connection pool
    """

    def __init__(self, **redis_config):
        """
        param:
            redis_config: This is a dictionary object, KV of redis connection parameter.

            REDIS_DATABASE: This is a dictionary object, the KV of redis connection parameter.
                            Configure in settings file.

            self.redis_config: Saved redis configuration information.

            self.redis_pool: Connection pool of reids.
        """
        if redis_config:
            self.redis_pool = redis.ConnectionPool(redis_config)
        else:
            if settings.REDIS_DATABASE:
                redis_config = settings.REDIS_DATABASE
                self.redis_pool = redis.ConnectionPool(**redis_config)

            else:
                raise Exception('No redis configuration found.')
        self.redis_cfg = redis_config

    def healthInfo(self):
        """
        redisPool's health information
        """
        # TODO 待完善 Redis健康信息
        return {
            'pid': self.redis_pool.pid,
            'max_conn': self.redis_pool.max_connections,
        }


class Redis(object):
    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)
        pass

    def init_app(self, app):

        if hasattr(app, 'teardown_appcontext'):
            app.teardown_appcontext(self.teardown)
        else:
            app.teardown_request(self.teardown)
        print('[init_app]redisPool is ', redisPool.pid)

    def __connect(self):
        if redisPool:
            # print('[connect]redisPool is ', redisPool.max_connections)
            return redis.Redis(connection_pool=redisPool)
        else:
            raise Exception('<ERROR> RedisPool creation failed')

    def teardown(self, exc):
        ctx = stack.top
        if hasattr(ctx, 'redis_db'):
            # print('[teardown] redis_db link ', ctx.redis_db)
            # ctx.redis_db.close()
            pass

    @property
    def connection(self):
        ctx = stack.top
        if ctx is not None:
            if hasattr(ctx, 'redis_db'):
                return ctx.redis_db
            elif not hasattr(ctx, 'redis_db'):
                ctx.redis_db = self.__connect()
                # print('[create] redis_db link ', ctx.redis_db)
                return ctx.redis_db


redisPool = RedisPool().redis_pool  # redis_pool

redis_db = Redis()

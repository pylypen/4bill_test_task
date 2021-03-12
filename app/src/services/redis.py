from src import redis_connect as redis


class RedisService:
    def __init__(self):
        self._redis = redis

    def _get_key(self, key_name):
        """
        Get value by key
        :param key_name: string.
        :return: integer
        """
        # Check TTL for key
        if self._redis.ttl(key_name) < 0:
            self._redis.delete(key_name)
            return 0

        # Getting key
        key = self._redis.get(key_name)
        return int(key) if key is not None else 0

    def check_sum(self, amount, config):
        """
        Check sum
        :param amount: int.
        :param config: dict.
        :return: bool|tuple
        """
        for key in config:
            # Getting keys and values for sum
            values = [self._get_key(f"sec_{key}"), amount]

            # Removing None by filter
            values = list(filter(None, values))

            # Calculate sum
            sum_amount = sum(map(int, values))

            # Return error
            if sum_amount > int(config[key]):
                return (config[key], key)

        # All fine
        return False

    def append_amount(self, amount, query_number, config):
        """
        Append amount
        :param amount: int.
        :param query_number: int.
        :param config: dict.
        :return: bool
        """
        pipe = self._redis.pipeline()

        try:
            # watching query_number
            pipe.watch('query_number')

            # starting transaction and appending amount
            pipe.multi()
            for key in config:
                key_name = f"sec_{key}"
                
                if self._get_key(key_name):
                    # Increment if key exist
                    pipe.incrby(key_name, amount)
                else:
                    # Set if key not exist
                    pipe.setex(key_name, key, amount)

            pipe.execute()
            return True
        except:
            # rollback if something went wrong
            pipe.reset()
            return False

    def get_query_number(self):
        """
        Get and incr query_number
        :return: int
        """
        # Getting query_number
        query_number = self._redis.get('query_number')

        # Set query_number if not exist
        if not query_number:
            self._redis.set('query_number', 1)

        # Updating query_number and return
        return self._redis.incr('query_number')

    def flush_all(self):
        self._redis.fushall()

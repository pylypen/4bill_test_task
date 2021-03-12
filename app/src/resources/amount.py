import os
import time
from random import uniform
from flask_restful import Resource
from src.services.redis import RedisService
import ast


class Amount(Resource):
    _redis = RedisService()
    _attempts = 3000

    def get(self, amount=None):
        """
        Append amount by GET Method
        :param: amount: int
        :return: JSON
        """
        # checking amount
        if not amount:
            return {
                "error": "Oops, 'amount' was missing!"
            }, 422

        # checking config
        if not self._check_config():
            return {
                "error": "Oops, something went wrong!"
            }, 500

        # Trying add amount
        for _ in range(self._attempts):
            # Checking sum
            check_sum = self._redis.check_sum(amount, self._config)
            if check_sum:
                return {
                    "error": f"Amount limit exeeded ({check_sum[0]}/{check_sum[1]}sec)"
                }, 503

            # get query_number
            query_number = self._redis.get_query_number()

            # set new amount
            if self._redis.append_amount(amount, query_number, self._config):
                # All fine
                return {'result': 'OK'}, 201

            time.sleep(uniform(0.03, 0.05))

        # It can be happen only after ~2 min of start adding amount
        return {
            "error": "Oops, something went wrong while saving!"
        }, 500

    def _check_config(self):
        """
        Check and set config
        :return: bool
        """
        try:
            # Converting str to dict
            _config = ast.literal_eval(os.environ.get('AMOUNT_LIMITS_CONFIG'))

            # Checking type and length
            if type(_config) != dict or not len(_config):
                print("Config must be Dictionary and not empty!")
                return False

            # Checking 0's in config
            for c in _config:
                if not int(c) or not int(_config[c]):
                    print("Config can't contain 0's!")
                    return False

            self._config = _config
        except:
            return False

        return True

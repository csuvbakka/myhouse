import common.redis_lib as redis
import common.services as services
from pushover import Client


def _read_keys():
    with open('/run/secrets/pushover_keys') as f:
        user_key = f.readline().rstrip()
        api_token = f.readline().rstrip()
    return user_key, api_token


if __name__ == '__main__':
    user_key, api_token = _read_keys()
    client = Client(user_key, api_token=api_token)

    redis_connection = redis.create_connection()

    while (True):
        data = redis_connection.blpop(services.pushover, 0)
        client.send_message(data, title='test')

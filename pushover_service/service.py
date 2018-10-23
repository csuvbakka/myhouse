import common.redis_lib as redis
from pushover import Client


pushover_service = 'pushover'


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
        data = redis.get_event(redis_connection, pushover_service)
        client.send_message(data, title='test')

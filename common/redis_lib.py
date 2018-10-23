import redis
import time

def _read_password():
    with open('/run/secrets/redis_password') as f:
        return f.readline().rstrip()


def _create_connection():
    return redis.StrictRedis(host='redis', port=6379, db=0, password=_read_password(), decode_responses=True)


def _is_redis_available(connection):
    try:
        connection.ping()
    except redis.exceptions.ConnectionError as e:
        print(e)
        return False

    return True


def create_connection(n_tries=10):
    """Creates a connection to the redis server.

    Since the redis server needs some time to startup, the number of times this function tries to
    establish the connection can be specified.

    :param int n_tries: How many times we try to establish the connection.
    :return StrictRedis: The redis connection."""
    connection = _create_connection()
    for i in range(n_tries):
        if _is_redis_available(connection):
            return connection
        else:
            time.sleep(3)

    raise redis.exceptions.ConnectionError("Failed to connect to the redis server after {} tries.".format(n_tries))


def get_event(redis_connection, key):
    return redis_connection.blpop(key, 0)

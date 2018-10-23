import random
import string

secrets = ['flask_key', 'redis_password']

chars = string.ascii_lowercase + string.ascii_uppercase + string.digits

for secret in secrets:
    length = random.randint(128, 160)
    key = ''.join(random.choice(chars) for _ in range(length))

    with open(secret, 'w') as f:
        f.write(key)

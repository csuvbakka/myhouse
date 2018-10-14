import random

secrets = ['flask_key', 'redis_password', 'web_login_password']

for secret in secrets:
    length = random.randint(64, 128)
    key = ''
    for i in range(0, length):
        key += chr(random.randint(33, 126))

    with open(secret, 'w') as f:
        f.write(key)

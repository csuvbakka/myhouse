#!/bin/sh

cp /usr/local/etc/redis/redis.conf.orig /usr/local/etc/redis/redis.conf
password=`cat /run/secrets/redis_password`
sed -i "s/%PASSWORD%/$password/" /usr/local/etc/redis/redis.conf

exec "$@"

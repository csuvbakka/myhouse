FROM redis:stretch

COPY entrypoint.sh /
ENTRYPOINT [ "/entrypoint.sh" ]
CMD [ "redis-server", "/usr/local/etc/redis/redis.conf" ]

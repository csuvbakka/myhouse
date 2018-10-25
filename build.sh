#!/bin/env sh

cd pushover_service
docker build -t myhouse_pushover .
cd ..

cd redis
docker build -t myhouse_redis .
cd ..

cd web
docker build -t myhouse_flask .
cd ..

cd wlan_presence
docker build -t myhouse_wlan_presence .
cd ..

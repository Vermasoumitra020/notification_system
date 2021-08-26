#!/bin/bash

# run docker of kafka docker service
echo "[INFO] Starting Kafka Docker Service..."
docker-compose -f kafka_docker/local.yml up -d
echo "[INFO] Kafka Docker Service run successfully"

# run docker of notification data handler service
echo "[INFO] Starting Notification Data Handler Service..."
docker-compose -f notification_data_handler/local.yml up -d
echo "[INFO] Notification Data Handler Service run successfully"

# run docker of notification gateway service
echo "[INFO] Starting Notification Gateway Service..."
docker-compose -f notification_gateway/local.yml up -d
echo "[INFO] Notification Gateway Service run successfully"

# run docker of notification validator service
echo "[INFO] Starting Notification Gateway Service..."
docker-compose -f notification_validator/local.yml up -d
echo "[INFO] Notification Gateway Service run successfully"

# run docker of provider handler
echo "[INFO] Starting Provider Handler Service..."
docker-compose -f provider_handler/local.yml up -d
echo "[INFO] Provider Handler Service run successfully"


if [[ $1 == 'setup' ]]
then
  exec ./setup.sh
fi

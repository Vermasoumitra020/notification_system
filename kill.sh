#!/bin/bash

# stop docker of kafka docker service
ECHO "[INFO] Stopping Kafka Docker Service..."
docker-compose -f kafka_docker/local.yml stop
ECHO "[INFO] Kafka Docker Service stop successfully"

# stop docker of notification data handler service
ECHO "[INFO] Stopping Notification Data Handler Service..."
docker-compose -f notification_data_handler/local.yml stop
ECHO "[INFO] Notification Data Handler Service stop successfully"

# stop docker of notification gateway service
ECHO "[INFO] Stopping Notification Gateway Service..."
docker-compose -f notification_gateway/local.yml stop
ECHO "[INFO] Notification Gateway Service stop successfully"

# stop docker of notification validator service
ECHO "[INFO] Stopping Notification Gateway Service..."
docker-compose -f notification_validator/local.yml stop
ECHO "[INFO] Notification Gateway Service stop successfully"

# stop docker of provider handler
ECHO "[INFO] Stopping Provider Handler Service..."
docker-compose -f provider_handler/local.yml stop
ECHO "[INFO] Provider Handler Service stop successfully"

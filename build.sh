#!/bin/bash

# build docker of kafka docker service
echo "[INFO] Building Kafka Docker Service..."
docker-compose -f kafka_docker/local.yml build
echo "[INFO] Kafka Docker Service build successfully"

# build docker of notification data handler service
echo "[INFO] Building Notification Data Handler Service..."
docker-compose -f notification_data_handler/local.yml build
echo "[INFO] Notification Data Handler Service build successfully"

# build docker of notification gateway service
echo "[INFO] Building Notification Gateway Service..."
docker-compose -f notification_gateway/local.yml build
echo "[INFO] Notification Gateway Service build successfully"

# build docker of notification validator service
echo "[INFO] Building Notification Validator Service..."
docker-compose -f notification_validator/local.yml build
echo "[INFO] Notification Validator Service build successfully"

# build docker of provider handler
echo "[INFO] Building Provider Handler Service..."
docker-compose -f provider_handler/local.yml build
echo "[INFO] Provider Handler Service build successfully"

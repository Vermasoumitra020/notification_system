#!/bin/bash

# run docker of kafka docker service
ECHO "[INFO] Starting Kafka Docker Service..."
docker-compose -f kafka_docker/local.yml up -d
ECHO "[INFO] Kafka Docker Service run successfully"

# run docker of notification data handler service
ECHO "[INFO] Starting Notification Data Handler Service..."
docker-compose -f notification_data_handler/local.yml up -d
ECHO "[INFO] Notification Data Handler Service run successfully"

# run docker of notification gateway service
ECHO "[INFO] Starting Notification Gateway Service..."
docker-compose -f notification_gateway/local.yml up -d
ECHO "[INFO] Notification Gateway Service run successfully"

# run docker of notification validator service
ECHO "[INFO] Starting Notification Gateway Service..."
docker-compose -f notification_validator/local.yml up -d
ECHO "[INFO] Notification Gateway Service run successfully"

# run docker of provider handler
ECHO "[INFO] Starting Provider Handler Service..."
docker-compose -f provider_handler/local.yml up -d
ECHO "[INFO] Provider Handler Service run successfully"

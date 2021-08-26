#!/bin/bash

# setup
./run.sh

# run coverage of notification data handler service
echo "[INFO] Starting Notification Data Handler Service coverage..."
docker-compose -f notification_data_handler/local.yml run --rm django coverage run -m pytest
docker-compose -f notification_data_handler/local.yml run --rm django coverage report -m
echo "[INFO] Notification Data Handler Service coverage run successfully"

# run coverage of notification gateway service
echo "[INFO] Starting Notification Gateway Service coverage..."
docker-compose -f notification_gateway/local.yml run --rm django coverage run -m pytest
docker-compose -f notification_gateway/local.yml run --rm django coverage report -m
echo "[INFO] Notification Gateway Service coverage run successfully"

# run coverage of notification validator service
echo "[INFO] Starting Notification Validator Service coverage..."
docker-compose -f notification_validator/local.yml run --rm django coverage run -m pytest
docker-compose -f notification_validator/local.yml run --rm django coverage report -m
echo "[INFO] Notification Validator Service coverage run successfully"

# run coverage of provider handler
echo "[INFO] Starting Provider Handler Service coverage..."
docker-compose -f provider_handler/local.yml run --rm django coverage run -m pytest
docker-compose -f provider_handler/local.yml run --rm django coverage report -m
echo "[INFO] Provider Handler Service coverage run successfully"

# teardown
./kill.sh

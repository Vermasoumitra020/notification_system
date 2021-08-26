#!/bin/bash

# setup
./run.sh

# run tests of notification data handler service
echo "[INFO] Starting Notification Data Handler Service tests..."
docker-compose -f notification_data_handler/local.yml run --rm django pytest
echo "[INFO] Notification Data Handler Service tests run successfully"

# run tests of notification gateway service
echo "[INFO] Starting Notification Gateway Service tests..."
docker-compose -f notification_gateway/local.yml run --rm django pytest
echo "[INFO] Notification Gateway Service tests run successfully"

# run tests of notification validator service
echo "[INFO] Starting Notification Validator Service tests..."
docker-compose -f notification_validator/local.yml run --rm django pytest
echo "[INFO] Notification Validator Service tests run successfully"

# run tests of provider handler
echo "[INFO] Starting Provider Handler Service tests..."
docker-compose -f provider_handler/local.yml run --rm django pytest
echo "[INFO] Provider Handler Service tests run successfully"

# teardown
./kill.sh

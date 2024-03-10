#!/bin/sh
pwd
# If the storage directory does not exist, create it
STORAGE_PATH="storage/"
if [ ! -f "$STORAGE_PATH" ]; then
    echo "Storage directory not found, creating an empty directory..."
    mkdir "$STORAGE_PATH"
fi

# If the DB does not already exist, create it
DB_PATH="backend/atto.db"
if [ ! -f "$DB_PATH" ]; then
    echo "SQLite database not found, creating an empty database."
    touch "$DB_PATH"
fi

# Run the Docker-Compose
docker-compose up --build
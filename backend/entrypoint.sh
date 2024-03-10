#!/bin/sh
echo "Applying Alembic migrations..."
alembic upgrade head

echo "Starting FastAPI application..."
exec "$@"
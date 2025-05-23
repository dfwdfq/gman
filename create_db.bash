#!/bin/bash
set -e

if [ -f ".env" ]; then
    export $(cat .env | grep -v '#' | awk '/=/ {print $1}')
else
    echo " .env file not found. Create it first using prepare.bash"
    exit 1
fi


echo "Waiting for psql to start..."
until pg_isready -h db -U "$POSTGRES_USER" -d "$POSTGRES_DB"; do
    sleep 2
done
echo "PostgreSQL is ready"

echo "Creating database '$POSTGRES_DB' if it doesn't exist..."
psql -h db -U "$POSTGRES_USER" -d postgres -tc "SELECT 1 FROM pg_database WHERE datname='$POSTGRES_DB'" | grep -q 1 || \
    psql -h db -U "$POSTGRES_USER" -d postgres -c "CREATE DATABASE \"$POSTGRES_DB\" OWNER \"$POSTGRES_USER\";" && \
    echo " Database '$POSTGRES_DB' created successfully"

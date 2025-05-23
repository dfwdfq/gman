#!/bin/bash
set -e

# Check if .env file exists
if [ -f ".env" ]; then
    echo ".env file already exists. Quitting..."
    exit 0
fi

echo "Generating .env file..."


read -p "Enter PostgreSQL username [default:bob]: " POSTGRES_USER
POSTGRES_USER=${POSTGRES_USER:-bob}

read -p "Enter PostgreSQL password [default: 12345]: " POSTGRES_PASSWORD
POSTGRES_PASSWORD=${POSTGRES_PASSWORD:-12345}

read -p "Enter PostgreSQL database name [default: db]: " POSTGRES_DB
POSTGRES_DB=${POSTGRES_DB:-db}


DATABASE_URL="postgresql+asyncpg://${POSTGRES_USER}:${POSTGRES_PASSWORD}@db:5432/${POSTGRES_DB}"


cat <<EOL > .env
POSTGRES_USER=$POSTGRES_USER
POSTGRES_PASSWORD=$POSTGRES_PASSWORD
POSTGRES_DB=$POSTGRES_DB
DATABASE_URL=$DATABASE_URL
EOL

echo ".env file created successfully!"

#!/bin/bash
# =============================================================================
# PostgreSQL initialization script
# Runs automatically on first container startup via /docker-entrypoint-initdb.d/
# Creates both the application database and the test database.
# Date: August 2026
# =============================================================================
set -e

echo "Initializing PostgreSQL databases..."

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    -- Create test database (application DB is already created by POSTGRES_DB env var)
    CREATE DATABASE capstone_test_db;

    -- Grant all privileges on both databases to the application user
    GRANT ALL PRIVILEGES ON DATABASE capstone_db TO $POSTGRES_USER;
    GRANT ALL PRIVILEGES ON DATABASE capstone_test_db TO $POSTGRES_USER;

    \echo 'Both databases created and privileges granted successfully.'
EOSQL

echo "PostgreSQL initialization complete."

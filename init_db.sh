#!/bin/bash
set -e

until psql -h dbpostgresql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c '\q'; do
  echo "Postgres is unavailable - sleeping"
  sleep 2
done

if psql -h dbpostgresql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c "SELECT 1 FROM diario_cuidador LIMIT 1;" 2>/dev/null; then
  echo "Database already initialized."
else
  echo "Initializing database..."
  psql -h dbpostgresql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -f /dump_file.sql
fi
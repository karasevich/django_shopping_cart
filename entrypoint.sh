#!/bin/sh

echo "--- Waiting for database to be ready..."
# Wait for the PostgreSQL container to accept connections on port 5432
# (This prevents errors where Django tries to connect before the DB is up)
while ! nc -z db 5432; do
  sleep 0.1
done
echo "--- PostgreSQL started successfully."

# 1. Apply database migrations
echo "--- Running database migrations..."
python manage.py migrate --noinput

# 2. Create Django Superuser if it does not exist
# We use the environment variables defined in .env
echo "--- Creating superuser (if not exists)..."
python manage.py createsuperuser --noinput \
    --username $DJANGO_SUPERUSER_USERNAME \
    --email $DJANGO_SUPERUSER_EMAIL || true
# The '|| true' ensures the script doesn't fail if the user already exists.

# 3. Start the Django web server
echo "--- Starting Django server..."
exec python manage.py runserver 0.0.0.0:8000
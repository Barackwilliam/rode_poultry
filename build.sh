#!/usr/bin/env bash
# Render build script for Rode Poultry Tanzania Limited
set -o errexit

pip install --upgrade pip
pip install -r requirements.txt

python manage.py collectstatic --noinput
python manage.py migrate

# Seed default categories (skips if already exist)
python manage.py seed_categories

# Compile translations
python manage.py compilemessages || true

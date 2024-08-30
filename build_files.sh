#!/bin/bash
echo "BUILD START"

# Install pip if not already installed
python3.9 -m ensurepip --upgrade
python3.9 -m pip install --upgrade pip

# Install dependencies
python3.9 -m pip install -r requirements.txt

# Collect static files
python3.9 manage.py collectstatic --noinput --output-dir staticfiles_build

echo "BUILD END"
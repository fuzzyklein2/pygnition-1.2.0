#!/usr/bin/env bash
# setup_venv.sh
# Sets up a .venv in the project root and installs pygnition in editable mode

set -e  # Exit on error
set -u  # Treat unset variables as errors
set -o pipefail

# Create virtual environment in .venv if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment in .venv..."
    py3.14 -m venv .venv
else
    echo "Virtual environment already exists in .venv"
fi

# Activate the virtual environment
source .venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install editable package
echo "Installing pygnition in editable mode..."
pip install -e .

# Install requirements if requirements.txt exists
if [ -f "requirements.txt" ]; then
    echo "Installing additional requirements..."
    pip install -r requirements.txt
fi

echo "Setup complete. Activate the venv with: source .venv/bin/activate"

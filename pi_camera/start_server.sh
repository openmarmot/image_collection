#!/bin/bash
# Script to set up a Python virtual environment and run the Pi Camera server

# Stop desktop media services that grab the camera
systemctl --user disable --now pipewire.socket pipewire-pulse.socket 2>/dev/null
systemctl --user stop pipewire wireplumber 2>/dev/null

# Define the virtual environment directory
VENV_DIR="venv"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python3 is not installed. Please install Python3 and try again."
    exit 1
fi

# Create a virtual environment if it doesn't exist
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment in $VENV_DIR..."
    python3 -m venv --system-site-packages $VENV_DIR
else
    echo "Virtual environment already exists in $VENV_DIR."
fi

# Activate the virtual environment
echo "Activating virtual environment..."
source $VENV_DIR/bin/activate

# Upgrade pip in the virtual environment
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Run the existing Python script
echo "Running program..."
python app.py

# Deactivate the virtual environment
echo "Deactivating virtual environment..."
deactivate

echo "Virtual environment setup and program execution complete."
echo "To reactivate the virtual environment later, run: source $VENV_DIR/bin/activate"

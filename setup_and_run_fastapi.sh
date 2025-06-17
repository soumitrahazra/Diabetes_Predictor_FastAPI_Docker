#!/bin/bash

set -e  # Exit immediately if any command fails

PROJECT_DIR="$(pwd)"
PYTHON_VERSION="3.11.9"
VENV_DIR="venv"

# Step 1: Ensure pyenv is installed
if ! command -v pyenv &> /dev/null; then
    echo "pyenv not found. Please install pyenv first."
    echo "Visit: https://github.com/pyenv/pyenv#installation"
    exit 1
fi

# Step 2: Install Python 3.11.9 if not already installed
if ! pyenv versions --bare | grep -q "^$PYTHON_VERSION$"; then
    echo "Installing Python $PYTHON_VERSION via pyenv..."
    pyenv install $PYTHON_VERSION
else
    echo "Python $PYTHON_VERSION already installed."
fi

# Step 3: Set local Python version
pyenv local $PYTHON_VERSION

# Step 4: Create virtual environment if it doesn't exist
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment with Python $PYTHON_VERSION..."
    $HOME/.pyenv/versions/$PYTHON_VERSION/bin/python -m venv $VENV_DIR
else
    echo "Virtual environment already exists."
fi

# Step 5: Activate the virtual environment
source $VENV_DIR/bin/activate

# Step 6: Upgrade pip and install dependencies
echo "Upgrading pip and installing packages..."
pip install --upgrade pip
pip install fastapi uvicorn numpy pandas scikit-learn

# Step 7: Freeze requirements
pip freeze > requirements.txt
echo "requirements.txt updated."

#Step 8: If any requirements are missing
pip install -r "$PROJECT_DIR/requirements.txt"

#Step 9: Kill any existing uvicorn on port 8001
echo "Stopping existing uvicorn processes on port 8001 (if any)..."
lsof -ti:8001 | xargs kill -9 2>/dev/null

# Step 10: Run uvicorn in background with nohup
echo "Starting FastAPI server in background..."
nohup uvicorn app.main:app --host 127.0.0.1 --port 8001 > "$PROJECT_DIR/uvicorn.log" 2>&1 &

# Wait to ensure server is up
sleep 5

# Send curl test request
echo "Sending test curl request..."
curl -X POST "http://localhost:8001/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "age": 0.05,
    "sex": 0.05,
    "bmi": 0.06,
    "bp": 0.02,
    "s1": -0.04,
    "s2": -0.04,
    "s3": -0.02,
    "s4": -0.01,
    "s5": 0.01,
    "s6": 0.02
  }'

echo -e "\nDone! FastAPI server running at http://127.0.0.1:8001"


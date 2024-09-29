#!/bin/bash

# Check if python is installed
if ! command -v python3 &> /dev/null
then
    echo "Python3 could not be found. Please install it."
    exit
fi

# Check if pip is installed
if ! command -v pip &> /dev/null
then
    echo "pip could not be found. Please install it."
    exit
fi

# Get the directory of the current script
SCRIPT_DIR="$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Navigate to your project directory
cd "$SCRIPT_DIR"

# Install the Python requirements
pip install -r requirements.txt

# Alias 'task-cli' command to your Python script
echo "alias task-cli='python3 \"$(pwd)/task_tracker.py\"'" >> ~/.bashrc

# Reload the .bashrc file.
source ~/.bashrc
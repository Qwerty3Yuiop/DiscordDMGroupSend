#!/bin/bash

# --- Get the absolute path of the current script ---
# Use BASH_SOURCE for sourced scripts, fallback to $0 for executed scripts
if [ -n "${BASH_SOURCE[0]}" ]; then
    SCRIPT_PATH_RAW="${BASH_SOURCE[0]}"
else
    SCRIPT_PATH_RAW="$0"
fi

SCRIPT_PATH="$(readlink -f "$SCRIPT_PATH_RAW")"

SCRIPT_DIR="$(dirname "$SCRIPT_PATH")"

SERVER_DIR="$(dirname "$SCRIPT_DIR")/server"
PYTHON_SCRIPT="database/setup_db.py"
FULL_PYTHON_SCRIPT_PATH="$SERVER_DIR/$PYTHON_SCRIPT"

if [ ! -d "$SERVER_DIR" ]; then
    echo "Error: Server directory not found at $SERVER_DIR"
    exit 1
fi

if [ ! -f "$FULL_PYTHON_SCRIPT_PATH" ]; then
    echo "Error: Python script not found at $FULL_PYTHON_SCRIPT_PATH"
    exit 1
fi

echo "Attempting to run Python script from: $SERVER_DIR"

(cd "$SERVER_DIR" && python3 "$PYTHON_SCRIPT")

echo "Python script execution finished."
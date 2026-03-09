#!/bin/bash

# Author: Hindav
# LinkedIn: https://www.linkedin.com/in/hindav/
# Description: Setup script for AskMyDocs using uv for dependency management.

echo "Starting setup script..."

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "Error: 'uv' is not installed. Please install it first."
    echo "To install consistently: pip install uv"
    exit 1
fi
echo "uv is installed. Proceeding..."

# Function to run the application
run_app() {
    echo "Running the application with Streamlit interface..."
    # uv run handles virtual environment activation automatically
    uv run streamlit run src/app.py
    echo "Application stopped."
}

# Function to sync dependencies
sync_deps() {
    echo "Syncing dependencies using uv..."
    uv sync
    if [ $? -ne 0 ]; then
        echo "Error: Failed to sync dependencies."
        exit 1
    fi
    echo "Dependencies synced successfully."
}

# Ensure dependencies are synced at least once or check if .venv exists
if [ ! -d ".venv" ]; then
    echo "Virtual environment not found. Syncing dependencies..."
    sync_deps
fi

# Main menu
while true; do
    echo ""
    echo "AskMyDocs (Chat with Your Documents) - Maintained by Hindav"
    echo "==========================================================="
    echo "1. Run App (Streamlit)"
    echo "2. Sync/Update Dependencies"
    echo "3. Exit"
    read -p "Enter your choice (1-3): " choice

    case $choice in
        1)
            run_app
            ;;
        2)
            sync_deps
            ;;
        3)
            echo "Exiting..."
            exit 0
            ;;
        *)
            echo "Invalid choice. Please try again."
            ;;
    esac
done

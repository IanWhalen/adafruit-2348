#!/bin/sh
cd `dirname $0`

PYTHON=".venv/bin/python"


# # Optional: Clean up venv on exit (remove if you want to keep venv between runs)
# cleanup() {
#     if [ -d .venv ]; then
#         rm -rf .venv
#         echo "Virtual environment cleaned up"
#     fi
# }
# trap cleanup EXIT

# # Fix permissions if venv exists (safety net)
# if [ -d .venv ]; then
#     sudo chown -R "$USER:$USER" .venv
# fi

# Install dependencies using uv
echo "Installing dependencies..."
uv sync

$PYTHON -m PyInstaller --onefile --hidden-import="googleapiclient" src/main.py
tar -czvf dist/archive.tar.gz ./dist/main

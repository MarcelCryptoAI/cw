#!/bin/bash
set -e

BACKEND_DIR="backend"
FRONTEND_DIR="public_html"
PYTHON_ENV="venv"

function open_mac_terminal() {
  local CMD="$1"
  osascript <<END
tell application "Terminal"
    activate
    do script "$CMD"
end tell
END
}

echo "==[ Start backend (Flask/pybit) ]=="
open_mac_terminal 'cd '"$(pwd)/$BACKEND_DIR"' && source ../'"$PYTHON_ENV"'/bin/activate && python app.py'

echo "==[ Start frontend (public_html) ]=="
open_mac_terminal 'cd '"$(pwd)/$FRONTEND_DIR"' && python3 -m http.server 8000'

echo "==[ Beide servers gestart in eigen Terminal-vensters! ]=="

#!/bin/bash
# GPO Autofish - Development Mode for macOS/Linux
# Navigate to project root
cd "$(dirname "$0")/../.."

echo "========================================"
echo "  GPO Autofish - Development Mode"
echo "========================================"
echo ""
echo "This mode shows console output for debugging"
echo ""
echo "Default Hotkeys:"
echo "  F1 - Start/Pause/Resume Fishing"
echo "  F2 - Toggle Overlay"
echo "  F3 - Exit Program"
echo "  F4 - Toggle System Tray"
echo ""
echo "Note: Some hotkeys may require accessibility permissions"
echo ""

# Find Python 3
PYTHON_CMD=""
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    # Check if it's Python 3
    PYTHON_VERSION=$(python --version 2>&1 | awk '{print $2}')
    if [[ $PYTHON_VERSION == 3* ]]; then
        PYTHON_CMD="python"
    fi
fi

if [ -z "$PYTHON_CMD" ]; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.12 or 3.13"
    echo ""
    echo "Press Enter to exit..."
    read
    exit 1
fi

echo "Using Python: $PYTHON_CMD"
$PYTHON_CMD --version

# Check and activate virtual environment if it exists
if [ -f ".venv/bin/activate" ]; then
    echo ""
    echo "Activating virtual environment..."
    source .venv/bin/activate
    echo "✅ Virtual environment activated"
else
    echo ""
    echo "⚠️ Virtual environment not found - using system Python"
fi

echo ""
echo "Starting GPO Autofish..."
echo "========================================"
echo ""

# Run the application with output visible
$PYTHON_CMD src/main.py

echo ""
echo "========================================"
echo "Program ended. Press Enter to exit..."
read

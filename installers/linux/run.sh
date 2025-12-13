#!/bin/bash
# GPO Autofish - Run Script for macOS/Linux
# Navigate to project root
cd "$(dirname "$0")/../.."

echo "========================================"
echo "  GPO Autofish - Loading..."
echo "========================================"
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

# Run the application
$PYTHON_CMD src/main.py &

# Get the PID of the background process
APP_PID=$!

echo "✅ Macro started successfully! (PID: $APP_PID)"
echo ""
echo "To stop the application:"
echo "  • Use the Exit hotkey (F3 by default)"
echo "  • Or run: kill $APP_PID"
echo ""
echo "This window will close in 3 seconds..."
sleep 3

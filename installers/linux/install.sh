#!/bin/bash
# GPO Autofish - Installation Script for macOS/Linux
# Navigate to project root
cd "$(dirname "$0")/../.."

echo "========================================"
echo "  GPO Autofish - Easy Installation"
echo "  [macOS/Linux]"
echo "========================================"
echo ""

# Detect OS
OS_TYPE="$(uname -s)"
case "$OS_TYPE" in
    Darwin*)
        OS_NAME="macOS"
        ;;
    Linux*)
        OS_NAME="Linux"
        ;;
    *)
        OS_NAME="Unknown"
        ;;
esac

echo "Detected OS: $OS_NAME"
echo ""

# Check for Python 3
echo "[1/4] Checking Python installation..."
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
    PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | awk '{print $2}')
    echo "✓ Python $PYTHON_VERSION found"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
    PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | awk '{print $2}')
    # Check if it's Python 3
    if [[ $PYTHON_VERSION == 3* ]]; then
        echo "✓ Python $PYTHON_VERSION found"
    else
        echo "ERROR: Python 3 is required, but Python $PYTHON_VERSION was found"
        echo ""
        echo "Please install Python 3.12 or 3.13:"
        echo "  macOS: brew install python@3.12"
        echo "  Linux: sudo apt install python3.12 (or use your package manager)"
        exit 1
    fi
else
    echo "ERROR: Python is not installed"
    echo ""
    echo "Please install Python 3.12 or 3.13:"
    echo "  macOS: brew install python@3.12"
    echo "  Linux: sudo apt install python3.12 python3-pip"
    exit 1
fi

# Upgrade pip
echo ""
echo "[2/4] Upgrading pip to latest version..."
$PYTHON_CMD -m pip install --upgrade pip &> /dev/null
if [ $? -eq 0 ]; then
    echo "✓ Pip upgraded successfully"
else
    echo "WARNING: Could not upgrade pip, continuing anyway..."
fi

# Install packages
echo ""
echo "[3/4] Installing required packages..."
echo "Installing packages individually..."
echo "This may take several minutes..."
echo ""

FAILED_PACKAGES=""
FAILED_COUNT=0

# Function to install package
install_package() {
    local package=$1
    local display_name=${2:-$package}
    echo "Installing $display_name..."
    if $PYTHON_CMD -m pip install "$package" &> /dev/null; then
        echo "✓ $display_name installed"
        return 0
    else
        echo "✗ $display_name failed"
        FAILED_PACKAGES="$FAILED_PACKAGES $package"
        FAILED_COUNT=$((FAILED_COUNT + 1))
        return 1
    fi
}

# Install all packages
install_package "customtkinter"
install_package "darkdetect"
install_package "keyboard"
install_package "mss"
install_package "numpy"
install_package "pillow"
install_package "pynput"
install_package "pyautogui" "pyautogui (cross-platform mouse control)"
install_package "pystray"
install_package "requests"
install_package "opencv-python"
install_package "easyocr" "easyocr (this may take a while - 1GB+ download)"

# Check if we're on Linux and need additional dependencies
if [[ "$OS_NAME" == "Linux" ]]; then
    echo ""
    echo "Note for Linux users:"
    echo "  - You may need to install tkinter separately:"
    echo "    sudo apt install python3-tk (Debian/Ubuntu)"
    echo "    sudo dnf install python3-tkinter (Fedora)"
    echo "  - You may need to install additional dependencies for opencv:"
    echo "    sudo apt install libgl1-mesa-glx libglib2.0-0"
    echo "  - Keyboard library may require root privileges (sudo)"
fi

if [[ "$OS_NAME" == "macOS" ]]; then
    echo ""
    echo "Note for macOS users:"
    echo "  - You may need to grant Accessibility permissions"
    echo "  - Go to System Preferences > Security & Privacy > Privacy > Accessibility"
    echo "  - Add Terminal or your Python executable to the list"
fi

echo ""
if [ $FAILED_COUNT -gt 0 ]; then
    echo "⚠️ WARNING: $FAILED_COUNT package(s) failed to install"
    echo ""
    echo "Failed packages:$FAILED_PACKAGES"
    echo ""
    echo "TO FIX:"
    echo "  1. Make sure you're using Python 3.12 or 3.13"
    echo "  2. Check your internet connection"
    echo "  3. Install manually: $PYTHON_CMD -m pip install [package_name]"
    echo "  4. On Linux, you may need: sudo apt install python3-dev build-essential"
    echo ""
else
    echo "✓ All packages installed successfully!"
fi

# Verify installation
echo ""
echo "[4/4] Verifying installation..."
$PYTHON_CMD -c "import keyboard, pynput, mss, numpy, PIL" 2> /dev/null
if [ $? -eq 0 ]; then
    echo "✓ Core modules verified"
else
    echo "WARNING: Some core modules may not be properly installed"
    echo "The program may still work, but some features might be limited"
fi

$PYTHON_CMD -c "import customtkinter, pystray" 2> /dev/null
if [ $? -eq 0 ]; then
    echo "✓ UI modules verified"
else
    echo "NOTE: UI modules may have issues"
fi

echo ""
echo "========================================"
echo "  Installation Complete!"
echo "========================================"
echo ""
echo "To run GPO Autofish:"
if [[ "$OS_NAME" == "macOS" ]]; then
    echo "  • Run: ./installers/mac/run.sh"
    echo "  • Or: ./installers/mac/run_dev.sh (for debug mode)"
elif [[ "$OS_NAME" == "Linux" ]]; then
    echo "  • Run: ./installers/linux/run.sh"
    echo "  • Or: ./installers/linux/run_dev.sh (for debug mode)"
fi
echo "  • Or: $PYTHON_CMD src/main.py"
echo ""
echo "Press Enter to exit..."
read

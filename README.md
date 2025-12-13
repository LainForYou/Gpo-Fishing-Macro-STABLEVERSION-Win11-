[![Discord](https://img.shields.io/badge/Discord-Join%20Server-7289da?style=for-the-badge&logo=discord&logoColor=white)](https://discord.gg/unPZxXAtfb)

# 🎣 GPO Autofish - GUIDE (Windows, macOS, Linux)

**💬 Join our Discord server:** https://discord.gg/unPZxXAtfb

## What is this?

This is the **open-source version** of the GPO fishing macro that everyone uses. Unlike the closed-source version that gets flagged as a virus and isn't trustworthy, this version is:

- ✅ **Fully open source** - You can see and verify all the code
- ✅ **No viruses** - Clean, transparent, and safe
- ✅ **Improved** - Better features and reliability
- ✅ **Community-driven** - Open for contributions and review
- ✅ **Cross-platform** - Works on Windows, macOS, and Linux

The original closed-source macro is sketchy and often flagged by antivirus software because you can't verify what it's actually doing. This open-source version solves that problem.

**🛡️ Concerned about safety? Read [IS_IT_A_VIRUS.md](IS_IT_A_VIRUS.md) for more information.**

---

**Features:**

- **🎣 Fishing System** - Automatic fish detection and tracking with PD controller
- **🍎 Devil Fruit Detection** - OCR-powered detection of devil fruit drops with keyword matching
- **🌟 Fruit Spawn Alerts** - Detects and webhooks when devil fruits spawn with exact fruit name recognition
- **📦 Auto Fruit Storage** - Automatically stores devil fruits in inventory when detected
- **🔔 Discord Webhook Alerts** - Notifications for devil fruit catches and world spawns
- **🛒 Auto-Purchase** - Configurable bait purchasing
- **🎯 Auto Setup** - Zoom control and layout switching
- **🖥️ Modern UI** - Clean interface with collapsible sections
- **⚡ One-click installation** with `install.bat`
- **📊 Logging** - Dev mode for debugging
- **⌨️ Global hotkey support** (F1/F2/F3/F4)

## 🚀 Key Features

### 🍎 Devil Fruit Detection

- **OCR Detection**: Detects devil fruit drops using text recognition
- **Spawn Detection**: Detects when devil fruits spawn in the world (all 33 GPO fruits)
- **Fuzzy Matching**: Handles OCR errors with 70% similarity threshold
- **Auto Storage**: Automatically stores caught fruits
- **Webhook Alerts**: Discord notifications for catches and spawns

### 🎯 Auto Setup

- **Zoom Control**: Automatically zooms out/in for fishing
- **Layout Switching**: Switches between fishing bar and drop detection
- **Mouse Positioning**: Moves to casting position
- **Menu Clearing**: Right-clicks to clear menus

### 🛒 Auto-Purchase

- **Configurable Intervals**: Buy bait every X fish caught
- **Point System**: Set 4 custom points for purchase sequence
- **Auto-save**: Settings persist between sessions

### ⚡ Performance

- **Silent Mode**: Use `run.bat` for background operation
- **Dev Mode**: Use `run_dev.bat` for debugging with console output
- **Logging**: Level-based logging system
- **Modern UI**: Clean interface

## Installation

### ⚠️ Python Version Requirement

**IMPORTANT**: This application requires **Python 3.12 or 3.13**.

- ❌ **Python 3.14+ is NOT supported** due to compatibility issues with required packages (EasyOCR, PyTorch, etc.)
- ✅ **Recommended**: Python 3.13.0 (most stable)
- ✅ **Alternative**: Python 3.12.7

### 🪟 Windows Installation

**Download Python:**

- [Python 3.13.0](https://www.python.org/ftp/python/3.13.0/python-3.13.0-amd64.exe) (Recommended)
- [Python 3.12.7](https://www.python.org/ftp/python/3.12.7/python-3.12.7-amd64.exe) (Alternative)

**Easy Installation:**

1. **Install Python 3.12 or 3.13** (see links above) - Make sure to check "Add Python to PATH"
2. **Download the repository** as ZIP and extract it
3. **Double-click `installers\windows\install.bat`** - This will:
   - Check if Python is installed and verify version compatibility
   - Install all required packages automatically
   - Set everything up for you
4. **Run the application:**
   - **Standard mode:** Double-click `installers\windows\run.bat` (silent, no console)
   - **Dev mode:** Double-click `installers\windows\run_dev.bat` (with console for debugging)

### 🍎 macOS Installation

**Install Python:**

```bash
# Using Homebrew (recommended)
brew install python@3.12

# Or download from python.org
```

**Easy Installation:**

1. **Download the repository** and extract it
2. **Open Terminal** and navigate to the folder:
   ```bash
   cd path/to/gpo-fishing
   ```
3. **Make scripts executable:**
   ```bash
   chmod +x installers/mac/install.sh
   chmod +x installers/mac/run.sh
   chmod +x installers/mac/run_dev.sh
   ```
4. **Run installation:**
   ```bash
   ./installers/mac/install.sh
   ```
5. **Run the application:**
   - **Standard mode:** `./installers/mac/run.sh`
   - **Dev mode:** `./installers/mac/run_dev.sh`

**Important Notes for macOS:**

- You may need to grant **Accessibility permissions** for keyboard/mouse control
- Go to: System Preferences → Security & Privacy → Privacy → Accessibility
- Add Terminal or Python to the allowed apps list

### 🐧 Linux Installation

**Install Python:**

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3.12 python3-pip python3-tk python3-dev

# Fedora
sudo dnf install python3.12 python3-pip python3-tkinter python3-devel

# Arch
sudo pacman -S python python-pip tk
```

**Easy Installation:**

1. **Download the repository** and extract it
2. **Open Terminal** and navigate to the folder:
   ```bash
   cd path/to/gpo-fishing
   ```
3. **Make scripts executable:**
   ```bash
   chmod +x installers/linux/install.sh
   chmod +x installers/linux/run.sh
   chmod +x installers/linux/run_dev.sh
   ```
4. **Run installation:**
   ```bash
   ./installers/linux/install.sh
   ```
5. **Run the application:**
   - **Standard mode:** `./installers/linux/run.sh`
   - **Dev mode:** `./installers/linux/run_dev.sh`

**Additional Linux Dependencies:**

```bash
# Ubuntu/Debian - for OpenCV and screenshot support
sudo apt install libgl1-mesa-glx libglib2.0-0 scrot

# Note: keyboard library may require sudo privileges for global hotkeys
```

### 🔧 Manual Installation (All Platforms)

1. **Install Python 3.12 or 3.13**

   - Windows: Download from links above
   - macOS: `brew install python@3.12`
   - Linux: Use your package manager

2. **Clone or download this repository**

   ```bash
   git clone https://github.com/arielldev/gpo-autofish.git
   cd gpo-autofish
   ```

3. **Install platform-specific requirements**

   ```bash
   # Windows
   pip install -r requirements-windows.txt

   # macOS
   pip3 install -r requirements-mac.txt

   # Linux
   pip3 install -r requirements-linux.txt
   ```

4. **Run the application**

   ```bash
   # Windows
   python src/main.py

   # macOS/Linux
   python3 src/main.py
   ```

## 🎮 Quick Start Guide

### First Time Setup

1. **Install**: Navigate to `installers/<your-platform>/` and run the install script
2. **Launch**: Use `run.bat` / `run.sh` (silent mode) or `run_dev.bat` / `run_dev.sh` (with console for debugging)
3. **Configure Layouts**: Position overlays over fishing bar and drop detection areas
4. **Set Points**: Configure fruit storage points and auto-purchase coordinates
5. **Enable Features**: Turn on devil fruit storage, webhooks, and auto-purchase as needed

### Devil Fruit Storage Setup

1. **Enable Fruit Storage**: Check the "Enable Fruit Storage" option
2. **Set Fruit Key**: Choose which inventory slot (1-9) to store fruits
3. **Set Fruit Point**: Click to set where to click for fruit selection
4. **Set Rod Key**: Choose which slot (1-9) contains your fishing rod
5. **Set Bait Point**: Click to set where to click for bait selection

### Discord Webhook Setup

1. **Create Webhook**: In your Discord server → Channel Settings → Integrations → Webhooks
2. **Copy URL**: Paste the webhook URL in the bot settings
3. **Configure Alerts**:
   - 🍎 Devil Fruit Catch Alerts - Notifications when you catch a fruit while fishing
   - 🌟 Devil Fruit Spawn Alerts - Notifications when fruits spawn in the world (with exact fruit name)
   - 🐟 Fish Progress Updates - Regular progress reports
   - 🛒 Auto Purchase Alerts - Bait purchase confirmations
4. **Set Interval**: Choose how often to send fish progress updates

### Hotkeys

- **F1**: Start/Stop fishing loop
- **F2**: Toggle layout overlay
- **F3**: Emergency stop and exit
- **F4**: Minimize to system tray
- **Note**: All hotkeys work without admin privileges

### Performance Tips

- **Long Sessions**: Use `run.bat` / `run.sh` for extended fishing sessions (runs silently in background)
- **Debugging**: Use `run_dev.bat` / `run_dev.sh` when you need to see console output or troubleshoot issues
- **Webhook Monitoring**: Use Discord alerts for fruit spawns and catches instead of watching console
- **OCR Optimization**: Ensure good lighting and clear text for better fruit detection
- **Spawn Detection**: The bot detects all 33 GPO devil fruits automatically using fuzzy matching

---

## 🔧 Troubleshooting

### Installation Issues

- **"Python not found"**: Download Python 3.12 or 3.13 from the links above and check "Add to PATH"
- **"Python 3.14+ not supported"**: Uninstall Python 3.14+ and install Python 3.13 or 3.12 instead
- **"pip not recognized"**: Reinstall Python with "Add to PATH" checked
- **Permission errors**: Right-click `install.bat` → "Run as administrator"
- **Package installation failures**: Ensure you're using Python 3.12 or 3.13, not 3.14+

### Runtime Issues

- **Hotkeys not working**:
  - Windows: Try running with administrator privileges
  - macOS: Grant Accessibility permissions in System Preferences
  - Linux: keyboard library may require sudo privileges
- **Fish detection failing**: Adjust overlay position over the blue fishing bar
- **Devil fruit not detected**: Check OCR setup and drop area positioning
- **Fruit spawns not detected**: Ensure drop layout covers the spawn message area
- **Auto-purchase failing**: Verify all 4 purchase points are set correctly
- **High CPU usage**: Use `run.bat` / `run.sh` for silent mode operation

### Devil Fruit Issues

- **Fruits not being stored**: Check if OCR detected the fruit in console logs
- **Storage sequence running without fruit**: Ensure OCR is working properly
- **Wrong inventory slot**: Verify fruit key setting matches your setup
- **Rod not switching back**: Check rod key and bait point configuration

### Performance Issues

- **Long sessions lagging**: Use `run.bat` / `run.sh` for silent background operation
- **Need console output**: Use `run_dev.bat` / `run_dev.sh` for debugging mode with full logging
- **Memory usage**: Standard mode automatically reduces memory footprint
- **OCR slow**: Install EasyOCR properly for faster text recognition
- **Spawn detection**: Works automatically for all 33 GPO fruits with fuzzy name matching

---

## 📁 Project Structure

The codebase has been refactored into a clean, modular structure:

```
src/
├── main.py              # Application entry point
├── gui.py               # Main GUI and UI components
├── fishing.py           # Fishing bot logic and devil fruit detection
├── overlay.py           # Overlay window management
├── layout_manager.py    # Layout switching and area management
├── zoom_controller.py   # Auto zoom control system
├── ocr_manager.py       # OCR text recognition for devil fruits
├── webhook.py           # Discord webhook integration
├── updater.py           # Auto-update system
├── settings.py          # Settings management
├── themes.py            # Theme system for UI customization
├── platform_adapter.py  # Cross-platform mouse/system abstraction
├── bait_manager.py      # Bait purchasing and inventory management
└── utils.py             # Utility classes

installers/
├── windows/             # Windows installation scripts (.bat)
├── mac/                 # macOS installation scripts (.sh)
└── linux/               # Linux installation scripts (.sh)
```

This modular structure makes the code:

- ✅ Easier to understand and maintain
- ✅ Better organized by functionality
- ✅ Simpler to extend with new features
- ✅ More testable and debuggable

### Modern UI with CustomTkinter

The application now uses **CustomTkinter** for a modern, professional look:

- Clean, modern interface with smooth animations
- Dark/Light theme support
- Better visual hierarchy and readability
- Professional-looking buttons and controls
- Improved user experience

## 🤝 Contributing

This is an open-source project! Feel free to:

- Report bugs and issues
- Suggest new features
- Submit pull requests
- Join our Discord community

**💬 Discord:** https://discord.gg/unPZxXAtfb

# GPO Autofish - Source Code Structure

This directory contains the refactored source code for GPO Autofish, organized into modular components.

## Python Version Requirement

**IMPORTANT**: This application requires **Python 3.12 or 3.13 only**.

- ❌ Python 3.14+ is NOT supported due to package compatibility issues
- ✅ Use Python 3.13.0 (recommended) or Python 3.12.7

## File Structure

- `main.py` - Entry point for the application
- `gui.py` - Main GUI class and UI components
- `fishing.py` - Fishing bot logic and auto-purchase system
- `platform_adapter.py` - Cross-platform abstraction for mouse and keyboard (Windows/Mac/Linux)
- `overlay.py` - Overlay window management
- `webhook.py` - Discord webhook notifications
- `updater.py` - Auto-update functionality
- `settings.py` - Settings management (save/load/presets)
- `utils.py` - Utility classes (ToolTip, CollapsibleFrame)

## Cross-Platform Support

The application uses `platform_adapter.py` to provide unified keyboard and mouse control:

- **Windows**: Uses `keyboard` library for hotkeys
- **Mac/Linux**: Uses `pynput` library (no admin/sudo privileges required!)
- **F1-F4 keys**: Fully supported on all platforms without crashes
- **Hotkey rebinding**: Works safely on all platforms

## Running the Application

From the project root directory:

**Development mode (with console):**

```
python src/main.py
```

or use the batch file:

```
run_dev.bat
```

**Silent mode (no console):**

```
pythonw src/main.py
```

or use the batch file:

```
run.bat
```

## Building Executable

Use the provided batch file:

```
MakeItExe.bat
```

This will create a standalone executable in the `dist/` folder.

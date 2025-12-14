"""
Cross-platform abstraction layer for system-specific operations.
Provides unified interface for mouse control, keyboard events, and system integration
across Windows, macOS, and Linux.
"""

import platform
import sys
import time
from typing import Tuple, Literal, Callable, Optional

# Determine the current operating system
SYSTEM = platform.system()  # 'Windows', 'Darwin' (macOS), 'Linux'


class MouseController:
    """
    Unified mouse control interface that works across Windows, macOS, and Linux.
    
    On Windows: Uses win32api for precise, low-level mouse control
    On macOS/Linux: Uses PyAutoGUI as a cross-platform fallback
    """
    
    def __init__(self):
        self.system = SYSTEM
        
        if self.system == "Windows":
            try:
                import win32api
                import win32con
                self._win32api = win32api
                self._win32con = win32con
                self._backend = "win32"
            except ImportError:
                print("Warning: pywin32 not found on Windows. Falling back to PyAutoGUI.")
                self._init_pyautogui()
        else:
            # macOS (Darwin) and Linux use PyAutoGUI
            self._init_pyautogui()
    
    def _init_pyautogui(self):
        """Initialize PyAutoGUI backend for cross-platform support."""
        try:
            import pyautogui
            self._pyautogui = pyautogui
            # Disable PyAutoGUI's failsafe (moving mouse to corner stops execution)
            self._pyautogui.FAILSAFE = False
            # Set minimal pause between PyAutoGUI calls for performance
            self._pyautogui.PAUSE = 0.01
            self._backend = "pyautogui"
        except ImportError:
            print("ERROR: PyAutoGUI is required for Mac/Linux support.")
            print("Install it with: pip install pyautogui")
            sys.exit(1)
    
    def get_screen_size(self) -> Tuple[int, int]:
        """
        Get the screen dimensions.
        
        Returns:
            Tuple[int, int]: (width, height) in pixels
        """
        if self._backend == "win32":
            width = self._win32api.GetSystemMetrics(0)  # SM_CXSCREEN
            height = self._win32api.GetSystemMetrics(1)  # SM_CYSCREEN
            return (width, height)
        else:
            size = self._pyautogui.size()
            return (size.width, size.height)
    
    def move_to(self, x: int, y: int):
        """
        Move mouse cursor to absolute screen coordinates.
        
        Args:
            x: X coordinate (0 = left edge)
            y: Y coordinate (0 = top edge)
        """
        if self._backend == "win32":
            self._win32api.SetCursorPos((int(x), int(y)))
        else:
            self._pyautogui.moveTo(int(x), int(y), duration=0)
    
    def click_at(self, x: int, y: int, button: Literal['left', 'right'] = 'left', clicks: int = 1):
        """
        Click at specific screen coordinates.
        
        Args:
            x: X coordinate
            y: Y coordinate
            button: 'left' or 'right' mouse button
            clicks: Number of clicks (1 = single, 2 = double)
        """
        if self._backend == "win32":
            # Move to position first
            self._win32api.SetCursorPos((int(x), int(y)))
            time.sleep(0.01)  # Small delay for position to register
            
            # Perform clicks
            for _ in range(clicks):
                if button == 'left':
                    self._win32api.mouse_event(self._win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
                    time.sleep(0.01)
                    self._win32api.mouse_event(self._win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
                elif button == 'right':
                    self._win32api.mouse_event(self._win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0)
                    time.sleep(0.01)
                    self._win32api.mouse_event(self._win32con.MOUSEEVENTF_RIGHTUP, 0, 0, 0, 0)
                
                if clicks > 1:
                    time.sleep(0.05)  # Delay between multiple clicks
        else:
            self._pyautogui.click(int(x), int(y), clicks=clicks, button=button)
    
    def mouse_down(self, button: Literal['left', 'right'] = 'left'):
        """
        Press and hold mouse button at current position.
        
        Args:
            button: 'left' or 'right' mouse button
        """
        if self._backend == "win32":
            if button == 'left':
                self._win32api.mouse_event(self._win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
            elif button == 'right':
                self._win32api.mouse_event(self._win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0)
        else:
            self._pyautogui.mouseDown(button=button)
    
    def mouse_up(self, button: Literal['left', 'right'] = 'left'):
        """
        Release mouse button at current position.
        
        Args:
            button: 'left' or 'right' mouse button
        """
        if self._backend == "win32":
            if button == 'left':
                self._win32api.mouse_event(self._win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
            elif button == 'right':
                self._win32api.mouse_event(self._win32con.MOUSEEVENTF_RIGHTUP, 0, 0, 0, 0)
        else:
            self._pyautogui.mouseUp(button=button)
    
    def scroll(self, clicks: int):
        """
        Scroll mouse wheel.
        
        Args:
            clicks: Number of scroll clicks (positive = up/away, negative = down/toward)
        """
        if self._backend == "win32":
            # Win32: WHEEL_DELTA = 120 per notch
            # Positive values scroll up (away from user), negative scroll down (toward user)
            wheel_delta = clicks * 120
            self._win32api.mouse_event(
                self._win32con.MOUSEEVENTF_WHEEL,
                0, 0,
                wheel_delta,
                0
            )
        else:
            # PyAutoGUI: positive scrolls up, negative scrolls down
            self._pyautogui.scroll(clicks)
    
    def drag_to(self, x: int, y: int, button: Literal['left', 'right'] = 'left'):
        """
        Drag mouse from current position to target coordinates.
        
        Args:
            x: Target X coordinate
            y: Target Y coordinate
            button: Mouse button to hold during drag
        """
        if self._backend == "win32":
            # Manual drag implementation for win32
            self.mouse_down(button)
            time.sleep(0.01)
            self.move_to(x, y)
            time.sleep(0.01)
            self.mouse_up(button)
        else:
            self._pyautogui.dragTo(int(x), int(y), button=button, duration=0.1)
    
    def get_position(self) -> Tuple[int, int]:
        """
        Get current mouse cursor position.
        
        Returns:
            Tuple[int, int]: (x, y) coordinates
        """
        if self._backend == "win32":
            return self._win32api.GetCursorPos()
        else:
            pos = self._pyautogui.position()
            return (pos.x, pos.y)


class KeyboardController:
    """
    Unified keyboard control interface that works across Windows, macOS, and Linux.
    
    On Windows: Uses 'keyboard' library for low-level hotkey support
    On macOS/Linux: Uses 'pynput' library which doesn't require admin privileges
    """
    
    def __init__(self):
        self.system = SYSTEM
        self._hotkeys = {}  # Store registered hotkeys
        
        if self.system == "Windows":
            # Use keyboard library on Windows - it works without admin privileges
            try:
                import keyboard as kb
                self._keyboard = kb
                self._backend = "keyboard"
            except ImportError:
                print("ERROR: keyboard library is required for Windows.")
                print("Install it with: pip install keyboard")
                sys.exit(1)
        else:
            # Use pynput on macOS and Linux - doesn't require admin privileges
            try:
                from pynput import keyboard as pynput_kb
                self._pynput = pynput_kb
                self._backend = "pynput"
                self._listeners = []
                self._pressed_keys = set()
            except ImportError:
                print("ERROR: pynput is required for Mac/Linux.")
                print("Install it with: pip install pynput")
                sys.exit(1)
    
    def _normalize_key(self, key_string: str) -> str:
        """Normalize key string to consistent format across platforms."""
        # Convert to lowercase for consistency
        key_string = key_string.lower().strip()
        
        # Map common key variations
        key_map = {
            'esc': 'escape',
            'ctrl': 'control',
            'del': 'delete',
            'ins': 'insert',
            'pgup': 'page_up',
            'pgdn': 'page_down',
            'pageup': 'page_up',
            'pagedown': 'page_down',
        }
        
        return key_map.get(key_string, key_string)
    
    def _key_to_pynput(self, key_string: str):
        """Convert key string to pynput Key object."""
        key_string = self._normalize_key(key_string)
        
        # Handle function keys (f1-f20)
        if key_string.startswith('f') and len(key_string) > 1:
            fn_num_str = key_string[1:]
            if fn_num_str.isdigit():
                fn_num = int(fn_num_str)
                if 1 <= fn_num <= 20:
                    # Return the actual Key object for function keys
                    return getattr(self._pynput.Key, f'f{fn_num}')
        
        # Handle special keys - build dynamically to handle Mac/Linux differences
        special_keys = {
            'escape': self._pynput.Key.esc,
            'esc': self._pynput.Key.esc,
            'space': self._pynput.Key.space,
            'enter': self._pynput.Key.enter,
            'return': self._pynput.Key.enter,
            'tab': self._pynput.Key.tab,
            'backspace': self._pynput.Key.backspace,
            'up': self._pynput.Key.up,
            'down': self._pynput.Key.down,
            'left': self._pynput.Key.left,
            'right': self._pynput.Key.right,
            'control': self._pynput.Key.ctrl,
            'ctrl': self._pynput.Key.ctrl,
            'shift': self._pynput.Key.shift,
            'alt': self._pynput.Key.alt,
        }
        
        # Add keys that may not exist on all platforms (e.g., Insert not on Mac)
        optional_keys = {
            'delete': 'delete',
            'insert': 'insert',
            'home': 'home',
            'end': 'end',
            'page_up': 'page_up',
            'page_down': 'page_down',
            'alt_l': 'alt_l',
            'alt_r': 'alt_r',
            'cmd': 'cmd',
            'command': 'cmd',
        }
        
        for key_name, attr_name in optional_keys.items():
            try:
                key_attr = getattr(self._pynput.Key, attr_name, None)
                if key_attr is not None:
                    special_keys[key_name] = key_attr
            except AttributeError:
                pass  # Key not available on this platform
        
        if key_string in special_keys:
            return special_keys[key_string]
        
        # Single character keys
        if len(key_string) == 1:
            return self._pynput.KeyCode.from_char(key_string)
        
        return None
    
    def add_hotkey(self, key_combination: str, callback: Callable):
        """
        Register a hotkey with a callback function.
        
        Args:
            key_combination: Key combination string (e.g., 'f1', 'ctrl+c', 'shift+alt+s')
            callback: Function to call when hotkey is pressed
        """
        if self._backend == "keyboard":
            # Use keyboard library on Windows
            try:
                self._keyboard.add_hotkey(key_combination, callback)
                self._hotkeys[key_combination] = callback
                return True
            except Exception as e:
                print(f"Error adding hotkey {key_combination}: {e}")
                return False
        else:
            # Use pynput on Mac/Linux
            # Parse key combination
            keys = [k.strip() for k in key_combination.split('+')]
            target_keys = set()
            
            for key in keys:
                pynput_key = self._key_to_pynput(key)
                if pynput_key:
                    target_keys.add(pynput_key)
            
            if not target_keys:
                print(f"Warning: Could not parse key combination: {key_combination}")
                return False
            
            # Store the hotkey mapping
            self._hotkeys[key_combination] = {
                'callback': callback,
                'keys': target_keys
            }
            
            # Start listener if not already running
            if not self._listeners:
                self._start_pynput_listener()
            
            return True
    
    def _start_pynput_listener(self):
        """Start pynput keyboard listener for hotkey detection."""
        self._hotkey_triggered = {}  # Track which hotkeys have been triggered
        
        def on_press(key):
            # Add to pressed keys
            self._pressed_keys.add(key)
            
            # Check if any hotkey combination matches
            for hotkey_id, hotkey_data in self._hotkeys.items():
                if isinstance(hotkey_data, dict) and 'keys' in hotkey_data:
                    # Check if this exact hotkey combination is pressed
                    if hotkey_data['keys'].issubset(self._pressed_keys):
                        # Only trigger once per press (not on every key in combination)
                        if hotkey_id not in self._hotkey_triggered or not self._hotkey_triggered[hotkey_id]:
                            self._hotkey_triggered[hotkey_id] = True
                            try:
                                hotkey_data['callback']()
                            except Exception as e:
                                print(f"Error in hotkey callback: {e}")
        
        def on_release(key):
            # Remove from pressed keys
            self._pressed_keys.discard(key)
            
            # Reset hotkey triggered states when keys are released
            for hotkey_id, hotkey_data in self._hotkeys.items():
                if isinstance(hotkey_data, dict) and 'keys' in hotkey_data:
                    # If the released key was part of this hotkey, reset the trigger
                    if key in hotkey_data['keys']:
                        self._hotkey_triggered[hotkey_id] = False
        
        listener = self._pynput.Listener(on_press=on_press, on_release=on_release)
        listener.start()
        self._listeners.append(listener)
    
    def unhook_all(self):
        """Remove all registered hotkeys."""
        if self._backend == "keyboard":
            try:
                self._keyboard.unhook_all()
            except Exception as e:
                print(f"Error unhooking hotkeys: {e}")
        else:
            # Stop all pynput listeners
            for listener in self._listeners:
                try:
                    listener.stop()
                except Exception:
                    pass
            self._listeners.clear()
            self._pressed_keys = set()
            if hasattr(self, '_hotkey_triggered'):
                self._hotkey_triggered = {}
        
        self._hotkeys.clear()
    
    def press_and_release(self, key: str):
        """
        Press and release a key with error handling for Mac stability.
        
        Args:
            key: Key to press (e.g., 'a', 'enter', 'ctrl+c')
        """
        try:
            if self._backend == "keyboard":
                self._keyboard.press_and_release(key)
            else:
                # Use pynput controller with robust error handling
                controller = self._pynput.Controller()
                
                # Handle combinations like 'ctrl+a'
                if '+' in key:
                    keys = [k.strip() for k in key.split('+')]
                    pynput_keys = [self._key_to_pynput(k) for k in keys]
                    
                    # Press all keys
                    for pkey in pynput_keys:
                        if pkey:
                            controller.press(pkey)
                            time.sleep(0.02)  # Slightly longer delay on Mac
                    
                    # Release in reverse order
                    for pkey in reversed(pynput_keys):
                        if pkey:
                            controller.release(pkey)
                            time.sleep(0.02)
                else:
                    # Single key
                    pkey = self._key_to_pynput(key)
                    if pkey:
                        controller.press(pkey)
                        time.sleep(0.02)
                        controller.release(pkey)
                    else:
                        print(f"⚠️ Warning: Could not map key '{key}' for {self.system}")
        except Exception as e:
            print(f"❌ Keyboard error pressing '{key}': {e}")
            import traceback
            traceback.print_exc()
    
    def write(self, text: str):
        """
        Type text string with error handling for Mac stability.
        
        Args:
            text: Text to type
        """
        try:
            if self._backend == "keyboard":
                self._keyboard.write(text)
            else:
                controller = self._pynput.Controller()
                controller.type(text)
        except Exception as e:
            print(f"❌ Keyboard error writing '{text}': {e}")
            import traceback
            traceback.print_exc()


class SystemAdapter:
    """
    System-level operations abstraction.
    Handles DPI awareness and other OS-specific system settings.
    """
    
    def __init__(self):
        self.system = SYSTEM
    
    def set_dpi_awareness(self):
        """
        Set DPI awareness for high-resolution displays.
        Only applicable on Windows. macOS and Linux handle this automatically.
        """
        if self.system == "Windows":
            try:
                import ctypes
                # SetProcessDpiAwareness: 0=unaware, 1=system aware, 2=per-monitor aware
                ctypes.windll.shcore.SetProcessDpiAwareness(1)
            except Exception as e:
                print(f"Warning: Could not set DPI awareness: {e}")
        # macOS and Linux handle DPI automatically - no action needed
    
    def is_windows(self) -> bool:
        """Check if running on Windows."""
        return self.system == "Windows"
    
    def is_mac(self) -> bool:
        """Check if running on macOS."""
        return self.system == "Darwin"
    
    def is_linux(self) -> bool:
        """Check if running on Linux."""
        return self.system == "Linux"


# Global instances for easy import
mouse = MouseController()
keyboard = KeyboardController()
system = SystemAdapter()


# Convenience functions for backward compatibility
def get_screen_size() -> Tuple[int, int]:
    """Get screen dimensions (width, height)."""
    return mouse.get_screen_size()


def move_to(x: int, y: int):
    """Move mouse to coordinates."""
    mouse.move_to(x, y)


def click_at(x: int, y: int, button: str = 'left', clicks: int = 1):
    """Click at coordinates."""
    mouse.click_at(x, y, button, clicks)


def mouse_down(button: str = 'left'):
    """Press mouse button."""
    mouse.mouse_down(button)


def mouse_up(button: str = 'left'):
    """Release mouse button."""
    mouse.mouse_up(button)


def scroll(clicks: int):
    """Scroll mouse wheel."""
    mouse.scroll(clicks)


def set_dpi_awareness():
    """Set DPI awareness (Windows only)."""
    system.set_dpi_awareness()


if __name__ == "__main__":
    # Test the platform adapter
    print(f"Operating System: {SYSTEM}")
    print(f"Mouse Backend: {mouse._backend}")
    print(f"Keyboard Backend: {keyboard._backend}")
    print(f"Screen Size: {get_screen_size()}")
    print(f"Current Position: {mouse.get_position()}")
    print("\n✅ Platform adapter initialized successfully!")
    print("\nKeyboard Controller Notes:")
    print("- Windows: Uses 'keyboard' library")
    print("- Mac/Linux: Uses 'pynput' library (no admin privileges required)")
    print("- F1-F4 keys are fully supported on all platforms")
    print("- Hotkeys can be rebound safely without crashes")

"""
Cross-platform abstraction layer for system-specific operations.
Provides unified interface for mouse control, keyboard events, and system integration
across Windows, macOS, and Linux.
"""

import platform
import sys
import time
from typing import Tuple, Literal

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
    print(f"Screen Size: {get_screen_size()}")
    print(f"Current Position: {mouse.get_position()}")
    print("\nPlatform adapter initialized successfully!")

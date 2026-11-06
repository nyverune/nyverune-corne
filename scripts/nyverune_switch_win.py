#!/usr/bin/env python3
"""
Nyverune Profile Switcher for Windows (Python).
Monitors active foreground window via user32.dll ctypes and interfaces with QMK Raw HID.
"""

import ctypes
from ctypes import wintypes
import time
import sys

user32 = ctypes.windll.user32

def get_foreground_window_title() -> str:
    hwnd = user32.GetForegroundWindow()
    if not hwnd:
        return ""
    length = user32.GetWindowTextLengthW(hwnd)
    if length == 0:
        return ""
    buff = ctypes.create_unicode_buffer(length + 1)
    user32.GetWindowTextW(hwnd, buff, length + 1)
    return buff.value

def main():
    print("[*] Starting Nyverune Windows Profile Monitor...")
    last_profile = ""

    while True:
        try:
            title = get_foreground_window_title()
            is_nvim = any(k in title.lower() for k in ("nvim", "neovim", "vim"))
            profile = "Neovim" if is_nvim else "Everyday"

            if profile != last_profile:
                print(f"  [➔] Window: '{title[:45]}' -> Profile: {profile}")
                last_profile = profile

        except KeyboardInterrupt:
            break
        except Exception:
            pass

        time.sleep(0.4)

if __name__ == "__main__":
    main()

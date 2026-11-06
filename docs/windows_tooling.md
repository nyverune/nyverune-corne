# Windows Tooling & Profile Integration

This document outlines the profile switching tooling and automation capabilities on Windows for **Nyverune Corne**.

---

## 1. Overview

While Arch Linux is the primary target environment, developers frequently work across dual-boot or Windows workstations. The Windows tooling provides:
1. **Active Window Focus Detection:** Monitors Win32 foreground windows via `user32.dll` (`GetForegroundWindow` / `GetWindowText`).
2. **Native Windows Notifications:** Dispatches standard Windows Action Center Toast notifications when profiles transition.
3. **PowerShell & Python Implementations:** Dual native implementations without requiring heavy third-party software.

---

## 2. Running the Watcher

### Via PowerShell:
```powershell
.\scripts\windows_switch.ps1 watch
```

### Via Python:
```powershell
python scripts\nyverune_switch_win.py
```

---

## 3. Auto-Start on Windows Login

To run the watcher automatically in the background on Windows boot:

1. Press `Win + R`, type `shell:startup` and press Enter.
2. Create a shortcut to `powershell.exe -WindowStyle Hidden -ExecutionPolicy Bypass -File "\\wsl.localhost\archlinux\root\nyverune\nyverune-corne\scripts\windows_switch.ps1" watch`.
3. The watcher will run silently in the background with negligible RAM (< 15MB) and 0% CPU consumption.

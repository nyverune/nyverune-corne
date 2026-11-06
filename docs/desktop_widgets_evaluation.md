# Desktop Widgets Feasibility & Performance Evaluation

This document evaluates the feasibility, resource impact, and integration mechanisms for desktop status and profile-switching widgets on **Arch Linux** and **Windows**.

---

## 1. Arch Linux Widget Options

### A. Waybar Module (`custom/nyverune`)
- **Mechanism:** Waybar executes `waybar_profile.sh` on an interval or receives real-time signals via POSIX signal `SIGRTMIN+8`.
- **Latency:** Instantaneous (< 5ms to update bar indicator).
- **CPU / RAM Impact:** Practically 0% CPU, < 2MB memory footprint.
- **Visual Design:** Styled using the Nyverune palette:
  - Default / Everyday: `#A855F7` (Neon Violet icon) on `#181224` (Obsidian pill).
  - Neovim Active: `#FF5CB8` (Dream Pink icon) on `#21182B` (Elevated pill).
- **Feasibility:** **Extremely High (Recommended).**

```css
/* Nyverune Waybar CSS */
#custom-nyverune {
    background-color: #181224;
    color: #F6F0FC;
    border: 1px solid #7E22CE;
    border-radius: 8px;
    padding: 2px 10px;
}
#custom-nyverune.neovim {
    color: #FF5CB8;
    border-color: #FF5CB8;
}
```

### B. Interactive Rofi / Wofi Launcher Menu
- **Mechanism:** Bound to a global hotkey (e.g. `Super + F12`), opens a modal picker styled in Nyverune Void/Obsidian.
- **Latency:** Instantaneous.
- **Feasibility:** **Extremely High.**

---

## 2. Windows System Tray Feasibility

### Evaluation:
- **Mechanism:** Background Python script using `pystray` or PowerShell script leveraging `System.Windows.Forms.NotifyIcon`.
- **Findings:**
  - Highly feasible for dual-boot users.
  - Displays keyboard icon in taskbar tray.
  - Right-click menu allows instant switching: `Everyday` / `Neovim` / `Exit`.
  - Windows Action Center toast notifications provide immediate non-intrusive feedback.

---

## 3. Conclusions & Final Assessment

1. Desktop widgets provide high-value ergonomic feedback, ensuring the typist always knows the keyboard's exact layer state without looking down at the keyboard OLED.
2. In Wayland (Hyprland / Sway), combining the **Waybar module** with **Hyprland's socket2** event stream yields the smoothest, zero-polling experience.

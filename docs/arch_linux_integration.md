# Arch Linux Desktop Integration & Auto-Switching

This guide explains how to configure automatic, app-aware profile switching for **Nyverune Corne** on Arch Linux with **Hyprland** (native IPC & Lua configuration), **Sway**, or **X11**.

---

## 1. Overview

When developing on Arch Linux, workflow transitions rapidly between:
- **Neovim** (terminal / Neovide): Benefits from HJKL navigation, LSP chords, window splits.
- **Web Browser** (Firefox, Zen, Chrome, Brave) / Chat: Benefits from standard cursor arrows, clipboard chords, and browser navigation.

The `nyverune_switch.py` daemon connects directly to **Hyprland's `socket2.sock`** event stream. It switches the keyboard layout in real time over USB Raw HID (<1ms latency) with **0% CPU polling overhead**.

---

## 2. Requirements & Permissions

Add a udev rule to allow non-root users to communicate with the Raw HID interface:
```bash
sudo tee /etc/udev/rules.d/99-nyverune-hid.rules << 'EOF'
# Nyverune Corne Raw HID access for non-root users
KERNEL=="hidraw*", ATTRS{idVendor}=="4653", MODE="0666"
SUBSYSTEM=="hidraw", MODE="0666"
EOF

sudo udevadm control --reload-rules && sudo udevadm trigger
```

---

## 3. Hyprland Integration

### Hyprland Lua Configuration (`~/.config/hypr/hyprland.lua`):
```lua
-- Nyverune Corne Profile Keybinding
hyprland.bind("SUPER", "F12", function()
    hyprland.dispatch("exec", "python3 ~/nyverune/nyverune-corne/scripts/nyverune_switch.py toggle")
end)

-- Auto-start the daemon with the session
hyprland.dispatch("exec-once", "python3 ~/nyverune/nyverune-corne/scripts/nyverune_switch.py watch")
```

### Standard Hyprland Conf (`~/.config/hypr/hyprland.conf`):
```ini
# Toggle keyboard profile manually
bind = $mainMod, F12, exec, python3 ~/nyverune/nyverune-corne/scripts/nyverune_switch.py toggle

# Auto-start auto-switch daemon
exec-once = python3 ~/nyverune/nyverune-corne/scripts/nyverune_switch.py watch
```

---

## 4. Systemd User Service (Alternative)

To manage the daemon via systemd:

```bash
mkdir -p ~/.config/systemd/user/
cp scripts/nyverune-profile-daemon.service ~/.config/systemd/user/

systemctl --user daemon-reload
systemctl --user enable --now nyverune-profile-daemon.service
```

---

## 5. Manual CLI Usage

```bash
# Set Everyday profile
python3 scripts/nyverune_switch.py set everyday

# Set Neovim profile
python3 scripts/nyverune_switch.py set neovim

# Toggle between profiles
python3 scripts/nyverune_switch.py toggle
```

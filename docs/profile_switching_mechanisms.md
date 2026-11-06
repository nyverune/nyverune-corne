# QMK Runtime Profile Switching Mechanisms: Research & Analysis

This document investigates mechanisms for switching keyboard layouts and operational profiles at runtime on the **Corne (crkbd) 3x6+3** split keyboard without reflashing the microcontroller firmware.

---

## 1. The Core Challenge

A keyboard configuration project like **Nyverune Corne** defines multiple workflows:
- **Everyday:** Focused on standard document typing, browser shortcuts, and window managers.
- **Neovim:** Focused on modal editing, HJKL navigation, splits, and LSP diagnostics.

Traditionally, users switch profiles by flashing a different `.hex` or `.uf2` file. However, physical flashing requires rebooting the microcontrollers, putting the halves into bootloader mode, and interrupting workflow.

---

## 2. Investigated Switching Mechanisms

### Mechanism A: Persistent Default Layer Switching (`eeconfig`)
QMK includes native support for persistent default layers:
- **API Function:** `set_single_persistent_default_layer(_PROFILE_LAYER)`
- **Mechanism:** QMK writes the selected default base layer index into emulated EEPROM (or RP2040 flash). When the keyboard powers on or is replugged, it immediately boots into the saved profile.
- **Trigger Methods:**
  - Physical chord or key on the `_ADJUST` layer (e.g., Lower + Raise + `E` for Everyday, Lower + Raise + `N` for Neovim).
  - Tap-dance on a thumb key.
- **Latency:** Instantaneous (< 1 millisecond).
- **Pros:** Completely self-contained within firmware; works on any machine (Linux, Windows, macOS, Android) without installing software.
- **Cons:** Requires manual keypress on the keyboard; cannot automatically detect which application is focused on the PC.

---

### Mechanism B: Bidirectional Raw HID Protocol
QMK provides a raw bidirectional USB HID channel (`RAW_ENABLE = yes` in `rules.mk`):
- **API Function:** `raw_hid_receive(uint8_t *data, uint8_t length)`
- **Mechanism:** The host PC communicates with the keyboard using standard 32-byte HID packets over the existing USB cable. No virtual serial port or COM port driver is required.
- **Packet Structure:**
  - `data[0] = 0xAA` (Nyverune Magic Header)
  - `data[1] = 0x01` (Command: Switch Profile)
  - `data[2] = 0x00` (Everyday) or `0x01` (Neovim)
- **Host Software:** A lightweight Python or C daemon runs in user space on Arch Linux or Windows, monitoring the active window (e.g. Neovim vs. Firefox) and sending a 32-byte packet whenever the window focus changes.
- **Latency:** ~1–2 milliseconds (within one USB polling interval of 1000Hz).
- **Pros:** Full desktop integration, automatic profile switching, no manual toggling required.
- **Cons:** Requires desktop script/service running on host.

---

### Mechanism C: Dynamic Keymaps (VIA / VIAL)
- **Mechanism:** Stores the entire matrix in EEPROM and exposes a GUI configuration protocol.
- **Evaluation:** While convenient for visual remapping, VIA/VIAL compromises version control and reproducibility because keymaps are stored in mutable EEPROM rather than git-tracked C source code.
- **Decision:** Not recommended as the primary source of truth for Nyverune Corne, but compatible as a secondary layer inspection tool.

---

## 3. Comparison Matrix

| Feature | Firmware Reflashing | QMK Default Layer (Hardware) | Raw HID Desktop Daemon |
|---|---|---|---|
| **Interruption to typing** | High (5–10 seconds) | None (<1ms) | None (<1ms) |
| **Requires Host Software** | Yes (QMK CLI / UF2) | No (Fully standalone) | Yes (Lightweight daemon) |
| **App-Aware Auto-Switch** | Impossible | No | **Yes (Automatic)** |
| **Cross-Platform Portability** | OS-specific | **Universal** | Arch Linux & Windows |
| **EEPROM Persistence** | Yes | **Yes** | **Yes** |

---

## 4. Recommended Architectural Hybrid

For Nyverune Corne, the ideal design combines **Mechanism A and Mechanism B**:
1. **Firmware Level:** Implement unified firmware containing both Everyday and Neovim base/navigation layers with persistent default layer switching and a Raw HID command handler.
2. **Desktop Level:** Provide background daemons for Arch Linux (Hyprland / Sway / X11) and Windows that detect Neovim focus and send Raw HID packets automatically, with manual hardware hotkey fallback.

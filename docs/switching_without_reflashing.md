# Switching Profiles Without Reflashing Firmware

This document evaluates and specifies the unified firmware architecture enabling instant switching between **Everyday** and **Neovim** profiles.

---

## 1. Technical Evaluation

### Can a single firmware image hold both profiles?
**Yes, easily.**
- The Corne (crkbd) running on an **RP2040** has **2 Megabytes of onboard SPI flash memory**, while a full QMK split build takes less than 90 Kilobytes (under 5% capacity).
- Even on an ATmega32U4 (Pro Micro, 32KB flash), a unified build containing 6 layers and Raw HID consumes ~27KB, safely below the 28.6KB Caterina limit with LTO enabled (`LTO_ENABLE = yes`).

---

## 2. Firmware Integration Strategy

### Dual-Channel Switching:
1. **Hardware Hotkey (Self-Contained):**
   - Access the Adjust layer (`_ADJUST`) by holding both center thumb keys.
   - Pressing `E` switches immediately to Everyday.
   - Pressing `N` switches immediately to Neovim.
   - The selected profile is persisted into EEPROM and updates the OLED screen.

2. **Raw HID Desktop Channel (Zero Latency Automation):**
   - Enabling `RAW_ENABLE = yes` creates a 32-byte bidirectional USB channel.
   - OS-level background scripts send a 32-byte packet (`0xAA 0x01 0x02 <profile_id>`) in under **1 millisecond**.
   - No USB disconnect, no virtual serial COM port polling, no permissions friction.

---

## 3. OLED Visual Confirmation

When a profile switch occurs:
- The Left Master OLED screen updates its header:
  - `[EVRD]` for Everyday.
  - `[NVIM]` for Neovim.
- The Right Slave screen continues displaying the custom pixel-art **Nyverune Corne** logo.

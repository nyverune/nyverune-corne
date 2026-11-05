# Corne Hardware Testing & Verification Guide

This guide details the physical testing checklist and verification procedures for the Corne 3x6+3 keyboard when flashing Nyverune configurations.

---

## 1. Safety Warnings

> [!CAUTION]
> **NEVER** plug in or disconnect the TRRS cable connecting the left and right halves while the keyboard is connected to USB power! Doing so can create momentary short circuits that permanently damage the Pro Micro / RP2040 microcontrollers. Always disconnect the USB cable first.

---

## 2. Flashing Procedure

1. Connect the **left half** (master) via USB.
2. Put the controller into bootloader mode:
   - Double tap the hardware reset button on the PCB, or
   - Press the key combination mapped to `QK_BOOT` (Outer upper thumb row in `_ADJUST` layer).
3. Flash the firmware:
   ```bash
   qmk flash -kb crkbd/rev1 -km nyverune_everyday
   # or
   qmk flash -kb crkbd/rev1 -km nyverune_neovim
   ```
4. Disconnect USB, connect the **right half** via USB, put it into bootloader mode, and flash the same firmware.
5. Disconnect USB.
6. Connect the TRRS cable securely between the two halves.
7. Connect USB to the **left half**.

---

## 3. Physical Hardware Test Checklist

### A. Matrix Keypress Test
Open [QMK Configurator Test](https://test.qmk.fm/) or [keyboard-tester.com]:
- [ ] Verify all 42 keys register individual actuation without sticking.
- [ ] Confirm no ghosting or unintended double strokes occur.
- [ ] Verify diode orientation: Ensure no keypress on one half erroneously registers a row/column on the other.

### B. Spanish Character Verification (Host OS = Spanish ISO)
In a text editor, test the following key outputs:
- [ ] `ES_NTIL` key outputs lowercase `ñ` and uppercase `Ñ` (with Shift).
- [ ] `ES_ACUT` dead key generates acute vowels: `á`, `é`, `í`, `ó`, `ú`.
- [ ] `ES_ACUT` with Shift generates diaeresis vowels: `ä`, `ë`, `ï`, `ö`, `ü`.
- [ ] Punctuation keys output correctly: `,`, `.`, `-`, `;`, `:`, `_`.
- [ ] Inverted marks: `¿` and `¡`.

### C. Layer Transition Test
- [ ] Hold Left Center Thumb: Lower layer (`_NUM`) activates; verify numeric keypad `0-9` and function keys `F1-F12`.
- [ ] Hold Right Center Thumb: Raise layer (`_NAV` or `_VIM_NAV`) activates; verify cursor movement.
- [ ] Hold both Center Thumbs: Adjust layer (`_ADJUST`) activates; test volume keys (`VOLD`, `VOLU`, `MUTE`).
- [ ] Release thumb: Instantly returns to Base Spanish QWERTY.

### D. Combos Verification
- [ ] Press `J + K` together: Triggers `Escape`.
- [ ] Press `E + R` together: Triggers `[`.
- [ ] Press `U + I` together: Triggers `]`.
- [ ] Press `D + F` together: Triggers `{`.
- [ ] Press `H + J` together: Triggers `}`.

### E. Neovim Profile Test (Neovim Keymap)
In Neovim:
- [ ] From Base, press Right Center Thumb + `H/J/K/L` to move cursor smoothly.
- [ ] Test `<C-w>v` and `<C-w>s` splits via Vim Nav layer.
- [ ] Test `:w<CR>` quick save keycode.

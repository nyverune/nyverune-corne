# Firmware Compilation & Flashing Guide

This guide provides end-to-end instructions for compiling and flashing Nyverune Corne firmware on **Arch Linux**, **Ubuntu/Debian**, **WSL2**, and **Windows**.

---

## 1. Prerequisites

### Install QMK CLI
On **Arch Linux**:
```bash
sudo pacman -S qmk
# or via pip:
python3 -m pip install --user qmk
```

On **Debian / Ubuntu / WSL2**:
```bash
sudo apt update && sudo apt install -y git python3-pip gcc-avr avr-libc dfu-programmer
python3 -m pip install --user qmk
```

On **Windows**:
- Install [QMK MSYS](https://msys.qmk.fm/) or compile via WSL2.
- Alternatively, use [QMK Toolbox](https://github.com/qmk/qmk_toolbox/releases) for graphical flashing.

---

## 2. Linking Keymaps to QMK

Run the automated setup script from the repository root:
```bash
chmod +x firmware/setup_env.sh
./firmware/setup_env.sh
```

Or link the keymaps manually:
```bash
QMK_DIR="${HOME}/qmk_firmware"

# Link Everyday keymap
ln -sfn "$(pwd)/firmware/keymaps/everyday" "${QMK_DIR}/keyboards/crkbd/keymaps/nyverune_everyday"

# Link Neovim keymap
ln -sfn "$(pwd)/firmware/keymaps/neovim" "${QMK_DIR}/keyboards/crkbd/keymaps/nyverune_neovim"
```

---

## 3. Compilation Commands

### For RP2040 Controllers (Recommended):
```bash
# Everyday Profile
qmk compile -kb crkbd/rev1 -km nyverune_everyday -e CONVERT_TO=rp2040_ce

# Neovim Profile
qmk compile -kb crkbd/rev1 -km nyverune_neovim -e CONVERT_TO=rp2040_ce
```
*(Generates `.uf2` file. Also supports `-e CONVERT_TO=sparkfun_pm2040` for official Sparkfun boards).*

### For Classic ATmega32U4 Pro Micro:
```bash
# Everyday Profile
qmk compile -kb crkbd/rev1 -km nyverune_everyday

# Neovim Profile
qmk compile -kb crkbd/rev1 -km nyverune_neovim
```
*(Generates `.hex` file).*

---

## 4. Flashing the Keyboard

> [!CAUTION]
> **ALWAYS** disconnect the TRRS cable before plugging individual halves into USB for flashing! Once both halves are flashed, disconnect USB, connect the TRRS cable, and plug USB into the left half.

### Flashing via QMK CLI:

1. **Flash Left Half:**
   - Plug the **left half** into USB.
   - Run:
     ```bash
     qmk flash -kb crkbd/rev1 -km nyverune_everyday
     ```
   - When prompted (`Waiting for bootloader...`), double-tap the physical reset button on the left controller or press `QK_BOOT` in the Adjust layer.
   - Wait for flashing to complete (`Flash complete`).

2. **Flash Right Half:**
   - Unplug USB from the left half.
   - Plug the **right half** into USB.
   - Run the same flash command:
     ```bash
     qmk flash -kb crkbd/rev1 -km nyverune_everyday
     ```
   - Double-tap the physical reset button on the right controller.
   - Wait for flashing to complete.

3. **Reassemble:**
   - Unplug USB.
   - Connect the TRRS cable securely between left and right halves.
   - Plug USB into the **left half** (master).

---

## 5. Linux udev Rules (Arch Linux / Ubuntu)

If `qmk flash` reports permission errors accessing the USB device:
```bash
sudo cp ${HOME}/qmk_firmware/util/udev/50-qmk.rules /etc/udev/rules.d/
sudo udevadm control --reload-rules
sudo udevadm trigger
```

Ensure your user belongs to the `uucp` (Arch) or `dialout` (Debian) group:
```bash
sudo usermod -aG uucp $USER   # Arch Linux
sudo usermod -aG dialout $USER # Ubuntu / Debian
```

---

## 6. Microcontroller Specifics

| Controller | Bootloader Type | Flashing Method |
|---|---|---|
| **Pro Micro (ATmega32U4)** | Caterina | `qmk flash` or QMK Toolbox (.hex) |
| **Elite-C** | DFU | `dfu-programmer atmega32u4 flash` |
| **RP2040 (ProMicro RP2040)** | UF2 | Drag & drop `.uf2` into mounted drive |
| **nice!nano (ZMK only)** | UF2 | *Note: Nyverune Corne is configured for QMK* |


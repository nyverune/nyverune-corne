#!/usr/bin/env bash
# Setup script for QMK development environment on Arch Linux / Debian / WSL
set -euo pipefail

echo "=========================================="
echo "  Nyverune Corne - QMK Environment Setup  "
echo "=========================================="

# Check if QMK CLI is installed
if ! command -v qmk &> /dev/null; then
    echo "[!] QMK CLI is not installed."
    echo "[*] Installing QMK CLI via pip..."
    python3 -m pip install --user qmk
else
    echo "[✓] QMK CLI found: $(qmk --version)"
fi

# QMK repository location (default ~/qmk_firmware)
QMK_DIR="${HOME}/qmk_firmware"

if [ ! -d "${QMK_DIR}" ]; then
    echo "[*] Cloning QMK firmware repository..."
    git clone --recurse-submodules https://github.com/qmk/qmk_firmware.git "${QMK_DIR}"
else
    echo "[✓] QMK firmware repository already present at ${QMK_DIR}"
fi

# Link or copy nyverune keymaps into crkbd directory
KEYMAPS_DIR="${QMK_DIR}/keyboards/crkbd/keymaps"
CURRENT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "[*] Linking Nyverune keymaps into QMK crkbd directory..."
mkdir -p "${KEYMAPS_DIR}"

ln -sfn "${CURRENT_DIR}/keymaps/everyday" "${KEYMAPS_DIR}/nyverune_everyday"
ln -sfn "${CURRENT_DIR}/keymaps/neovim" "${KEYMAPS_DIR}/nyverune_neovim"

echo "[✓] Symlinks created:"
echo "    - ${KEYMAPS_DIR}/nyverune_everyday -> ${CURRENT_DIR}/keymaps/everyday"
echo "    - ${KEYMAPS_DIR}/nyverune_neovim   -> ${CURRENT_DIR}/keymaps/neovim"

echo ""
echo "Setup complete! You can now compile using:"
echo "  qmk compile -kb crkbd/rev1 -km nyverune_everyday"
echo "  qmk compile -kb crkbd/rev1 -km nyverune_neovim"


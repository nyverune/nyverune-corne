#!/usr/bin/env bash
# Interactive Rofi / Wofi menu for Nyverune Corne profile switching
# Styled to match Nyverune Palette

OPTIONS="1. Everyday Profile (General typing, navigation, clipboard)\n2. Neovim Profile (HJKL, splits, buffer & LSP shortcuts)"

CHOICE=$(echo -e "$OPTIONS" | rofi -dmenu -p "Nyverune Corne Profile" -theme-str '
  window { background-color: #100D16; border: 2px solid #7E22CE; border-radius: 12px; width: 550px; }
  mainbox { background-color: #100D16; padding: 15px; }
  element { background-color: #181224; text-color: #F6F0FC; border-radius: 8px; padding: 10px; margin: 4px; }
  element selected { background-color: #21182B; text-color: #A855F7; border: 1px solid #FF5CB8; }
')

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

case "$CHOICE" in
    *"Everyday"*)
        python3 "${SCRIPT_DIR}/nyverune_switch.py" set everyday
        ;;
    *"Neovim"*)
        python3 "${SCRIPT_DIR}/nyverune_switch.py" set neovim
        ;;
esac

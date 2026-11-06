#!/usr/bin/env bash
# Waybar custom module output script for Nyverune Corne profile
# Outputs JSON consumed by Waybar

PROFILE=$(python3 "$(dirname "$0")/nyverune_switch.py" get 2>/dev/null || echo "Everyday")

if [[ "$PROFILE" =~ [Nn]eovim ]]; then
    TEXT="󰌌 NVIM"
    TOOLTIP="Nyverune Corne: Neovim Profile (Active)\nClick to toggle"
    CLASS="neovim"
else
    TEXT="󰌌 EVRD"
    TOOLTIP="Nyverune Corne: Everyday Profile (Active)\nClick to toggle"
    CLASS="everyday"
fi

printf '{"text": "%s", "tooltip": "%s", "class": "%s"}\n' "$TEXT" "$TOOLTIP" "$CLASS"

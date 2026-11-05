#!/usr/bin/env python3
"""
Keymap and Layout Validation Script for Nyverune Corne
Validates Corne 3x6+3 (42 keys) matrix dimensions, JSON schemas,
and C keymap consistency across profiles.
"""

import json
import sys
from pathlib import Path

REQUIRED_KEYS = 42
ROOT_DIR = Path(__file__).resolve().parent.parent

def validate_json_layout(file_path: Path) -> bool:
    print(f"[*] Validating {file_path.relative_to(ROOT_DIR)}...")
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"  [!] JSON Parse Error: {e}")
        return False

    success = True
    layers = data.get("layers", [])
    if not layers:
        print("  [!] No layers found in layout definition.")
        return False

    for layer in layers:
        layer_id = layer.get("id")
        layer_name = layer.get("name")
        keys = layer.get("keys", [])
        key_count = len(keys)

        if key_count != REQUIRED_KEYS:
            print(f"  [X] Layer {layer_id} ({layer_name}): Expected {REQUIRED_KEYS} keys, found {key_count}!")
            success = False
        else:
            print(f"  [✓] Layer {layer_id} ({layer_name}): {key_count} keys verified.")

    return success

def validate_c_keymap(file_path: Path) -> bool:
    print(f"[*] Checking C keymap: {file_path.relative_to(ROOT_DIR)}...")
    if not file_path.is_file():
        print(f"  [X] File not found: {file_path}")
        return False

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Verify key headers and LAYOUT macro usage
    required_tokens = ["LAYOUT_split_3x6_3", "QMK_KEYBOARD_H", "layer_state_set_user"]
    for token in required_tokens:
        if token not in content:
            print(f"  [!] Missing expected token: {token}")
            return False

    print("  [✓] C Keymap structure verified.")
    return True

def main():
    print("==========================================")
    print("   Nyverune Corne Keymap Validation Suite  ")
    print("==========================================")

    all_passed = True
    layout_files = [
        ROOT_DIR / "layouts" / "everyday" / "layout.json",
        ROOT_DIR / "layouts" / "neovim" / "layout.json",
    ]

    for lf in layout_files:
        if not validate_json_layout(lf):
            all_passed = False

    c_keymaps = [
        ROOT_DIR / "firmware" / "keymaps" / "everyday" / "keymap.c",
        ROOT_DIR / "firmware" / "keymaps" / "neovim" / "keymap.c",
    ]

    for ck in c_keymaps:
        if not validate_c_keymap(ck):
            all_passed = False

    print("==========================================")
    if all_passed:
        print("[✓] ALL CHECKS PASSED: Keymaps are valid for Corne 3x6+3.")
        return 0
    else:
        print("[X] VALIDATION FAILED: Please fix errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""
Automatic Documentation Generator for Nyverune Corne.
Extracts layout schemas, layers, combos, and bindings from JSON definitions
and produces comprehensive, formatted Markdown documentation.
"""

import json
import os
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent

def friendly_label(key_code: str) -> str:
    clean = key_code.replace("KC_", "").replace("ES_", "")
    translations = {
        "BSPC": "Backspace (⌫)",
        "ENT": "Enter (⏎)",
        "TAB": "Tab (⇥)",
        "SPC": "Space (␣)",
        "ESC": "Escape (Esc)",
        "DEL": "Delete (Del)",
        "LSFT": "Left Shift",
        "RSFT": "Right Shift",
        "LGUI": "Super / Windows (◆)",
        "RALT": "AltGr (ISO)",
        "NTIL": "Ñ (Spanish)",
        "ACUT": "´ ¨ (Acute / Diaeresis)",
        "CCED": "Ç (C-cedilla)",
        "COMM": ", (Comma)",
        "DOT": ". (Period)",
        "MINS": "- (Hyphen)",
        "PLUS": "+ (Plus)",
        "ASTR": "* (Asterisk)",
        "SLSH": "/ (Slash)",
        "EQLS": "= (Equals)",
        "QUES": "? (Question)",
        "IQUE": "¿ (Inverted Question)",
        "IEXC": "¡ (Inverted Exclamation)",
        "EXCL": "! (Exclamation)",
        "DQOT": "\" (Quote)",
        "HASH": "# (Hash)",
        "DLLR": "$ (Dollar)",
        "PERC": "% (Percent)",
        "AMPR": "& (Ampersand)",
        "LPRN": "( (Left Paren)",
        "RPRN": ") (Right Paren)",
        "LBRC": "[ (Left Bracket)",
        "RBRC": "] (Right Bracket)",
        "LCBR": "{ (Left Brace)",
        "RCBR": "} (Right Brace)",
        "LABK": "< (Less than)",
        "RABK": "> (Greater than)",
        "PIPE": "| (Pipe)",
        "BSLS": "\\ (Backslash)",
        "TILD": "~ (Tilde)",
        "EURO": "€ (Euro)",
        "ATSN": "@ (At)",
        "COLN": ": (Colon)",
        "SCLN": "; (Semicolon)",
        "UNDS": "_ (Underscore)",
        "TRNS": "▽ (Transparent)",
        "NO": "· (No Key)",
        "QK_BOOT": "Bootloader Jump",
        "EE_CLR": "Clear EEPROM",
        "NK_TOGG": "Toggle NKRO",
        "BRID": "Brightness Down",
        "BRIU": "Brightness Up",
        "VOLD": "Volume Down",
        "VOLU": "Volume Up",
        "MUTE": "Mute Audio",
        "MPLY": "Play / Pause",
        "MNXT": "Next Track",
        "MPRV": "Previous Track",
        "VIM_SAVE": "Save Buffer (:w<CR>)",
        "VIM_QUIT": "Quit (:q<CR>)",
        "VIM_VSPLIT": "Vertical Split (<C-w>v)",
        "VIM_HSPLIT": "Horizontal Split (<C-w>s)",
        "VIM_BNEXT": "Next Buffer (:bnext<CR>)",
        "VIM_BPREV": "Prev Buffer (:bprev<CR>)",
        "VIM_DEF": "Go to Definition (gd)",
        "VIM_REF": "Go to References (gr)",
        "VIM_DIAGN": "Next Diagnostic (]d)",
        "VIM_DIAGP": "Prev Diagnostic ([d)",
        "VIM_HOVER": "Hover Doc (K)",
        "VIM_ACT": "Code Action (<spc>ca)",
        "VIM_REN": "Rename Symbol (<spc>rn)",
        "QUOT": "' ? (Apostrophe / Single Quote)",
        "APOS": "' (Apostrophe)",
        "CIRC": "^ (Caret)",
        "NOT": "¬ (Logical NOT)",
        "RM_TOGG": "RGB Matrix Toggle",
        "RM_NEXT": "Next RGB Matrix Effect",
        "RM_PREV": "Previous RGB Matrix Effect",
        "RM_HUEU": "RGB Hue Up (Cycle Color)",
        "RM_HUED": "RGB Hue Down",
        "RM_SATU": "RGB Saturation Up",
        "RM_SATD": "RGB Saturation Down",
        "RM_VALU": "RGB Brightness Up",
        "RM_VALD": "RGB Brightness Down",
        "RGB_NYV": "Nyverune Brand Color (Neon Violet #A855F7)",
        "PRF_EVR": "Switch to Everyday Profile",
        "PRF_NVM": "Switch to Neovim Profile",
        "PRF_TOGG": "Toggle Everyday / Neovim Profile",
        "SYM_CIRC": "^ (Literal Caret)",
        "SYM_GRV": "` (Literal Backtick)",
        "SYM_TILD": "~ (Literal Tilde)",
    }
    if key_code in translations:
        return translations[key_code]
    if clean in translations:
        return translations[clean]
    if key_code.startswith("LCTL_T("):
        inner = key_code[7:-1].replace("KC_", "")
        return f"Tap: {inner} | Hold: Left Ctrl"
    if key_code.startswith("MO("):
        layer_num = key_code[3:-1]
        layer_map = {"1": "Nav", "2": "Sym", "3": "Num", "4": "VimNav", "5": "VimCode", "6": "Adjust"}
        return f"Momentary Layer {layer_map.get(layer_num, layer_num)}"
    if key_code.startswith("LCTL("):
        inner = key_code[5:-1].replace("KC_", "")
        return f"Ctrl + {inner}"
    return clean

def generate_layout_doc(profile: str, data: dict) -> str:
    name = data.get("name", profile.capitalize())
    desc = data.get("description", "")
    layers = data.get("layers", [])

    lines = [
        f"# {name} — Layout & Keymap Documentation",
        "",
        f"> {desc}",
        "",
        "## Architecture Overview",
        "",
        "- **Base Typology:** Spanish QWERTY (native `Ñ`, accents and dead keys).",
        "- **Physical Matrix:** Corne split (3x6+3, 42 keys total).",
        f"- **Active Layers in this Profile:** {len(layers)} layers.",
        "",
        "---",
        ""
    ]

    for layer in layers:
        lid = layer["id"]
        lname = layer["name"]
        ltitle = layer.get("title", lname)
        ldesc = layer.get("description", "")
        keys = layer.get("keys", [])

        lines.append(f"## Layer {lid}: {lname} — {ltitle}")
        lines.append("")
        lines.append(f"*{ldesc}*")
        lines.append("")
        lines.append(f"![Diagram](../diagrams/{profile}/layer_{lid}_{lname.lower()}.svg)")
        lines.append("")
        lines.append("### Key Mapping Matrix")
        lines.append("")
        lines.append("| Position | Hand | Row | QMK Keycode | Primary Function |")
        lines.append("|---|---|---|---|---|")

        # Top 3 rows
        row_names = ["Top Row", "Home Row", "Bottom Row"]
        for r in range(3):
            # Left Hand (0 to 5)
            for c in range(6):
                idx = r * 12 + c
                code = keys[idx]
                lines.append(f"| L{r}{c} | Left | {row_names[r]} | `{code}` | {friendly_label(code)} |")
            # Right Hand (6 to 11)
            for c in range(6, 12):
                idx = r * 12 + c
                code = keys[idx]
                lines.append(f"| R{r}{c-6} | Right | {row_names[r]} | `{code}` | {friendly_label(code)} |")

        # Thumbs
        thumb_names = ["Outer Thumb", "Center Thumb", "Inner Thumb"]
        for i in range(3):
            code = keys[36 + i]
            lines.append(f"| LT{i} | Left | Thumb ({thumb_names[i]}) | `{code}` | {friendly_label(code)} |")
        thumb_right_names = ["Inner Thumb", "Center Thumb", "Outer Thumb"]
        for i in range(3):
            code = keys[39 + i]
            lines.append(f"| RT{i} | Right | Thumb ({thumb_right_names[i]}) | `{code}` | {friendly_label(code)} |")

        lines.append("")
        lines.append("---")
        lines.append("")

    return "\n".join(lines)

def main():
    print("[*] Generating automated layout documentation...")
    profiles = ["everyday", "neovim"]

    for profile in profiles:
        layout_path = ROOT_DIR / "layouts" / profile / "layout.json"
        if not layout_path.is_file():
            print(f"[!] Layout file not found: {layout_path}")
            continue

        with open(layout_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        doc_content = generate_layout_doc(profile, data)
        out_doc = ROOT_DIR / "docs" / f"{profile}_layout.md"

        with open(out_doc, "w", encoding="utf-8") as f:
            f.write(doc_content)

        print(f"  [✓] Generated documentation: {out_doc.relative_to(ROOT_DIR)}")

    print("[✓] Documentation generation completed.")

if __name__ == "__main__":
    main()


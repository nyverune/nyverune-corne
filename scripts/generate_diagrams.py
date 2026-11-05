#!/usr/bin/env python3
"""
Corne 3x6+3 SVG & Text Layout Diagram Generator for Nyverune Corne.
Generates publication-quality SVG diagrams and ASCII representations for every layer,
styled with the official Nyverune color palette.
"""

import json
import os
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent

# Official Nyverune Color Palette
NYVERUNE_PALETTE = {
    "void": "#100D16",         # Absolute background
    "obsidian": "#181224",     # Base surface / keycaps
    "elevated": "#21182B",     # Elevated panels / borders
    "neon_violet": "#A855F7",  # Primary identity / active keys
    "deep_violet": "#7E22CE",  # Deep hover / card borders
    "dream_pink": "#FF5CB8",   # Secondary accent / thumb layers
    "soft_lilac": "#D9C4FF",   # Subtitles / secondary labels
    "ghost_white": "#F6F0FC",  # High-contrast reading text
    "success": "#10B981",      # OK / test pass
    "warning": "#F59E0B",      # Warnings
    "danger": "#EF4444",       # Reset / bootloader
    "info": "#38BDF8",         # Navigation / cursor
}

# Thematic mapping for keyboard diagram components
COLORS = {
    "bg": NYVERUNE_PALETTE["void"],
    "surface": NYVERUNE_PALETTE["obsidian"],
    "border": NYVERUNE_PALETTE["elevated"],
    "text": NYVERUNE_PALETTE["ghost_white"],
    "text_muted": NYVERUNE_PALETTE["soft_lilac"],

    # Key type stylings
    "alpha": NYVERUNE_PALETTE["obsidian"],
    "alpha_border": "#2c1e40",
    "alpha_text": NYVERUNE_PALETTE["ghost_white"],

    "modifier": NYVERUNE_PALETTE["elevated"],
    "modifier_border": NYVERUNE_PALETTE["deep_violet"],
    "modifier_text": NYVERUNE_PALETTE["neon_violet"],

    "thumb_layer": NYVERUNE_PALETTE["elevated"],
    "thumb_layer_border": NYVERUNE_PALETTE["dream_pink"],
    "thumb_layer_text": NYVERUNE_PALETTE["dream_pink"],

    "nav": NYVERUNE_PALETTE["elevated"],
    "nav_border": NYVERUNE_PALETTE["info"],
    "nav_text": NYVERUNE_PALETTE["info"],

    "adjust": NYVERUNE_PALETTE["elevated"],
    "adjust_border": NYVERUNE_PALETTE["danger"],
    "adjust_text": NYVERUNE_PALETTE["danger"],

    "trans": "#130f1b",
    "trans_border": "#1c1626",
    "trans_text": "#443b54",
}

KEY_WIDTH = 56
KEY_HEIGHT = 56
KEY_GAP = 8
SPLIT_GAP = 60

def get_key_category(key_name: str) -> str:
    key_name = key_name.upper()
    if key_name in ("KC_TRNS", "KC_NO"):
        return "trans"
    if any(k in key_name for k in ("QK_BOOT", "EE_CLR", "RESET")):
        return "adjust"
    if any(k in key_name for k in ("MO(", "LT(", "OSL(")):
        return "thumb_layer"
    if any(k in key_name for k in ("CTL", "SFT", "ALT", "GUI", "LCTL", "LSFT", "LALT", "LGUI", "RALT", "RSFT")):
        return "modifier"
    if any(k in key_name for k in ("UP", "DOWN", "LEFT", "RGHT", "HOME", "END", "PGUP", "PGDN", "VIM_")):
        return "nav"
    return "alpha"

def friendly_label(key_code: str) -> str:
    clean = key_code.replace("KC_", "").replace("ES_", "")
    translations = {
        "BSPC": "⌫",
        "ENT": "⏎",
        "TAB": "⇥",
        "SPC": "␣",
        "ESC": "Esc",
        "DEL": "Del",
        "LSFT": "⇧ Shift",
        "RSFT": "Shift ⇧",
        "LGUI": "◆ Super",
        "RALT": "AltGr",
        "NTIL": "Ñ",
        "ACUT": "´ ¨",
        "CCED": "Ç",
        "COMM": ",",
        "DOT": ".",
        "MINS": "-",
        "PLUS": "+",
        "ASTR": "*",
        "SLSH": "/",
        "EQLS": "=",
        "QUES": "?",
        "IQUE": "¿",
        "IEXC": "¡",
        "EXCL": "!",
        "DQOT": "\"",
        "HASH": "#",
        "DLLR": "$",
        "PERC": "%",
        "AMPR": "&",
        "LPRN": "(",
        "RPRN": ")",
        "LBRC": "[",
        "RBRC": "]",
        "LCBR": "{",
        "RCBR": "}",
        "LABK": "<",
        "RABK": ">",
        "PIPE": "|",
        "BSLS": "\\",
        "TILD": "~",
        "EURO": "€",
        "ATSN": "@",
        "COLN": ":",
        "SCLN": ";",
        "UNDS": "_",
        "TRNS": "▽",
        "NO": "·",
        "QK_BOOT": "BOOT",
        "EE_CLR": "CLR",
        "NK_TOGG": "NKRO",
        "BRID": "Bri-",
        "BRIU": "Bri+",
        "VOLD": "Vol-",
        "VOLU": "Vol+",
        "MUTE": "Mute",
        "MPLY": "⏯",
        "MNXT": "⏭",
        "MPRV": "⏮",
        "VIM_SAVE": ":w",
        "VIM_QUIT": ":q",
        "VIM_VSPLIT": "<C-w>v",
        "VIM_HSPLIT": "<C-w>s",
        "VIM_BNEXT": ":bnext",
        "VIM_BPREV": ":bprev",
        "VIM_DEF": "gd",
        "VIM_REF": "gr",
        "VIM_DIAGN": "]d",
        "VIM_DIAGP": "[d",
        "VIM_HOVER": "K (doc)",
        "VIM_ACT": "<spc>ca",
        "VIM_REN": "<spc>rn",
    }
    if key_code in translations:
        return translations[key_code]
    if clean in translations:
        return translations[clean]
    if key_code.startswith("LCTL_T("):
        inner = key_code[7:-1].replace("KC_", "")
        return f"{inner}/Ctrl"
    if key_code.startswith("MO("):
        layer_num = key_code[3:-1]
        layer_map = {"1": "Nav", "2": "Sym", "3": "Num", "4": "VimNav", "5": "VimCode", "6": "Adjust"}
        return f"MO({layer_map.get(layer_num, layer_num)})"
    if key_code.startswith("LCTL("):
        inner = key_code[5:-1].replace("KC_", "")
        return f"C-{inner}"
    return clean

def render_svg_layer(profile_name: str, layer_data: dict) -> str:
    layer_name = layer_data["name"]
    layer_title = layer_data.get("title", layer_name)
    keys = layer_data["keys"]

    total_width = 12 * (KEY_WIDTH + KEY_GAP) + SPLIT_GAP + 60
    total_height = 4 * (KEY_HEIGHT + KEY_GAP) + 120

    svg_lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {total_width} {total_height}" width="{total_width}" height="{total_height}">',
        '  <defs>',
        '    <style>',
        f'      .title {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, monospace; font-size: 20px; font-weight: 700; fill: {NYVERUNE_PALETTE["ghost_white"]}; }}',
        f'      .subtitle {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, monospace; font-size: 13px; fill: {NYVERUNE_PALETTE["soft_lilac"]}; }}',
        '      .key-label {{ font-family: "JetBrains Mono", "Cascadia Code", Consolas, monospace; font-size: 13px; font-weight: 600; text-anchor: middle; dominant-baseline: middle; }}',
        '    </style>',
        f'    <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">',
        f'      <feDropShadow dx="0" dy="2" stdDeviation="3" flood-color="#7E22CE" flood-opacity="0.25"/>',
        f'    </filter>',
        '  </defs>',
        f'  <rect width="{total_width}" height="{total_height}" fill="{COLORS["bg"]}" rx="14" stroke="{NYVERUNE_PALETTE["elevated"]}" stroke-width="2" />',
        f'  <circle cx="24" cy="40" r="5" fill="{NYVERUNE_PALETTE["neon_violet"]}" />',
        f'  <text x="38" y="45" class="title">{profile_name.capitalize()} — Layer {layer_data["id"]}: {layer_name}</text>',
        f'  <text x="38" y="68" class="subtitle">{layer_title}: {layer_data.get("description", "")}</text>',
        '  <g transform="translate(30, 95)">'
    ]

    # Render Left Half (cols 0-5) and Right Half (cols 6-11)
    for r in range(3):
        for c in range(12):
            key_idx = r * 12 + c
            raw_key = keys[key_idx]
            category = get_key_category(raw_key)
            label = friendly_label(raw_key)

            x = c * (KEY_WIDTH + KEY_GAP)
            if c >= 6:
                x += SPLIT_GAP
            y = r * (KEY_HEIGHT + KEY_GAP)

            bg_col = COLORS.get(f"{category}", COLORS["alpha"])
            border_col = COLORS.get(f"{category}_border", COLORS["border"])
            text_col = COLORS.get(f"{category}_text", COLORS["text"])

            svg_lines.append(
                f'    <rect x="{x}" y="{y}" width="{KEY_WIDTH}" height="{KEY_HEIGHT}" rx="8" ry="8" fill="{bg_col}" stroke="{border_col}" stroke-width="1.6" filter="url(#glow)" />'
            )
            svg_lines.append(
                f'    <text x="{x + KEY_WIDTH/2}" y="{y + KEY_HEIGHT/2}" fill="{text_col}" class="key-label">{label}</text>'
            )

    # Thumbs (Row 3, 6 keys total)
    thumb_positions = [
        (3, 36), (4, 37), (5, 38),
        (6, 39), (7, 40), (8, 41)
    ]

    thumb_y = 3 * (KEY_HEIGHT + KEY_GAP) + 6
    for col_align, key_idx in thumb_positions:
        raw_key = keys[key_idx]
        category = get_key_category(raw_key)
        label = friendly_label(raw_key)

        x = col_align * (KEY_WIDTH + KEY_GAP)
        if col_align >= 6:
            x += SPLIT_GAP

        bg_col = COLORS.get(f"{category}", COLORS["thumb_layer"])
        border_col = COLORS.get(f"{category}_border", COLORS["thumb_layer_border"])
        text_col = COLORS.get(f"{category}_text", COLORS["thumb_layer_text"])

        svg_lines.append(
            f'    <rect x="{x}" y="{thumb_y}" width="{KEY_WIDTH}" height="{KEY_HEIGHT}" rx="8" ry="8" fill="{bg_col}" stroke="{border_col}" stroke-width="1.6" />'
        )
        svg_lines.append(
            f'    <text x="{x + KEY_WIDTH/2}" y="{thumb_y + KEY_HEIGHT/2}" fill="{text_col}" class="key-label">{label}</text>'
        )

    svg_lines.append('  </g>')
    svg_lines.append('</svg>')
    return "\n".join(svg_lines)

def generate_text_diagram(layer_data: dict) -> str:
    keys = layer_data["keys"]
    lines = []
    lines.append(f"### Layer {layer_data['id']}: {layer_data['name']} ({layer_data.get('title', '')})")
    lines.append("")
    lines.append("```")
    for r in range(3):
        left_half = " ".join(f"[{friendly_label(keys[r*12 + c]):^7}]" for c in range(6))
        right_half = " ".join(f"[{friendly_label(keys[r*12 + c]):^7}]" for c in range(6, 12))
        lines.append(f"{left_half}    {right_half}")

    lt = " ".join(f"[{friendly_label(keys[36 + i]):^7}]" for i in range(3))
    rt = " ".join(f"[{friendly_label(keys[39 + i]):^7}]" for i in range(3))
    spacer = " " * (3 * 10)
    lines.append(f"{spacer}{lt}    {rt}")
    lines.append("```")
    lines.append("")
    return "\n".join(lines)

def main():
    print("[*] Generating diagrams for Everyday and Neovim layouts with Nyverune palette...")
    profiles = ["everyday", "neovim"]

    for profile in profiles:
        layout_path = ROOT_DIR / "layouts" / profile / "layout.json"
        if not layout_path.is_file():
            print(f"[!] Layout file not found: {layout_path}")
            continue

        with open(layout_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        out_dir = ROOT_DIR / "diagrams" / profile
        out_dir.mkdir(parents=True, exist_ok=True)

        md_summary = [f"# {data.get('name', profile.capitalize())} — Visual Diagrams\n"]

        for layer in data.get("layers", []):
            layer_name = layer["name"].lower()
            svg_content = render_svg_layer(profile, layer)
            svg_file = out_dir / f"layer_{layer['id']}_{layer_name}.svg"

            with open(svg_file, "w", encoding="utf-8") as f:
                f.write(svg_content)
            print(f"  [✓] Generated SVG: {svg_file.relative_to(ROOT_DIR)}")

            text_dia = generate_text_diagram(layer)
            md_summary.append(f"## Layer {layer['id']}: {layer['name']}\n")
            md_summary.append(f"![Layer {layer['id']} Diagram](layer_{layer['id']}_{layer_name}.svg)\n")
            md_summary.append(text_dia)

        index_md = out_dir / "README.md"
        with open(index_md, "w", encoding="utf-8") as f:
            f.write("\n".join(md_summary))
        print(f"  [✓] Generated Diagram Summary: {index_md.relative_to(ROOT_DIR)}")

    print("[✓] Diagram generation workflow completed successfully.")

if __name__ == "__main__":
    main()

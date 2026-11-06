#!/usr/bin/env python3
"""
Corne 3x6+3 SVG & Text Layout Diagram Generator for Nyverune Corne.
Generates publication-quality SVG diagrams and ASCII representations for every layer,
styled with the official Nyverune color palette and two-tier keycap typography.
Strictly XML-escapes all strings (&, <, >, ", ') to ensure 100% W3C / browser SVG validity.
"""

import html
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

KEY_WIDTH = 62
KEY_HEIGHT = 60
KEY_GAP = 8
SPLIT_GAP = 64

def xml_escape(text: str) -> str:
    """Escapes XML entities (&, <, >, \", ') for valid SVG rendering."""
    return html.escape(str(text), quote=True)

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

def parse_key_labels(key_code: str) -> tuple[str, str]:
    """
    Returns (primary_label, sub_label) for elegant 2-tier keycap rendering.
    If sub_label is empty, primary_label is centered vertically.
    """
    clean = key_code.replace("KC_", "").replace("ES_", "")

    # Dual-role Mod-Tap keys
    if key_code.startswith("LCTL_T(") or key_code.startswith("RCTL_T("):
        inner = key_code[7:-1].replace("KC_", "")
        return (inner.capitalize(), "Ctrl")
    if key_code.startswith("LT("):
        parts = key_code[3:-1].split(",")
        layer_num = parts[0].strip()
        tap_key = parts[1].strip().replace("KC_", "") if len(parts) > 1 else ""
        return (tap_key, f"L{layer_num}")

    # Momentary layer switches
    if key_code.startswith("MO("):
        layer_num = key_code[3:-1]
        layer_names = {
            "1": "NAV",
            "2": "SYM",
            "3": "NUM",
            "4": "VIM",
            "5": "CODE",
            "6": "ADJ",
            "_NAV": "NAV",
            "_SYM": "SYM",
            "_NUM": "NUM",
            "_VIM_NAV": "VIM",
            "_VIM_CODE": "CODE",
            "_ADJUST": "ADJ"
        }
        name = layer_names.get(layer_num, f"L{layer_num}")
        return (name, "HOLD")

    # Control combos
    if key_code.startswith("LCTL("):
        inner = key_code[5:-1].replace("KC_", "")
        return (f"^ {inner}", "")

    # Standard mappings
    mappings = {
        "TAB": ("Tab", "⇥"),
        "BSPC": ("Bksp", "⌫"),
        "ENT": ("Enter", "⏎"),
        "SPC": ("Space", "␣"),
        "ESC": ("Esc", ""),
        "DEL": ("Del", "⌦"),
        "LSFT": ("Shift", "⇧"),
        "RSFT": ("Shift", "⇧"),
        "LGUI": ("Super", "◆"),
        "RALT": ("AltGr", ""),
        "NTIL": ("Ñ", ""),
        "ACUT": ("´", "¨"),
        "GRV": ("`", "^"),
        "CCED": ("Ç", ""),
        "COMM": (",", ";"),
        "DOT": (".", ":"),
        "MINS": ("-", "_"),
        "PLUS": ("+", "*"),
        "ASTR": ("*", ""),
        "SLSH": ("/", "?"),
        "EQL": ("=", "+"),
        "EQLS": ("=", "+"),
        "QUES": ("?", ""),
        "IQUE": ("¿", ""),
        "IEXC": ("¡", ""),
        "EXLM": ("!", ""),
        "EXCL": ("!", ""),
        "DQUO": ("\"", ""),
        "DQOT": ("\"", ""),
        "HASH": ("#", ""),
        "DLR": ("$", ""),
        "DLLR": ("$", ""),
        "PERC": ("%", ""),
        "AMPR": ("&", ""),
        "LPRN": ("(", ""),
        "RPRN": (")", ""),
        "LBRC": ("[", ""),
        "RBRC": ("]", ""),
        "LCBR": ("{", ""),
        "RCBR": ("}", ""),
        "LABK": ("<", ""),
        "RABK": (">", ""),
        "PIPE": ("|", ""),
        "BSLS": ("\\", ""),
        "TILD": ("~", ""),
        "EURO": ("€", ""),
        "ATSN": ("@", ""),
        "COLN": (":", ""),
        "SCLN": (";", ""),
        "UNDS": ("_", ""),
        "TRNS": ("▽", ""),
        "NO": ("·", ""),
        "QK_BOOT": ("BOOT", "Reset"),
        "EE_CLR": ("CLEAR", "EEPROM"),
        "NK_TOGG": ("NKRO", "Toggle"),
        "BRID": ("Bri-", "☼"),
        "BRIU": ("Bri+", "☼"),
        "VOLD": ("Vol-", "🔉"),
        "VOLU": ("Vol+", "🔊"),
        "MUTE": ("Mute", "🔇"),
        "MPLY": ("Play", "⏯"),
        "MNXT": ("Next", "⏭"),
        "MPRV": ("Prev", "⏮"),
        "HOME": ("Home", "↖"),
        "END": ("End", "↘"),
        "PGUP": ("PgUp", "⇞"),
        "PGDN": ("PgDn", "⇟"),
        "UP": ("Up", "↑"),
        "DOWN": ("Down", "↓"),
        "LEFT": ("Left", "←"),
        "RGHT": ("Right", "→"),
        "INS": ("Ins", ""),
        "VIM_SAVE": (":w", "Save"),
        "VIM_QUIT": (":q", "Quit"),
        "VIM_VSPLIT": ("vsplit", "^w v"),
        "VIM_HSPLIT": ("split", "^w s"),
        "VIM_BNEXT": (":bnext", "Buffer"),
        "VIM_BPREV": (":bprev", "Buffer"),
        "VIM_DEF": ("gd", "Def"),
        "VIM_REF": ("gr", "Refs"),
        "VIM_DIAGN": ("]d", "Next"),
        "VIM_DIAGP": ("[d", "Prev"),
        "VIM_HOVER": ("K", "Hover"),
        "VIM_ACT": ("Code", "Action"),
        "VIM_REN": ("Rename", "LSP"),
    }

    if key_code in mappings:
        return mappings[key_code]
    if clean in mappings:
        return mappings[clean]

    return (clean, "")

def render_svg_layer(profile_name: str, layer_data: dict) -> str:
    layer_name = layer_data["name"]
    layer_title = layer_data.get("title", layer_name)
    layer_desc = layer_data.get("description", "")
    keys = layer_data["keys"]

    total_width = 12 * (KEY_WIDTH + KEY_GAP) + SPLIT_GAP + 64
    total_height = 4 * (KEY_HEIGHT + KEY_GAP) + 130

    font_family = "system-ui, -apple-system, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif"

    # XML Escape titles and descriptions
    escaped_profile = xml_escape(profile_name.capitalize())
    escaped_layer_name = xml_escape(layer_name)
    escaped_title = xml_escape(layer_title)
    escaped_desc = xml_escape(layer_desc)

    svg_lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {total_width} {total_height}" width="{total_width}" height="{total_height}">',
        '  <defs>',
        '    <style>',
        f'      .title {{ font-family: {font_family}; font-size: 20px; font-weight: 700; fill: {NYVERUNE_PALETTE["ghost_white"]}; letter-spacing: 0.5px; }}',
        f'      .subtitle {{ font-family: {font_family}; font-size: 13px; fill: {NYVERUNE_PALETTE["soft_lilac"]}; }}',
        f'      .key-main {{ font-family: {font_family}; font-weight: 600; text-anchor: middle; dominant-baseline: central; }}',
        f'      .key-sub {{ font-family: {font_family}; font-weight: 500; font-size: 10px; text-anchor: middle; dominant-baseline: central; }}',
        '    </style>',
        '    <filter id="keyGlow" x="-20%" y="-20%" width="140%" height="140%">',
        f'      <feDropShadow dx="0" dy="2" stdDeviation="3" flood-color="{NYVERUNE_PALETTE["deep_violet"]}" flood-opacity="0.3"/>',
        '    </filter>',
        '  </defs>',
        f'  <!-- Canvas Background -->',
        f'  <rect width="{total_width}" height="{total_height}" fill="{COLORS["bg"]}" rx="16" stroke="{NYVERUNE_PALETTE["elevated"]}" stroke-width="2" />',
        f'  <!-- Header -->',
        f'  <circle cx="36" cy="42" r="6" fill="{NYVERUNE_PALETTE["neon_violet"]}" />',
        f'  <text x="52" y="47" class="title">{escaped_profile} — Layer {layer_data["id"]}: {escaped_layer_name}</text>',
        f'  <text x="52" y="70" class="subtitle">{escaped_title}: {escaped_desc}</text>',
        '  <g transform="translate(32, 96)">'
    ]

    # Helper to render keycap
    def render_keycap(x, y, w, h, raw_key):
        category = get_key_category(raw_key)
        main_label, sub_label = parse_key_labels(raw_key)

        # XML escape the key labels
        esc_main = xml_escape(main_label)
        esc_sub = xml_escape(sub_label)

        bg_col = COLORS.get(f"{category}", COLORS["alpha"])
        border_col = COLORS.get(f"{category}_border", COLORS["border"])
        main_text_col = COLORS.get(f"{category}_text", COLORS["text"])
        sub_text_col = NYVERUNE_PALETTE["soft_lilac"] if category != "thumb_layer" else NYVERUNE_PALETTE["dream_pink"]

        if len(main_label) >= 6:
            font_size = 11
        elif len(main_label) >= 4:
            font_size = 12
        else:
            font_size = 14

        key_elements = []
        key_elements.append(
            f'    <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="9" ry="9" fill="{bg_col}" stroke="{border_col}" stroke-width="1.6" filter="url(#keyGlow)" />'
        )

        cx = x + w / 2
        if sub_label:
            cy_main = y + h / 2 - 8
            cy_sub = y + h / 2 + 10
            key_elements.append(
                f'    <text x="{cx}" y="{cy_main}" font-size="{font_size}" fill="{main_text_col}" class="key-main">{esc_main}</text>'
            )
            key_elements.append(
                f'    <text x="{cx}" y="{cy_sub}" fill="{sub_text_col}" class="key-sub">{esc_sub}</text>'
            )
        else:
            cy_main = y + h / 2
            key_elements.append(
                f'    <text x="{cx}" y="{cy_main}" font-size="{font_size}" fill="{main_text_col}" class="key-main">{esc_main}</text>'
            )

        return "\n".join(key_elements)

    # Render Rows 0-2 (12 keys per row)
    for r in range(3):
        for c in range(12):
            key_idx = r * 12 + c
            raw_key = keys[key_idx]

            x = c * (KEY_WIDTH + KEY_GAP)
            if c >= 6:
                x += SPLIT_GAP
            y = r * (KEY_HEIGHT + KEY_GAP)

            svg_lines.append(render_keycap(x, y, KEY_WIDTH, KEY_HEIGHT, raw_key))

    # Render Thumbs (Row 3, 6 keys)
    thumb_positions = [
        (3, 36), (4, 37), (5, 38),
        (6, 39), (7, 40), (8, 41)
    ]

    thumb_y = 3 * (KEY_HEIGHT + KEY_GAP) + 8
    for col_align, key_idx in thumb_positions:
        raw_key = keys[key_idx]
        x = col_align * (KEY_WIDTH + KEY_GAP)
        if col_align >= 6:
            x += SPLIT_GAP

        svg_lines.append(render_keycap(x, thumb_y, KEY_WIDTH, KEY_HEIGHT, raw_key))

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
        left_half = " ".join(f"[{parse_key_labels(keys[r*12 + c])[0]:^7}]" for c in range(6))
        right_half = " ".join(f"[{parse_key_labels(keys[r*12 + c])[0]:^7}]" for c in range(6, 12))
        lines.append(f"{left_half}    {right_half}")

    lt = " ".join(f"[{parse_key_labels(keys[36 + i])[0]:^7}]" for i in range(3))
    rt = " ".join(f"[{parse_key_labels(keys[39 + i])[0]:^7}]" for i in range(3))
    spacer = " " * (3 * 10)
    lines.append(f"{spacer}{lt}    {rt}")
    lines.append("```")
    lines.append("")
    return "\n".join(lines)

def main():
    print("[*] Re-generating SVG diagrams with strict XML escaping...")
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
            print(f"  [✓] Updated SVG: {svg_file.relative_to(ROOT_DIR)}")

            text_dia = generate_text_diagram(layer)
            md_summary.append(f"## Layer {layer['id']}: {layer['name']}\n")
            md_summary.append(f"![Layer {layer['id']} Diagram](layer_{layer['id']}_{layer_name}.svg)\n")
            md_summary.append(text_dia)

        index_md = out_dir / "README.md"
        with open(index_md, "w", encoding="utf-8") as f:
            f.write("\n".join(md_summary))
        print(f"  [✓] Updated Diagram Summary: {index_md.relative_to(ROOT_DIR)}")

    print("[✓] All layout diagrams updated successfully.")

if __name__ == "__main__":
    main()

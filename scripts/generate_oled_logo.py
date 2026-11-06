#!/usr/bin/env python3
"""
Nyverune OLED Logo Generator for Corne (crkbd) 128x32 OLED screens.
Creates a custom pixel-art header file (firmware/shared/oled_logo.h)
compatible with QMK's oled_write_raw_P().
"""

import sys
from pathlib import Path

WIDTH = 128
HEIGHT = 32
PAGES = HEIGHT // 8  # 4 pages of 8 pixels height

def create_nyverune_bitmap() -> list[int]:
    # 128x32 2D grid: grid[y][x] = 1 (lit pixel) or 0 (dark)
    grid = [[0 for _ in range(WIDTH)] for _ in range(HEIGHT)]

    # Draw stylish double border
    for x in range(2, WIDTH - 2):
        grid[0][x] = 1
        grid[HEIGHT - 1][x] = 1
        grid[2][x] = 1 if (x % 3 != 0) else 0
        grid[HEIGHT - 3][x] = 1 if (x % 3 != 0) else 0

    for y in range(HEIGHT):
        grid[y][2] = 1
        grid[y][WIDTH - 3] = 1

    # Corner accents
    for d in range(4):
        grid[d][d + 2] = 1
        grid[d][WIDTH - 3 - d] = 1
        grid[HEIGHT - 1 - d][d + 2] = 1
        grid[HEIGHT - 1 - d][WIDTH - 3 - d] = 1

    # Rune / Diamond icons on left and right
    # Left diamond center at (16, 16)
    left_cx, right_cx = 16, WIDTH - 17
    cy = 16
    for i in range(-5, 6):
        span = 5 - abs(i)
        for s in range(-span, span + 1):
            if abs(s) == span or abs(i) == 5 or (abs(i) <= 1 and abs(s) <= 1):
                grid[cy + i][left_cx + s] = 1
                grid[cy + i][right_cx + s] = 1

    # Draw centered text using 5x7 bitmap font
    FONT_5X7 = {
        ' ': [0x00, 0x00, 0x00, 0x00, 0x00],
        'N': [0x7F, 0x04, 0x08, 0x10, 0x7F],
        'Y': [0x03, 0x04, 0x78, 0x04, 0x03],
        'V': [0x1F, 0x20, 0x40, 0x20, 0x1F],
        'E': [0x7F, 0x49, 0x49, 0x49, 0x41],
        'R': [0x7F, 0x09, 0x19, 0x29, 0x46],
        'U': [0x3F, 0x40, 0x40, 0x40, 0x3F],
        'C': [0x3E, 0x41, 0x41, 0x41, 0x22],
        'O': [0x3E, 0x41, 0x41, 0x41, 0x3E],
        'S': [0x46, 0x49, 0x49, 0x49, 0x31],
        'P': [0x7F, 0x09, 0x09, 0x09, 0x06],
        'L': [0x7F, 0x40, 0x40, 0x40, 0x40],
        'I': [0x00, 0x41, 0x7F, 0x41, 0x00],
        'T': [0x01, 0x01, 0x7F, 0x01, 0x01],
        '-': [0x08, 0x08, 0x08, 0x08, 0x08],
        '3': [0x21, 0x41, 0x45, 0x4B, 0x31],
        '6': [0x3C, 0x4A, 0x49, 0x49, 0x30],
        '+': [0x08, 0x08, 0x3E, 0x08, 0x08],
        'X': [0x63, 0x14, 0x08, 0x14, 0x63],
    }

    def draw_str(s: str, start_x: int, start_y: int):
        cur_x = start_x
        for ch in s.upper():
            glyph = FONT_5X7.get(ch, FONT_5X7[' '])
            for col_idx, col_byte in enumerate(glyph):
                for row_idx in range(7):
                    if (col_byte >> row_idx) & 1:
                        if 0 <= start_y + row_idx < HEIGHT and 0 <= cur_x + col_idx < WIDTH:
                            grid[start_y + row_idx][cur_x + col_idx] = 1
            cur_x += 6

    # Title: NYVERUNE (Centered on line 1, y=7)
    title = "NYVERUNE"
    title_width = len(title) * 6 - 1
    title_x = (WIDTH - title_width) // 2
    draw_str(title, title_x, 7)

    # Subtitle: CORNE 3X6+3 (Centered on line 2, y=18)
    sub = "CORNE 3X6+3"
    sub_width = len(sub) * 6 - 1
    sub_x = (WIDTH - sub_width) // 2
    draw_str(sub, sub_x, 18)

    # Convert 128x32 grid to SSD1306 format:
    # 4 pages of 128 bytes each. Each byte represents 8 vertical pixels (LSB at top).
    buffer = []
    for page in range(PAGES):
        for col in range(WIDTH):
            byte_val = 0
            for bit in range(8):
                y = page * 8 + bit
                if grid[y][col]:
                    byte_val |= (1 << bit)
            buffer.append(byte_val)

    return buffer

def main():
    buf = create_nyverune_bitmap()
    root = Path(__file__).resolve().parent.parent
    out_file = root / "firmware" / "shared" / "oled_logo.h"

    lines = [
        "#pragma once",
        "",
        "#include QMK_KEYBOARD_H",
        "",
        "/*",
        " * Custom 128x32 pixel OLED logo for Nyverune Corne",
        " * Rendered on slave half (right screen) via oled_write_raw_P()",
        " */",
        "",
        "static const char PROGMEM nyverune_oled_logo[512] = {"
    ]

    # Format bytes in rows of 16
    for i in range(0, len(buf), 16):
        chunk = buf[i:i+16]
        hex_str = ", ".join(f"0x{b:02X}" for b in chunk)
        comma = "," if i + 16 < len(buf) else ""
        lines.append(f"    {hex_str}{comma}")

    lines.append("};")
    lines.append("")

    with open(out_file, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"[✓] Generated custom OLED logo header: {out_file.relative_to(root)}")

if __name__ == "__main__":
    main()

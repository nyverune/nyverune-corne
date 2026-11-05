# Secondary Layers & Combos Architecture

Nyverune Corne relies on specialized secondary layers and chorded combos to maximize ergonomic efficiency on a 42-key layout without hand contortions.

---

## 1. Unified Thumb Cluster Strategy

The thumb cluster layout is symmetrical and predictable across all profiles:

```
[Left Hand Thumbs]                [Right Hand Thumbs]
[LGUI] [Lower / Num] [Space]      [Enter] [Raise / Nav] [AltGr]
```

### Accessing Layers:
- **Tapping Left Center Thumb:** Momentarily accesses the `_NUM` (Numeric + Function keys) layer.
- **Tapping Right Center Thumb:** Momentarily accesses the navigation layer (`_NAV` in Everyday, `_VIM_NAV` in Neovim).
- **Holding Both Center Thumbs:** Automatically engages the `_ADJUST` layer via QMK tri-layer logic.
- **Accessing `_SYM` Layer:** Accessible directly from `_NUM` (right thumb) and `_NAV` (left thumb), creating a seamless cross-hand flow for symbol entry.

---

## 2. Ergonomic Combos (Chords)

Combos allow triggering essential commands and delimiters directly from the base layer by striking two adjacent keys simultaneously.

| Combo Keys | Output | Description |
|---|---|---|
| `J + K` | `Escape` | Standard Vim escape without leaving home row |
| `Q + W` | `Escape` | Quick left-hand escape chord |
| `E + R` | `[` | Left square bracket (AltGr + ` in Spanish) |
| `U + I` | `]` | Right square bracket (AltGr + + in Spanish) |
| `D + F` | `{` | Left curly brace |
| `H + J` | `}` | Right curly brace |
| `C + V` | `(` | Left parenthesis |
| `M + N` | `)` | Right parenthesis |
| `P + Backspace` | `Delete` | Forward delete chord |

---

## 3. Secondary Layer Matrix Overview

### Navigation (`_NAV`)
Optimized for non-modal environments:
- Inverted-T / Cross arrow layout on right hand (`Left, Down, Up, Right`).
- Home, End, PageUp, PageDown positioned logically above arrows.
- Full clipboard operations (`Ctrl+A`, `Ctrl+C`, `Ctrl+V`, `Ctrl+X`, `Ctrl+Z`, `Ctrl+Y`) clustered on the left hand.

### Symbols (`_SYM`)
Eliminates the major pain point of Spanish ISO layouts where brackets and braces require AltGr chords:
- Delimiters `[ ]`, `{ }`, `( )` are placed symmetrically on home row and upper row.
- Common programming operators (`=`, `+`, `-`, `*`, `/`, `&`, `|`, `~`, `\`) are immediately accessible.

### Numbers & Functions (`_NUM`)
- Full 10-key numeric keypad on the right hand for high-throughput numeric data entry.
- F1–F12 function keys organized sequentially on the left hand.

### Neovim Modal (`_VIM_NAV` & `_VIM_CODE`)
- Native HJKL motion on the home row.
- Dedicated window splitting (`<C-w>v`, `<C-w>s`) and buffer navigation (`:bnext`, `:bprev`).
- Code intelligence actions (`gd` definition, `gr` references, `[d` / `]d` diagnostics, hover docs, code actions).


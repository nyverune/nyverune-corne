# Design Decisions & Ergonomic Architecture

This document records the architectural and ergonomic rationale behind **Nyverune Corne**.

---

## 1. Keyboard Form Factor: Corne 3x6+3 (42 Keys)

### Decision
Adopt the 6-column Corne variant (3 rows × 6 columns + 3 thumb keys per half) rather than the ultra-compact 5-column variant (36 keys).

### Rationale
- **Spanish Layout Requirements:** Spanish typing requires immediate, uncompromised access to the `Ñ` key, acute accents (`´`), and punctuation keys (`,`, `.`, `-`). On a 5-column board, `Ñ` is frequently forced onto a secondary layer or combo, severely degrading typing speed in Spanish.
- **Dedicated Outer Modifiers:** Retaining column 0 and column 5 provides dedicated outer keys for `Tab`, `Backspace`, and `Shift`, reducing cognitive load and finger gymnastics.

---

## 2. Spanish ISO Compatibility Without Host Remapping

### Decision
Construct all keymaps assuming the host operating system (Linux / Windows) input method is standard **Spanish (ISO)** (`es` or `es-ES`), leveraging QMK's `<keymap_extras/keymap_spanish.h>`.

### Rationale
- When pairing a split keyboard with laptops or multi-device setups, altering the OS keymap to US ANSI breaks built-in laptop keyboards and introduces friction when switching devices.
- By emitting standard Spanish scan codes, the Corne keyboard produces expected characters on any workstation configured for Spanish without custom OS daemon hooks.

---

## 3. Resolving the AltGr Bottleneck for Developers

### Problem
In standard Spanish ISO keyboards, critical programming symbols (`[`, `]`, `{`, `}`, `\`, `|`, `~`) require awkward three-finger `AltGr` combinations:
- `[` is `AltGr + ` `
- `]` is `AltGr + +`
- `{` is `AltGr + '`
- `}` is `AltGr + ç`
- `\` is `AltGr + º`

### Solution
1. **Dedicated `_SYM` Layer:** Provides single-tap access to all programming delimiters organized symmetrically (left brackets on left hand, right brackets on right hand).
2. **Ergonomic Direct Combos:**
   - `E + R` -> `[`
   - `U + I` -> `]`
   - `D + F` -> `{`
   - `H + J` -> `}`
   - `J + K` -> `Escape`
   - `P + Backspace` -> `Delete`

---

## 4. Modifier Strategy & Home Row Mods

### Decision
Use selective Dual-Role Tap-Hold keys (`LCTL_T(KC_ESC)`) rather than full 8-finger Home Row Mods (GACS).

### Rationale
- While 8-finger Home Row Mods are popular, they often introduce accidental modifier holds during fast rolling keystrokes in Spanish (where letter pairs like *es*, *er*, *en*, *st* roll rapidly).
- Mapping `Escape` on tap and `Left Control` on hold on the CapsLock position provides instant Vim escape without false modifiers during rapid prose typing.

---

## 5. Neovim Workflow Optimization

### Decision
Provide a specialized `neovim` profile with dedicated `_VIM_NAV` and `_VIM_CODE` layers while keeping the `_BASE` layer identical to `everyday`.

### Rationale
- Preserving the exact same base alphanumeric layer ensures zero muscle-memory penalty when moving between general typing and Neovim editing.
- The `_VIM_NAV` layer clusters `<C-w>` window splits, buffer cycling (`:bnext`, `:bprev`), and half-page jumps (`<C-u>`, `<C-d>`) directly under home row fingertips.
- The `_VIM_CODE` layer maps LSP definitions (`gd`), references (`gr`), diagnostics (`]d`, `[d`), and code actions (`<leader>ca`) to single chords.

---

## 6. Symmetrical Thumb Cluster and Tri-Layer

### Decision
Both profiles share an identical thumb cluster configuration:
- Left Thumbs: `[Super, Lower (_NUM), Space]`
- Right Thumbs: `[Enter, Raise (_NAV / _VIM_NAV), AltGr]`
- Simultaneous hold of Lower + Raise automatically triggers `_ADJUST` (hardware reset, bootloader, media).

### Rationale
The thumb cluster provides the highest mechanical leverage on a split keyboard. Keeping thumb roles consistent ensures effortless switching between profiles.

---

## 7. Nyverune Visual Identity

All diagrams and documentation widgets adhere strictly to the **Nyverune Palette**:
- **Void** (`#100D16`): Absolute canvas background.
- **Obsidian** (`#181224`): Primary keycap surfaces.
- **Elevated** (`#21182B`): Borders and control keys.
- **Neon Violet** (`#A855F7`): Active key highlighting and identity.
- **Dream Pink** (`#FF5CB8`): Thumb layer indicators.
- **Info** (`#38BDF8`): Navigation and directional arrows.
- **Ghost White** (`#F6F0FC`): Primary readable text.


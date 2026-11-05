# Layout and Layer Conventions

This document establishes the architecture, layer naming schemes, thumb cluster conventions, and design standards for all layouts in **Nyverune Corne**.

---

## 1. Physical Matrix Layout (Corne 3x6+3)

The Corne keyboard features an ergonomic split design with 42 total keys:
- **Left Half:** 3 rows × 6 columns + 3 thumb keys (21 keys).
- **Right Half:** 3 rows × 6 columns + 3 thumb keys (21 keys).

```
Left Half:                                 Right Half:
[ 0] [ 1] [ 2] [ 3] [ 4] [ 5]              [ 6] [ 7] [ 8] [ 9] [10] [11]
[12] [13] [14] [15] [16] [17]              [18] [19] [20] [21] [22] [23]
[24] [25] [26] [27] [28] [29]              [30] [31] [32] [33] [34] [35]
              [36] [37] [38]                [39] [40] [41]
```

---

## 2. Layer Enumeration and Hierarchy

All profiles conform to the following layer numbering scheme to maintain interoperability:

| Layer ID | Name | Constant | Purpose |
|---|---|---|---|
| `0` | **Base** | `_BASE` | Spanish QWERTY primary alphanumeric layer. Shared across all profiles. |
| `1` | **Navigation** | `_NAV` | Directional arrows, word hopping, page scrolling, clipboard operations. |
| `2` | **Symbols** | `_SYM` | Brackets, braces, arithmetic and programming symbols. |
| `3` | **Numbers** | `_NUM` | Numeric keypad grid and functional calculation keys. |
| `4` | **Vim Nav** | `_VIM_NAV` | Modal movement, window splits, buffer cycling, Neovim actions. |
| `5` | **Vim Code** | `_VIM_CODE` | LSP actions, code diagnostics, folding, Git integrations. |
| `6` | **Media** | `_MEDIA` | Audio volume, play/pause, media navigation, brightness. |
| `7` | **Adjust** | `_ADJUST` | Firmware reset, bootloader jump, EEPROM clear, hardware controls. |

---

## 3. Thumb Cluster Conventions

The thumb keys are the most accessible keys on a split ergonomic keyboard. To avoid cognitive dissonance when switching profiles, thumb keys follow a strict convention:

### Left Thumb Cluster
1. **Outer Thumb:** `KC_LGUI` (Super / Windows / Command key).
2. **Center Thumb:** `MO(_NUM)` (Momentary activation of Number / Lower layer).
3. **Inner Thumb:** `KC_SPC` (Spacebar).

### Right Thumb Cluster
1. **Inner Thumb:** `KC_ENT` (Enter key).
2. **Center Thumb:** `MO(_NAV)` (Momentary activation of Navigation / Raise layer).
3. **Outer Thumb:** `KC_RALT` (AltGr / Alternative Graphic key for Spanish symbols).

### Tri-Layer Activation
- Holding both **Lower** (`MO(_NUM)`) and **Raise** (`MO(_NAV)`) simultaneously automatically activates the `_ADJUST` layer via QMK's `update_tri_layer` logic.

---

## 4. Modifier & Ergonomic Strategy

- **Escape / Control:** Dual-role key on CapsLock physical location (`LCTL_T(KC_ESC)`):
  - Tap: sends `KC_ESC`.
  - Hold: acts as Left Control (`LCTL`).
- **Shift Keys:** Positioned symmetrically on outer bottom rows (`KC_LSFT` on left, `KC_RSFT` on right).
- **Tapping Term:** Configured to `200ms` with `PERMISSIVE_HOLD` and `QUICK_TAP_TERM = 120ms` to eliminate misfires while typing rapidly.

---

## 5. Profile Separation Principles

1. **Everyday Profile:**
   - General-purpose focus: web browsing, document writing, standard coding, shell work.
   - Standard arrows clustered on the right hand (I/J/K/L or H/J/K/L).
   - Dedicated media and shortcut keys.

2. **Neovim Profile:**
   - Editor-focused modal workflow.
   - HJKL navigation layer positioned natively on home row.
   - Single-chord shortcuts for Neovim window splitting (`<C-w>v`, `<C-w>s`), buffer switches (`:bprev`, `:bnext`), and diagnostic jumps (`[d`, `]d`).
   - Identical base typing layer so ordinary text input is uninterrupted.

---

## 6. Declarative JSON Schema

All layouts are authored or generated as declarative JSON files under `layouts/<profile>/layout.json` to empower automatic diagram rendering and documentation generation tools.

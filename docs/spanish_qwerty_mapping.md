# Spanish QWERTY Keymap Reference

The Nyverune Corne keyboard maps characters under the assumption that the host operating system (Linux / Windows) has its keyboard layout configured to **Spanish (ISO)** (`es` or `es-ES`).

## Core Principles

1. **Native Typing Experience:** All standard letters, accents (`á, é, í, ó, ú`), diaeresis (`ü`), and the `ñ / Ñ` letter behave identically to a native Spanish keyboard without requiring unicode hex input or OS switching.
2. **Dedicated `Ñ` Key:** Positioned in its canonical home-row position (right of `L`), giving Spanish writers immediate, muscle-memory accuracy.
3. **Ergonomic Access to Programming Symbols:** Programming symbols that are notoriously cumbersome on ISO Spanish keyboards (such as `[ ]`, `{ }`, `\`, `|`, `~`) are mapped on dedicated layers without requiring difficult multi-finger AltGr gymnastics.

## Mapping Table

| Character | Spanish ISO Keycode | QMK Keycode Alias | Description |
|---|---|---|---|
| `Ñ` | `ES_NTIL` (`KC_SCLN`) | `ES_NTIL` | Canonical Spanish Ñ key |
| `´ / ¨` | `ES_ACUT` (`KC_QUOT`) | `ES_ACUT` | Acute accent and diaeresis dead key |
| `Ç` | `ES_CCED` (`KC_BSLS`) | `ES_CCED` | C-cedilla |
| `, / ;` | `ES_COMM` (`KC_COMM`) | `ES_COMM` | Comma (Shift: Semicolon) |
| `. / :` | `ES_DOT` (`KC_DOT`) | `ES_DOT` | Period (Shift: Colon) |
| `- / _` | `ES_MINS` (`KC_SLSH`) | `ES_MINS` | Hyphen (Shift: Underscore) |
| `' / ?` | `ES_APOS` (`KC_MINS`) | `ES_APOS` | Single quote (Shift: Question mark) |
| `¡ / ¿` | `ES_IEXC` (`KC_EQL`) | `ES_IEXC` | Inverted exclamation (Shift: Inverted question) |
| `< / >` | `ES_LABK` (`KC_NUBS`) | `ES_LABK` | Less than (Shift: Greater than) |
| `º / ª / \`| `ES_ORDM` (`KC_GRV`) | `ES_ORDM` | Ordinal male / female / Backslash (AltGr) |

## Specialized Programming Symbols on Secondary Layers

To overcome standard Spanish ISO layout friction in coding and Neovim:
- `[` and `]` are accessible via the Symbol layer directly.
- `{` and `}` are grouped symmetrically for rapid block scoping.
- `\` and `/` are positioned on primary thumb/row extensions.
- `~` (tilde) and `|` (pipe) are single-tap symbols on the Symbol layer.


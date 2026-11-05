# Practical Ergonomic Refinements

Based on continuous typing evaluation and real-world Corne 3x6+3 usage, several key timings and keymap ergonomics were calibrated to prevent typing fatigue and input errors.

---

## 1. Timing Parameter Calibrations

| Parameter | Original | Refined | Rationale |
|---|---|---|---|
| `TAPPING_TERM` | `200ms` | `185ms` | Reduces hold latency when rolling across keys; prevents dual-role keys (like `LCTL_T(KC_ESC)`) from lagging. |
| `QUICK_TAP_TERM` | `120ms` | `100ms` | Eliminates accidental auto-repeat when quickly double tapping dual-role or tap-dance keys. |
| `COMBO_TERM` | `40ms` | `35ms` | Minimizes false-positive combo activations during fast typing bursts in Spanish (e.g. typing *ejemplo* will not accidentally trigger `E+R` or `J+K`). |
| `PERMISSIVE_HOLD` | Enabled | Enabled | Resolves dual-role key as hold immediately if another key is pressed and released before tapping term expires. |

---

## 2. Spanish ISO Symbol Accessibility Improvements

Standard Spanish QWERTY keyboards require heavy use of `AltGr` for brackets, braces, and backslash:
- On a traditional layout:
  - `[` = `AltGr + ` `
  - `]` = `AltGr + +`
  - `{` = `AltGr + '`
  - `}` = `AltGr + ç`
  - `\` = `AltGr + º`
  - `~` = `AltGr + 4`
- In **Nyverune Corne**:
  - `[` and `]` are accessible via the `E+R` and `U+I` direct combos, as well as dedicated keys on the `_SYM` layer.
  - `{` and `}` are mapped via `D+F` and `H+J` combos, keeping hands anchored on the home row.
  - `\` is placed on a primary reach on the `_SYM` layer.
  - `~` is mapped to upper left key on `_SYM` layer, allowing immediate terminal and home path usage (`~/`).

---

## 3. Thumb Cluster Balance

- **Left Thumb Cluster:** Dedicated to system commands (`Super`), numeric/lower layer access (`_NUM`), and Space.
- **Right Thumb Cluster:** Dedicated to confirmation (`Enter`), navigation/raise layer access (`_NAV`), and `AltGr`.
- This ensures balanced hand load: the left hand controls layer shift for numbers, while the right hand enters the numbers; the right hand controls layer shift for navigation, while the left hand triggers editing chords.

#pragma once

/*
 * Hardware and Ergonomic Configuration for Corne (crkbd) 3x6+3
 * Refined for high-speed typing and responsive dual-role key resolution.
 */

// Split keyboard master detection
#define EE_HANDS
#define USE_SERIAL

// Refined ergonomic tapping timing settings
#define TAPPING_TERM 185
#define QUICK_TAP_TERM 100
#define PERMISSIVE_HOLD
#define HOLD_ON_OTHER_KEY_PRESS

// Combo configuration - tight timing to avoid accidental chords during fast prose typing
#define COMBO_COUNT 16
#define COMBO_TERM 35

// Tap-Dance configuration
#define TAPPING_TERM_PER_KEY

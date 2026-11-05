#pragma once

/*
 * Layer Definitions for Nyverune Corne
 * Common layer enumeration and bitmasks across all layouts.
 */

enum nyverune_layers {
    _BASE = 0,    // Spanish QWERTY primary layer (shared across all profiles)
    _NAV,         // Directional arrows, home/end, page navigation, clipboard
    _SYM,         // Programming and punctuation symbols adapted for Spanish keycodes
    _NUM,         // Numpad, operators and functional number rows
    _VIM_NAV,     // Specialized Neovim modal navigation, splits and buffers
    _VIM_CODE,    // Specialized Neovim LSP, code actions and editor triggers
    _MEDIA,       // Audio, volume, brightness and OS controls
    _ADJUST       // Hardware control, reset, bootloader and layer toggles
};

// Layer state bitmask shorthands
#define LAYER_MASK_BASE    (1UL << _BASE)
#define LAYER_MASK_NAV     (1UL << _NAV)
#define LAYER_MASK_SYM     (1UL << _SYM)
#define LAYER_MASK_NUM     (1UL << _NUM)
#define LAYER_MASK_VIM_NAV (1UL << _VIM_NAV)
#define LAYER_MASK_VIM_CODE(1UL << _VIM_CODE)
#define LAYER_MASK_MEDIA   (1UL << _MEDIA)
#define LAYER_MASK_ADJUST  (1UL << _ADJUST)

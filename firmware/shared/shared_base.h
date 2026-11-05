#pragma once

#include QMK_KEYBOARD_H
#include "layers.h"
#include "spanish_aliases.h"

/*
 * Shared Primary Base Layer Macro for Corne 3x6+3 (42 keys)
 * Preserved across Everyday and Neovim layouts.
 */

#define LAYOUT_NYVERUNE_BASE \
    /* Left hand */ \
    KC_TAB,         ES_Q, ES_W, ES_E, ES_R, ES_T, \
    /* Right hand */ \
    ES_Y, ES_U, ES_I, ES_O, ES_P, KC_BSPC, \
    \
    /* Left hand home row */ \
    LCTL_T(KC_ESC), ES_A, ES_S, ES_D, ES_F, ES_G, \
    /* Right hand home row */ \
    ES_H, ES_J, ES_K, ES_L, ES_NTIL, ES_ACUT, \
    \
    /* Left hand bottom row */ \
    KC_LSFT,        ES_Z, ES_X, ES_C, ES_V, ES_B, \
    /* Right hand bottom row */ \
    ES_N, ES_M, ES_COMM, ES_DOT, ES_MINS, KC_RSFT, \
    \
    /* Thumb cluster: [Left GUI, Lower, Space] [Enter, Raise, AltGr] */ \
    KC_LGUI, MO(_NUM), KC_SPC,   KC_ENT, MO(_NAV), KC_RALT


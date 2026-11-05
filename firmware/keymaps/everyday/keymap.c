#include QMK_KEYBOARD_H
#include "../../shared/layers.h"
#include "../../shared/spanish_aliases.h"
#include "../../shared/shared_base.h"

/*
 * Everyday Keymap for Corne (crkbd) 3x6+3
 * General-purpose profile with Spanish QWERTY base, navigation, numpad, symbols and adjust layers.
 */

const uint16_t PROGMEM keymaps[][MATRIX_ROWS][MATRIX_COLS] = {
    [_BASE] = LAYOUT_split_3x6_3(
        /* Left Hand */
        KC_TAB,         ES_Q, ES_W, ES_E, ES_R, ES_T,
        /* Right Hand */
        ES_Y, ES_U, ES_I, ES_O, ES_P, KC_BSPC,

        /* Left Home Row */
        LCTL_T(KC_ESC), ES_A, ES_S, ES_D, ES_F, ES_G,
        /* Right Home Row */
        ES_H, ES_J, ES_K, ES_L, ES_NTIL, ES_ACUT,

        /* Left Bottom Row */
        KC_LSFT,        ES_Z, ES_X, ES_C, ES_V, ES_B,
        /* Right Bottom Row */
        ES_N, ES_M, ES_COMM, ES_DOT, ES_MINS, KC_RSFT,

        /* Left Thumbs: Super, Lower (Num), Space */
        KC_LGUI, MO(_NUM), KC_SPC,
        /* Right Thumbs: Enter, Raise (Nav), AltGr */
        KC_ENT, MO(_NAV), KC_RALT
    ),

    [_NAV] = LAYOUT_split_3x6_3(
        KC_TRNS, KC_HOME, KC_PGDN, KC_PGUP, KC_END,  KC_INS,
        KC_PGUP, KC_HOME, KC_UP,   KC_END,   KC_DEL,  KC_BSPC,

        KC_TRNS, LCTL(KC_A), LCTL(KC_S), KC_TAB, KC_ENT, KC_ESC,
        KC_PGDN, KC_LEFT, KC_DOWN, KC_RGHT, KC_DEL,  KC_TRNS,

        KC_LSFT, LCTL(KC_Z), LCTL(KC_X), LCTL(KC_C), LCTL(KC_V), LCTL(KC_Y),
        KC_NO,   KC_MNXT, KC_VOLD, KC_VOLU, KC_MPLY, KC_RSFT,

        KC_TRNS, MO(_SYM), KC_TRNS,
        KC_TRNS, KC_TRNS, KC_TRNS
    ),

    [_SYM] = LAYOUT_split_3x6_3(
        KC_TILD, ES_EXCL, ES_DQOT, ES_HASH, ES_DLLR, ES_PERC,
        ES_AMPR, ES_SLSH, ES_LPRN, ES_RPRN, ES_EQLS, KC_DEL,

        KC_TRNS, ES_BSLS, ES_PIPE, ES_LCBR, ES_RCBR, ES_GRAV,
        ES_PLUS, ES_MINS, ES_LBRC, ES_RBRC, ES_ASTR, ES_QUES,

        KC_TRNS, ES_LABK, ES_RABK, ES_ATSN, ES_TILD, ES_EURO,
        ES_UNDS, ES_COLN, ES_SCLN, ES_IQUE, ES_IEXC, KC_TRNS,

        KC_TRNS, KC_TRNS, KC_TRNS,
        KC_TRNS, KC_TRNS, KC_TRNS
    ),

    [_NUM] = LAYOUT_split_3x6_3(
        KC_ESC,  KC_F1,  KC_F2,  KC_F3,  KC_F4,  KC_F5,
        ES_SLSH, ES_7,   ES_8,   ES_9,   ES_MINS, KC_BSPC,

        KC_TAB,  KC_F6,  KC_F7,  KC_F8,  KC_F9,  KC_F10,
        ES_ASTR, ES_4,   ES_5,   ES_6,   ES_PLUS, KC_ENT,

        KC_LSFT, KC_F11, KC_F12, KC_NO,  KC_NO,  KC_NO,
        ES_0,    ES_1,   ES_2,   ES_3,   ES_DOT,  KC_RSFT,

        KC_TRNS, KC_TRNS, KC_TRNS,
        KC_TRNS, MO(_SYM), KC_TRNS
    ),

    [_ADJUST] = LAYOUT_split_3x6_3(
        QK_BOOT, KC_NO, KC_NO, KC_NO, KC_NO, KC_NO,
        KC_NO, KC_BRID, KC_BRIU, KC_NO, KC_NO, QK_BOOT,

        EE_CLR,  KC_NO, KC_NO, KC_NO, KC_NO, KC_NO,
        KC_MPRV, KC_MNXT, KC_VOLD, KC_VOLU, KC_MPLY, KC_MUTE,

        KC_NO,   KC_NO, KC_NO, KC_NO, KC_NO, KC_NO,
        NK_TOGG, KC_NO,   KC_NO,   KC_NO,   KC_NO,   KC_NO,

        KC_TRNS, KC_TRNS, KC_TRNS,
        KC_TRNS, KC_TRNS, KC_TRNS
    )
};

// Automatic Tri-layer activation: Lower (_NUM) + Raise (_NAV) => _ADJUST
layer_state_t layer_state_set_user(layer_state_t state) {
    return update_tri_layer_state(state, _NUM, _NAV, _ADJUST);
}

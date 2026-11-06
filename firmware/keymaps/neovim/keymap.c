#include QMK_KEYBOARD_H
#include "../../shared/layers.h"
#include "../../shared/spanish_aliases.h"
#include "../../shared/shared_base.h"
#include "../../shared/combos.h"

/*
 * Custom Neovim Keycodes and Macros
 */
enum custom_neovim_keycodes {
    VIM_SAVE = SAFE_RANGE,
    VIM_QUIT,
    VIM_VSPLIT,
    VIM_HSPLIT,
    VIM_BNEXT,
    VIM_BPREV,
    VIM_DEF,
    VIM_REF,
    VIM_DIAGN,
    VIM_DIAGP,
    VIM_HOVER,
    VIM_ACT,
    VIM_REN
};

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
        /* Right Thumbs: Enter (Hold: Ctrl), Raise (Vim Nav), AltGr (Hold: Sym) */
        RCTL_T(KC_ENT), MO(_VIM_NAV), LT(_SYM, KC_RALT)
    ),

    [_VIM_NAV] = LAYOUT_split_3x6_3(
        KC_TAB,  VIM_BPREV,    LCTL(KC_U),  LCTL(KC_D),  VIM_BNEXT,   LCTL(KC_T),
        KC_HOME, KC_PGDN,      KC_PGUP,     KC_END,      VIM_SAVE,    KC_BSPC,

        KC_ESC,  LCTL(KC_A),   VIM_HSPLIT,  VIM_VSPLIT,  KC_NO,       LCTL(KC_W),
        KC_LEFT, KC_DOWN,      KC_UP,       KC_RGHT,     ES_COLN,     KC_ENT,

        KC_LSFT, LCTL(KC_Z),   LCTL(KC_X),  LCTL(KC_C),  LCTL(KC_V),  LCTL(KC_Y),
        LCTL(KC_O), LCTL(KC_I), KC_NO,      KC_NO,       VIM_QUIT,    KC_RSFT,

        MO(_VIM_CODE), KC_TRNS, KC_TRNS,
        KC_TRNS,       KC_TRNS, MO(_VIM_CODE)
    ),

    [_VIM_CODE] = LAYOUT_split_3x6_3(
        KC_TAB,  VIM_DIAGP, VIM_DIAGN, VIM_HOVER, KC_NO,   KC_NO,
        KC_NO,   VIM_DEF,   VIM_REF,   KC_NO,     KC_NO,   KC_BSPC,

        KC_ESC,  VIM_ACT,   VIM_REN,   KC_NO,     KC_NO,   KC_NO,
        KC_NO,   KC_NO,     KC_NO,     KC_NO,     KC_NO,   KC_ENT,

        KC_LSFT, KC_NO,     KC_NO,     KC_NO,     KC_NO,   KC_NO,
        KC_NO,   KC_NO,     KC_NO,     KC_NO,     KC_NO,   KC_RSFT,

        KC_TRNS, KC_TRNS, KC_TRNS,
        KC_TRNS, KC_TRNS, KC_TRNS
    ),

    [_SYM] = LAYOUT_split_3x6_3(
        KC_TAB,  ES_EXLM, ES_DQUO, ES_HASH, ES_DLR, ES_PERC,
        ES_AMPR, ES_SLSH, ES_LPRN, ES_RPRN, ES_EQL, KC_DEL,

        KC_ESC,  ES_BSLS, ES_PIPE, ES_LCBR, ES_RCBR, ES_GRV,
        ES_PLUS, ES_MINS, ES_LBRC, ES_RBRC, ES_ASTR, ES_QUES,

        KC_LSFT, ES_LABK, ES_RABK, ES_ATSN, ES_TILD, ES_EURO,
        ES_UNDS, ES_COLN, ES_SCLN, ES_IQUE, ES_IEXC, KC_RSFT,

        KC_TRNS, KC_TRNS, KC_TRNS,
        KC_TRNS, KC_TRNS, KC_TRNS
    ),

    [_NUM] = LAYOUT_split_3x6_3(
        KC_TAB,  KC_F1,  KC_F2,  KC_F3,  KC_F4,  KC_F5,
        ES_SLSH, ES_7,   ES_8,   ES_9,   ES_MINS, KC_BSPC,

        KC_ESC,  KC_F6,  KC_F7,  KC_F8,  KC_F9,  KC_F10,
        ES_ASTR, ES_4,   ES_5,   ES_6,   ES_PLUS, KC_ENT,

        KC_LSFT, KC_F11, KC_F12, KC_NO,  KC_NO,  KC_NO,
        ES_0,    ES_1,   ES_2,   ES_3,   ES_DOT,  KC_RSFT,

        KC_TRNS, KC_TRNS, KC_TRNS,
        KC_TRNS, KC_TRNS, MO(_SYM)
    ),

    [_ADJUST] = LAYOUT_split_3x6_3(
        KC_TAB,  QK_BOOT, KC_NO,   KC_NO,   KC_NO,   KC_NO,
        KC_NO,   KC_BRID, KC_BRIU, KC_NO,   KC_NO,   QK_BOOT,

        KC_ESC,  EE_CLR,  KC_NO,   KC_NO,   KC_NO,   KC_NO,
        KC_MPRV, KC_MNXT, KC_VOLD, KC_VOLU, KC_MPLY, KC_MUTE,

        KC_LSFT, KC_NO,   KC_NO,   KC_NO,   KC_NO,   KC_NO,
        NK_TOGG, KC_NO,   KC_NO,   KC_NO,   KC_NO,   KC_NO,

        KC_TRNS, KC_TRNS, KC_TRNS,
        KC_TRNS, KC_TRNS, KC_TRNS
    )
};

static void send_vim_cmd(const char *cmd) {
    tap_code16(ES_COLN);
    for (const char *p = cmd; *p; p++) {
        if (*p >= 'a' && *p <= 'z') {
            tap_code(KC_A + (*p - 'a'));
        } else if (*p == '\n') {
            tap_code(KC_ENT);
        } else if (*p == ' ') {
            tap_code(KC_SPC);
        }
    }
}

// Macro execution for specialized Neovim commands with native Spanish keycode compatibility
bool process_record_user(uint16_t keycode, keyrecord_t *record) {
    if (record->event.pressed) {
        switch (keycode) {
            case VIM_SAVE:
                send_vim_cmd("w\n");
                return false;
            case VIM_QUIT:
                send_vim_cmd("q\n");
                return false;
            case VIM_VSPLIT:
                tap_code16(C(KC_W));
                tap_code(KC_V);
                return false;
            case VIM_HSPLIT:
                tap_code16(C(KC_W));
                tap_code(KC_S);
                return false;
            case VIM_BNEXT:
                send_vim_cmd("bnext\n");
                return false;
            case VIM_BPREV:
                send_vim_cmd("bprev\n");
                return false;
            case VIM_DEF:
                tap_code(KC_G);
                tap_code(KC_D);
                return false;
            case VIM_REF:
                tap_code(KC_G);
                tap_code(KC_R);
                return false;
            case VIM_DIAGN:
                tap_code16(ES_RBRC);
                tap_code(KC_D);
                return false;
            case VIM_DIAGP:
                tap_code16(ES_LBRC);
                tap_code(KC_D);
                return false;
            case VIM_HOVER:
                tap_code16(S(KC_K));
                return false;
            case VIM_ACT:
                tap_code(KC_SPC);
                tap_code(KC_C);
                tap_code(KC_A);
                return false;
            case VIM_REN:
                tap_code(KC_SPC);
                tap_code(KC_R);
                tap_code(KC_N);
                return false;
        }
    }
    return true;
}

// Automatic Tri-layer activation: Lower (_NUM) + Raise (_VIM_NAV) => _ADJUST
layer_state_t layer_state_set_user(layer_state_t state) {
    return update_tri_layer_state(state, _NUM, _VIM_NAV, _ADJUST);
}

#ifdef OLED_ENABLE
#include "../../shared/oled_logo.h"

void oled_render_logo(void) {
    oled_write_raw_P(nyverune_oled_logo, sizeof(nyverune_oled_logo));
}
#endif

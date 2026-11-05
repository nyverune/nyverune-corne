#pragma once

#include QMK_KEYBOARD_H
#include "spanish_aliases.h"

/*
 * Ergonomic Combos for Corne 3x6+3
 * Allows rapid access to vital keys and symbols without leaving the base layer.
 */

enum combos {
    CB_JK_ESC,    // J + K -> Escape (Classic Vim chord)
    CB_QW_ESC,    // Q + W -> Escape (Left-hand rapid chord)
    CB_ER_LBRC,   // E + R -> [
    CB_UI_RBRC,   // U + I -> ]
    CB_DF_LCBR,   // D + F -> {
    CB_HJ_RCBR,   // H + J -> }
    CB_CV_LPRN,   // C + V -> (
    CB_MN_RPRN,   // M + N -> )
    CB_DEL        // P + Backspace -> Delete
};

const uint16_t PROGMEM jk_combo[]   = {ES_J, ES_K, COMBO_END};
const uint16_t PROGMEM qw_combo[]   = {ES_Q, ES_W, COMBO_END};
const uint16_t PROGMEM er_combo[]   = {ES_E, ES_R, COMBO_END};
const uint16_t PROGMEM ui_combo[]   = {ES_U, ES_I, COMBO_END};
const uint16_t PROGMEM df_combo[]   = {ES_D, ES_F, COMBO_END};
const uint16_t PROGMEM hj_combo[]   = {ES_H, ES_J, COMBO_END};
const uint16_t PROGMEM cv_combo[]   = {ES_C, ES_V, COMBO_END};
const uint16_t PROGMEM mn_combo[]   = {ES_M, ES_N, COMBO_END};
const uint16_t PROGMEM del_combo[]  = {ES_P, KC_BSPC, COMBO_END};

combo_t key_combos[] = {
    [CB_JK_ESC]  = COMBO(jk_combo, KC_ESC),
    [CB_QW_ESC]  = COMBO(qw_combo, KC_ESC),
    [CB_ER_LBRC] = COMBO(er_combo, ES_LBRC),
    [CB_UI_RBRC] = COMBO(ui_combo, ES_RBRC),
    [CB_DF_LCBR] = COMBO(df_combo, ES_LCBR),
    [CB_HJ_RCBR] = COMBO(hj_combo, ES_RCBR),
    [CB_CV_LPRN] = COMBO(cv_combo, ES_LPRN),
    [CB_MN_RPRN] = COMBO(mn_combo, ES_RPRN),
    [CB_DEL]     = COMBO(del_combo, KC_DEL)
};

uint16_t COMBO_LEN = sizeof(key_combos) / sizeof(key_combos[0]);

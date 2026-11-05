#pragma once

#include QMK_KEYBOARD_H

/*
 * QMK Spanish QWERTY Keycode definitions and ergonomic aliases.
 * Assumes the host OS input source is set to Spanish (Spain / ISO).
 */

#ifndef ES_A
#include <keymap_extras/keymap_spanish.h>
#endif

// Fallbacks / convenience aliases for keymap clarity and consistency
#ifndef ES_NTIL
#define ES_NTIL KC_SCLN       // ñ and Ñ
#endif

#ifndef ES_ACUT
#define ES_ACUT KC_QUOT       // ´ (acute accent) and ¨ (diaeresis)
#endif

#ifndef ES_CCED
#define ES_CCED KC_BSLS       // ç and Ç
#endif

#ifndef ES_PLUS
#define ES_PLUS KC_RBRC       // + and * and ] (with AltGr)
#endif

#ifndef ES_COMM
#define ES_COMM KC_COMM       // , and ;
#endif

#ifndef ES_DOT
#define ES_DOT  KC_DOT        // . and :
#endif

#ifndef ES_MINS
#define ES_MINS KC_SLSH       // - and _
#endif

#ifndef ES_LABK
#define ES_LABK KC_NUBS       // < and >
#endif

#ifndef ES_APOS
#define ES_APOS KC_MINS       // ' and ?
#endif

#ifndef ES_IEXC
#define ES_IEXC KC_EQL        // ¡ and ¿
#endif

#ifndef ES_ORDM
#define ES_ORDM KC_GRV        // º and ª and \ (with AltGr)
#endif

// Ergonomic symbol shorthand aliases for layers
#define ES_EXCL S(ES_1)       // !
#define ES_DQOT S(ES_2)       // "
#define ES_HASH ALGR(ES_3)    // #
#define ES_DLLR S(ES_4)       // $
#define ES_PERC S(ES_5)       // %
#define ES_AMPR S(ES_6)       // &
#define ES_SLSH S(ES_7)       // /
#define ES_LPRN S(ES_8)       // (
#define ES_RPRN S(ES_9)       // )
#define ES_EQLS S(ES_0)       // =
#define ES_QUES S(ES_APOS)    // ?
#define ES_IQUE S(ES_IEXC)    // ¿
#define ES_COLN S(ES_DOT)     // :
#define ES_SCLN S(ES_COMM)    // ;
#define ES_UNDS S(ES_MINS)    // _
#define ES_ASTR S(ES_PLUS)    // *

// AltGr symbol shortcuts (Spanish ISO)
#define ES_BSLS ALGR(ES_ORDM) // \  (AltGr + º)
#define ES_PIPE ALGR(ES_1)    // |  (AltGr + 1)
#define ES_ATSN ALGR(ES_2)    // @  (AltGr + 2)
#define ES_HASH ALGR(ES_3)    // #  (AltGr + 3)
#define ES_TILD ALGR(ES_4)    // ~  (AltGr + 4)
#define ES_EURO ALGR(ES_5)    // €  (AltGr + 5)
#define ES_LBRC ALGR(ES_ACUT) // [  (AltGr + `)
#define ES_RBRC ALGR(ES_PLUS) // ]  (AltGr + +)
#define ES_LCBR ALGR(ES_ACUT) // {  (or AltGr + ')
#define ES_RCBR ALGR(ES_CCED) // }  (AltGr + ç)

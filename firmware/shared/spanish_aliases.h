#pragma once

#include QMK_KEYBOARD_H
#include <keymap_extras/keymap_spanish.h>

/*
 * QMK Spanish QWERTY Keycode definitions and ergonomic aliases.
 * Assumes the host OS input source is set to Spanish (Spain / ISO).
 * Bridges shorthand aliases to QMK's native keymap_spanish.h definitions.
 */

// Shorthand aliases & compatibility bridges for Nyverune keymaps
#ifndef ES_EXCL
#define ES_EXCL ES_EXLM
#endif

#ifndef ES_DQOT
#define ES_DQOT ES_DQUO
#endif

#ifndef ES_DLLR
#define ES_DLLR ES_DLR
#endif

#ifndef ES_EQLS
#define ES_EQLS ES_EQL
#endif

#ifndef ES_GRAV
#define ES_GRAV ES_GRV
#endif

#ifndef ES_ATSN
#define ES_ATSN ES_AT
#endif

#ifndef ES_APOS
#define ES_APOS ES_QUOT
#endif

#ifndef ES_IEXC
#define ES_IEXC ES_IEXL
#endif

#ifndef ES_ORDM
#define ES_ORDM ES_MORD
#endif

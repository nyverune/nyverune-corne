#pragma once

#include QMK_KEYBOARD_H
#include "raw_hid_protocol.h"
#include "layers.h"

#ifdef RAW_ENABLE
#include "raw_hid.h"

static uint8_t current_active_profile = PROFILE_EVERYDAY;

inline uint8_t get_nyverune_profile(void) {
    return current_active_profile;
}

inline void set_nyverune_profile(uint8_t profile) {
    current_active_profile = (profile == PROFILE_NEOVIM) ? PROFILE_NEOVIM : PROFILE_EVERYDAY;
    if (current_active_profile == PROFILE_NEOVIM) {
        default_layer_set(LAYER_MASK_BASE);
    } else {
        default_layer_set(LAYER_MASK_BASE);
    }
}

void raw_hid_receive(uint8_t *data, uint8_t length) {
    if (length < 32 || data[0] != NYVERUNE_RAW_MAGIC) {
        return;
    }

    uint8_t cmd = data[2];
    uint8_t resp[32] = {0};
    resp[0] = NYVERUNE_RAW_MAGIC;
    resp[1] = NYVERUNE_RAW_VERSION;
    resp[2] = cmd;

    switch (cmd) {
        case CMD_GET_PROFILE:
            resp[3] = current_active_profile;
            break;

        case CMD_SET_PROFILE:
            set_nyverune_profile(data[3]);
            resp[3] = current_active_profile;
            break;

        case CMD_GET_STATUS:
            resp[3] = current_active_profile;
            resp[4] = get_highest_layer(layer_state);
            break;

        case CMD_PING:
            resp[3] = 0x55; // Pong
            break;

        default:
            resp[2] = 0xFF; // Unknown command
            break;
    }

    raw_hid_send(resp, 32);
}
#endif

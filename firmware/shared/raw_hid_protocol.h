#pragma once

#include <stdint.h>

/*
 * Nyverune Raw HID Protocol Specification
 * Bidirectional 32-byte packet structure for desktop profile synchronization.
 */

#define NYVERUNE_RAW_MAGIC      0xAA
#define NYVERUNE_RAW_VERSION    0x01

enum nyverune_hid_commands {
    CMD_GET_PROFILE = 0x01,  // Request current active profile
    CMD_SET_PROFILE = 0x02,  // Switch active profile
    CMD_GET_STATUS  = 0x03,  // Query keyboard info, layer, and WPM
    CMD_PING        = 0x04   // Keepalive / presence ping
};

enum nyverune_profile_id {
    PROFILE_EVERYDAY = 0x00,
    PROFILE_NEOVIM   = 0x01
};

typedef struct {
    uint8_t magic;      // Always 0xAA
    uint8_t version;    // 0x01
    uint8_t command;    // nyverune_hid_commands
    uint8_t payload[29];
} nyverune_hid_packet_t;

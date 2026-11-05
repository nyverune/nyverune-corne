# QMK global build configuration for Corne 3x6+3

# Microcontroller settings (default Corne uses ATmega32U4 / RP2040)
MCU ?= atmega32u4
BOOTLOADER ?= caterina

# Hardware feature toggles
BOOTMAGIC_ENABLE = yes     # Virtual DIP switch configuration
MOUSEKEY_ENABLE = no       # Mouse keys
EXTRAKEY_ENABLE = yes      # Audio controls and System keys
CONSOLE_ENABLE = no        # Console for debug
COMMAND_ENABLE = no        # Commands for debug and configuration
SLEEP_LED_ENABLE = no      # Breathing sleep LED during USB suspend
NKRO_ENABLE = yes          # USB N-Key Rollover
BACKLIGHT_ENABLE = no      # Custom backlighting
RGBLIGHT_ENABLE = no       # RGB underglow (disabled by default to save firmware space)
OLED_ENABLE = no           # OLED display support
COMBO_ENABLE = yes         # Key chord / combo support
TAP_DANCE_ENABLE = no      # Disabled to avoid undeclared tap dance actions
LTO_ENABLE = yes           # Link Time Optimization to reduce binary size

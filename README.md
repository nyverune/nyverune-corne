# Nyverune Corne

Personal collection of custom keyboard layouts and configurations for the Corne (crkbd) split keyboard, designed around ergonomics, productivity, and specialized workflows.

The project maintains reproducible, documented, and version-controlled configurations using QMK firmware with a consistent Spanish QWERTY primary layer across all profiles.

## Technical Specifications

| Component | Selection |
|---|---|
| Keyboard | Corne (crkbd) 3x6+3 (42 keys) |
| Firmware | QMK Firmware |
| Base layout | Spanish QWERTY (native `Ñ` and punctuation) |
| Primary layer | Shared across all profiles |
| Secondary layers | Profile-specific (Everyday, Neovim) |
| Documentation | Automated Markdown & SVG diagrams |
| Target environments | Linux (Arch Linux) and Windows |

## Repository Structure

```
nyverune-corne/
├── layouts/           # Declarative JSON layout definitions per profile
│   ├── shared/        # Shared base layer definitions
│   ├── everyday/      # Everyday profile definitions
│   └── neovim/        # Neovim profile definitions
├── firmware/          # QMK source files, rules, and keymaps
│   ├── shared/        # Shared QMK headers and Spanish keycodes
│   └── keymaps/       # Profile-specific QMK keymaps
│       ├── everyday/  # Everyday keymap (keymap.c, rules.mk, config.h)
│       └── neovim/    # Neovim keymap (keymap.c, rules.mk, config.h)
├── diagrams/          # Generated visual layout diagrams (SVG & ASCII)
├── docs/              # Comprehensive design, layer, and flashing documentation
└── scripts/           # Validation, diagram, and documentation generation utilities
```

## Profiles

- **Everyday:** General-purpose layout for typing, navigation, numbers, symbols, and window management.
- **Neovim:** Modal editing layout with dedicated layers for HJKL navigation, window splits, buffer management, and LSP controls.

## Development Milestones

- [x] **Milestone 1 — Project Foundation**
  - [x] Establish the repository structure.
  - [ ] Configure the QMK development environment.
  - [ ] Define the shared primary layer.
  - [ ] Establish the Spanish QWERTY keymap.
  - [ ] Define conventions for layout and layer organization.
- [ ] **Milestone 2 — Initial Layouts**
  - [ ] Implement the Everyday layout.
  - [ ] Implement the Neovim layout.
  - [ ] Design and configure specialized secondary layers.
  - [ ] Test both layouts on the Corne keyboard.
  - [ ] Refine mappings based on practical usage.
- [ ] **Milestone 3 — Documentation and Diagrams**
  - [ ] Establish a diagram generation workflow.
  - [ ] Generate visual representations of each layout.
  - [ ] Implement automatic documentation generation.
  - [ ] Document layers, key mappings, and design decisions.
  - [ ] Document firmware compilation and flashing.
- [ ] **Milestone 4 — Profile Management Exploration**

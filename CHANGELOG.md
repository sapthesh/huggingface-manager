# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

### Planned
- pagination for large repo lists
- more polished terminal layout
- additional Space controls
- package/installable CLI support

## [2.0.0] - 2025-08-08

### Added
- Rich-based terminal UI with panels, tables, and colors
- Interactive dashboard-style home screen
- Repository browsing for models, datasets, and spaces
- Public repo search and inspection
- File operations:
  - list files
  - upload file
  - upload folder
  - download file
  - delete files
  - create folder
- Repository operations:
  - create repo
  - rename/move repo
  - change visibility
  - delete repo
- Discussion operations:
  - list discussions
  - create discussion
  - comment on discussion
- Space operations:
  - runtime info
  - restart
  - pause
  - request hardware
  - set sleep time
  - add/delete secrets
  - add/delete variables
- Back/Cancel support across menus and flows
- Safer confirmation flow for destructive actions

### Changed
- Replaced older token handling with `get_token()` for newer `huggingface_hub` versions
- Improved UX to reduce forced exits and restart of the app

### Fixed
- `HfFolder` import compatibility issue
- Missing cancel path in delete and nested flows

# 🤗 Hugging Face Terminal Manager V2

[![Python](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/)
[![Hugging Face Hub](https://img.shields.io/badge/HuggingFace-Hub-yellow)](https://huggingface.co/)
[![Rich](https://img.shields.io/badge/UI-Rich-magenta)](https://github.com/Textualize/rich)
[![InquirerPy](https://img.shields.io/badge/Prompts-InquirerPy-green)](https://github.com/kazhala/InquirerPy)
[![Terminal UI](https://img.shields.io/badge/interface-interactive%20terminal%20ui-brightgreen)](#)
[![Status](https://img.shields.io/badge/status-active-success)](#)
<a href="https://hits.sh/github.com/sapthesh/huggingface-manager/"><img alt="Hits" src="https://hits.sh/github.com/sapthesh/huggingface-manager.svg?view=today-total&color=fe7d37"/></a>

A polished, colorful, interactive terminal manager for the Hugging Face Hub.

This project lets you manage `models`, `datasets`, and `spaces` directly from the terminal with a more visual, GUI-like experience using `rich` panels, tables, colors, and `InquirerPy` prompts.

It is designed for users who want to do common Hugging Face Hub tasks without repeatedly opening the web UI.

---

## ✨ Highlights

- Interactive terminal dashboard
- Rich panels, tables, and colorful status messages
- Manage `models`, `datasets`, and `spaces`
- Browse and inspect public repositories
- File operations from terminal
- Discussion management
- Space runtime and environment controls
- Safe `Back / Cancel` flow across menus
- More modern CLI/TUI feel than a plain script

---

## 📸 UI Style

This is a terminal UI, not a web app, but it aims to feel more polished and interactive than a traditional CLI.

### Visual Elements
- Dashboard panels
- Colored repo info tables
- README preview panels
- Danger panels for destructive actions
- Styled success, warning, and error messages
- Interactive menus and multi-select checkboxes

### Interaction Style
- Arrow-key navigation
- Enter to confirm
- Space for multi-select
- Esc or Ctrl+C to cancel/back in many prompts
- Blank text input cancels many operations safely

---

## 🚀 Features

## Feature Overview

| Category | Feature | Supported |
|---|---|---:|
| Account | Show current logged-in user | ✅ |
| Account | Show masked token info | ✅ |
| Repositories | Manage your models | ✅ |
| Repositories | Manage your datasets | ✅ |
| Repositories | Manage your spaces | ✅ |
| Repositories | Browse public repositories | ✅ |
| Repositories | Search public repositories | ✅ |
| Repositories | Create repositories | ✅ |
| Repositories | Rename / move repositories | ✅ |
| Repositories | Change repo visibility | ✅ |
| Repositories | Delete repositories | ✅ |
| Files | List repo files | ✅ |
| Files | Upload a file | ✅ |
| Files | Upload a folder | ✅ |
| Files | Download a file | ✅ |
| Files | Delete one or many files | ✅ |
| Files | Create folders via placeholder file | ✅ |
| Preview | Preview `README.md` in terminal | ✅ |
| Discussions | List discussions / PRs | ✅ |
| Discussions | Create discussion | ✅ |
| Discussions | Comment on discussion | ✅ |
| Spaces | View runtime info | ✅* |
| Spaces | Restart Space | ✅* |
| Spaces | Pause Space | ✅* |
| Spaces | Request hardware | ✅* |
| Spaces | Set sleep time | ✅* |
| Spaces | Add/delete secrets | ✅* |
| Spaces | Add/delete variables | ✅* |
| UX | Back / Cancel in menus | ✅ |
| UX | Safer destructive confirmations | ✅ |

> `*` Space features depend on the installed `huggingface_hub` version and API support.

---

## 🧩 Detailed Features

## Repository Management

| Action | Models | Datasets | Spaces |
|---|---:|---:|---:|
| View repo info | ✅ | ✅ | ✅ |
| List files | ✅ | ✅ | ✅ |
| Preview README | ✅ | ✅ | ✅ |
| Upload file | ✅ | ✅ | ✅ |
| Upload folder | ✅ | ✅ | ✅ |
| Download file | ✅ | ✅ | ✅ |
| Delete files | ✅ | ✅ | ✅ |
| Create folder | ✅ | ✅ | ✅ |
| Change visibility | ✅ | ✅ | ✅ |
| Rename / move | ✅ | ✅ | ✅ |
| Delete repo | ✅ | ✅ | ✅ |
| Discussions | ✅ | ✅ | ✅ |
| Space runtime controls | ❌ | ❌ | ✅ |

## Space Controls

| Space Action | Description |
|---|---|
| Runtime Info | Shows stage, hardware, requested hardware, sleep time, and storage |
| Restart Space | Requests a Space restart |
| Pause Space | Pauses a running Space |
| Request Hardware | Requests a different Space hardware tier |
| Set Sleep Time | Sets automatic sleep timeout in seconds |
| Add Secret | Adds a private secret environment value |
| Delete Secret | Deletes a Space secret |
| Add Variable | Adds a normal environment variable |
| Delete Variable | Deletes a normal environment variable |

## Safety and UX

| UX Feature | Description |
|---|---|
| Back / Cancel | Available throughout the app |
| Blank input cancel | Many text prompts cancel on blank input |
| Ctrl+C safety | Many prompts return instead of killing the session |
| Delete confirmation | Destructive operations require explicit confirmation |
| Exact repo confirmation | Repo deletion requires typing the exact repo ID |

---

## 📦 Requirements

- Python `3.9+`
- Hugging Face account
- Hugging Face access token
- Internet connection

---

## 🔧 Dependencies

Install required packages:

```bash
pip install -U huggingface_hub InquirerPy rich
```

---

## 🔐 Login

Before using the manager, log in with:

```bash
huggingface-cli login
```

Paste your Hugging Face token when prompted.

You can create or manage tokens here:

- `https://huggingface.co/settings/tokens`

### Recommended Token Permissions
Depending on what you want to do, your token may need permission for:
- read access
- write access
- repo deletion
- Space management
- discussions
- secrets / variables

---

## ▶️ Running the App

Save the script as:

```bash
hf_manager_v2.py
```

Run it with:

```bash
python hf_manager_v2.py
```

---

## 🖥️ Main Menu

When launched, the app opens a dashboard-like terminal interface with a main menu similar to:

- `Account info`
- `Manage my repos`
- `Create repo`
- `Search public repos`
- `Browse public repo and inspect`
- `Exit`

---

## ⌨️ Controls

| Key | Action |
|---|---|
| `↑` / `↓` | Move through menu items |
| `Enter` | Confirm selection |
| `Space` | Select checkbox items |
| `Esc` | Cancel in supported prompts |
| `Ctrl+C` | Back/cancel in many prompts |
| Blank input | Cancels many text-input flows |

---

## 🗂️ Menu Walkthrough

## 1. Account Info

Displays:
- Hugging Face username
- masked token
- user payload returned by the Hub

Useful for:
- confirming session status
- checking which account is active

---

## 2. Manage My Repos

Lets you manage repositories that belong to your account.

### Step 1
Choose a repository type:
- `Models`
- `Datasets`
- `Spaces`

### Step 2
Choose one of your repos.

### Step 3
Open the repo actions menu.

Available actions include:
- repo info
- list files
- README preview
- upload file
- upload folder
- download file
- delete files
- create folder
- change visibility
- rename / move repo
- list discussions
- create discussion
- comment on discussion
- Space controls
- delete repo

---

## 3. Create Repo

Create a new:
- model repo
- dataset repo
- space repo

### Space SDK options
If you create a Space, you can choose:
- `gradio`
- `streamlit`
- `docker`
- `static`

### Visibility
You can also choose:
- public
- private

---

## 4. Search Public Repos

Searches public repositories by type:
- models
- datasets
- spaces

Useful for:
- discovery
- quick lookup
- terminal-first browsing

---

## 5. Browse Public Repo and Inspect

Lets you search for public repositories and inspect them from the terminal.

Depending on permissions and ownership, you may be able to:
- view repo info
- list files
- preview README
- browse discussions

Some write operations may fail for repos you do not own.

---

## 📁 Repository Actions

## Repo Info

Shows metadata such as:
- repo ID
- repo type
- private/public status
- author
- SHA
- last modified time
- downloads
- likes
- tags
- gated / disabled state when available

---

## List Files

Displays repository files in a rich table.

Useful for:
- checking model checkpoints
- browsing dataset structure
- viewing Space app contents

---

## Preview README

Downloads and previews `README.md` directly inside the terminal.

Useful for:
- reading model cards
- checking dataset documentation
- viewing Space descriptions

---

## Upload File

Upload one local file to a selected repo.

### Inputs
- local file path
- target path in repo
- commit message

---

## Upload Folder

Upload a whole local folder to the repo.

### Inputs
- local folder path
- destination folder path
- commit message

---

## Download File

Download a file from a repo to a local folder.

### Inputs
- source file in repo
- local destination directory

---

## Delete Files

Select one or more files and delete them from the repo.

### Safety
- checkbox-based multi-select
- cancel support
- confirmation before deletion

---

## Create Folder

Creates a folder using a placeholder `.gitkeep` file.

This is needed because Git-based repos do not track empty folders by themselves.

---

## Change Visibility

Switch a repo between:
- public
- private

---

## Rename / Move Repo

Move or rename a repo by changing its repo ID.

### Example

```text
old: yourname/my-model
new: yourname/my-model-v2
```

Restrictions may apply depending on ownership and namespace permissions.

---

## Delete Repo

Deletes the entire repository permanently.

### Protection Steps
1. warning panel
2. confirmation prompt
3. exact repo ID re-entry

### Example

```text
Type the exact repo id to confirm: yourname/my-model
```

---

## 💬 Discussions

## List Discussions

Shows discussions and pull requests for a repository.

Displayed fields:
- discussion number
- title
- status
- author

---

## Create Discussion

Create a new discussion directly from terminal.

Useful for:
- notes
- questions
- collaboration
- issue tracking

---

## Comment on Discussion

Comment on an existing discussion by selecting it or entering the discussion number.

---

## 🚀 Space Controls

Only available when managing a repository of type `space`.

### Runtime Info
Shows:
- current stage
- hardware
- requested hardware
- sleep time
- storage

### Restart Space
Useful after:
- code updates
- environment changes
- runtime issues

### Pause Space
Useful for:
- stopping unused Space activity
- managing resource usage

### Request Hardware
Request available hardware tiers such as:
- `cpu-basic`
- `cpu-upgrade`
- `t4-small`
- `t4-medium`
- `a10g-small`
- `a10g-large`
- `a100-large`

Availability depends on your account plan and Space settings.

### Set Sleep Time
Set auto-sleep timeout in seconds.

Examples:
- `3600`
- `7200`
- `86400`

### Secrets
Use secrets for sensitive information such as:
- API keys
- service tokens
- private credentials

### Variables
Use variables for non-sensitive configuration such as:
- app mode
- region
- flags
- runtime settings

---

## 🛡️ Back / Cancel Behavior

This version is designed so you do not get stuck inside a flow.

### Supported behavior
- `⬅ Back / Cancel` entries in menus
- blank text input cancels many prompts
- Esc cancels many prompt screens
- Ctrl+C often returns to the menu instead of forcing a full app exit
- destructive actions require explicit confirmation

This makes the tool much smoother to use than a simple linear script.

---

## 🧪 Example Workflows

## Example 1: Safely Delete Files

1. Start the app
2. Open `Manage my repos`
3. Select `Models`
4. Choose a repo
5. Select `Delete files`
6. Mark files with `Space`
7. Confirm deletion or cancel

## Example 2: Create a New Space

1. Open `Create repo`
2. Select `Spaces`
3. Enter a repo name
4. Choose the Space SDK
5. Choose public or private
6. Confirm creation

## Example 3: Restart a Space

1. Open `Manage my repos`
2. Choose `Spaces`
3. Select your Space
4. Open `Space controls`
5. Choose `Restart Space`

## Example 4: Inspect a Public Model

1. Open `Browse public repo and inspect`
2. Select `Models`
3. Search for a repo
4. Open `Repo info`
5. Open `List files`
6. Open `Preview README`

---

## 🧯 Troubleshooting

## Import Error for `HfFolder`

Older examples often use `HfFolder`, but recent versions of `huggingface_hub` changed token access patterns.

This project uses:

```python
from huggingface_hub import get_token
```

Upgrade if needed:

```bash
pip install -U huggingface_hub
```

---

## Not Logged In

If the app says you are not logged in:

```bash
huggingface-cli login
```

Then run the program again.

---

## Space Features Not Available

Some Space operations depend on your installed `huggingface_hub` version and API support.

Upgrade first:

```bash
pip install -U huggingface_hub
```

If the option still does not work, that capability may not be available in your current Hub client version.

---

## Permission Errors

If an operation fails due to permissions:
- confirm you own the repository
- verify your token scopes
- make sure you are logged into the correct Hugging Face account
- check whether the repo is protected or restricted

---

## ⚠️ Limitations

This project relies on the public `huggingface_hub` Python API.

That means:
- it can only support features exposed by the library
- some Hugging Face web GUI features are not available via API
- some Space features are version-dependent
- some actions may behave differently based on repo type, account plan, or permissions

It covers many of the most useful Hub workflows, but it is not guaranteed to be a 100% replacement for every web UI feature.

---

## 🔒 Security Notes

- Never share your Hugging Face token
- Use Space secrets for sensitive credentials
- Be careful with delete operations
- Review visibility changes before confirming
- Prefer private repos for non-public content

---

## 🛠️ Tech Stack

| Component | Purpose |
|---|---|
| `huggingface_hub` | Hugging Face Hub API access |
| `InquirerPy` | Interactive prompts and menus |
| `rich` | Panels, tables, colors, layout, styled output |

---

## 📋 Minimal Quick Start

### Install
```bash
pip install -U huggingface_hub InquirerPy rich
```

### Login
```bash
huggingface-cli login
```

### Run
```bash
python hf_manager_v2.py
```

---

## 🗺️ Roadmap Ideas

Potential future improvements:
- pagination for very large repo lists
- sortable tables
- live refresh
- keyboard shortcuts
- command palette
- export to JSON / CSV
- batch repo actions
- local config support
- true multi-pane TUI using `Textual`
- mouse support
- live logs for Spaces

---

## 🤝 Contributing

You can extend this project by improving:
- UI polish
- pagination
- error handling
- Hub API compatibility
- batch operations
- Space feature coverage
- documentation

---

## 📄 License

Distributed under the MIT License. See the LICENSE file for more information.


---

## 🙌 Credits

Built with:
- [Hugging Face Hub](https://huggingface.co/docs/huggingface_hub/index)
- [Rich](https://github.com/Textualize/rich)
- [InquirerPy](https://github.com/kazhala/InquirerPy)

Created By:
- [sapthesh](https://github.com/sapthesh/)

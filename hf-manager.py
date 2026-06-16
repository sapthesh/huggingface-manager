import os
import sys
import shutil
import tempfile
from pathlib import Path
from typing import Iterable, List, Optional, Sequence

from huggingface_hub import HfApi, get_token, hf_hub_download, list_repo_files
from huggingface_hub.utils import HfHubHTTPError
from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from rich.align import Align
from rich.box import HEAVY, ROUNDED, SIMPLE_HEAVY
from rich.console import Console, Group
from rich.panel import Panel
from rich.table import Table
from rich.text import Text


api = HfApi()
console = Console()


def clear():
    os.system("cls" if os.name == "nt" else "clear")


def pause():
    try:
        input("\nPress Enter to continue...")
    except KeyboardInterrupt:
        pass


def safe_execute(title, func, *args, **kwargs):
    try:
        return func(*args, **kwargs)
    except HfHubHTTPError as error:
        console.print(
            Panel(
                f"[bold red]HF ERROR[/bold red]\n{title}\n\n{error}",
                border_style="red",
                title="Request Failed",
            )
        )
    except Exception as error:
        console.print(
            Panel(
                f"[bold red]ERROR[/bold red]\n{title}\n\n{error}",
                border_style="red",
                title="Unexpected Failure",
            )
        )
    return None


def back_choice():
    return Choice("back", name="⬅ Back / Cancel")


def is_back(value):
    if value is None:
        return True
    if value == "back":
        return True
    if isinstance(value, str) and value.strip() == "":
        return True
    return False


def prompt_select(message: str, choices: Sequence, **kwargs):
    try:
        return inquirer.select(message=message, choices=list(choices), **kwargs).execute()
    except KeyboardInterrupt:
        return "back"


def prompt_checkbox(message: str, choices: Sequence, **kwargs):
    try:
        return inquirer.checkbox(message=message, choices=list(choices), **kwargs).execute()
    except KeyboardInterrupt:
        return ["back"]


def prompt_text(message: str, default: str = "", allow_cancel: bool = True, **kwargs):
    if allow_cancel:
        if default:
            message = f"{message} (blank = cancel)"
        else:
            message = f"{message} (blank = cancel)"
    try:
        value = inquirer.text(message=message, default=default, **kwargs).execute()
    except KeyboardInterrupt:
        return ""
    if allow_cancel and isinstance(value, str) and value.strip() == "":
        return ""
    return value


def prompt_secret(message: str, allow_cancel: bool = True):
    if allow_cancel:
        message = f"{message} (blank = cancel)"
    try:
        value = inquirer.secret(message=message).execute()
    except KeyboardInterrupt:
        return ""
    if allow_cancel and isinstance(value, str) and value.strip() == "":
        return ""
    return value


def prompt_confirm(message: str, default: bool = False):
    try:
        return inquirer.confirm(message=message, default=default).execute()
    except KeyboardInterrupt:
        return False


def prompt_filepath(message: str, default: str = ""):
    try:
        value = inquirer.filepath(message=f"{message} (Esc/Ctrl+C = cancel)", default=default).execute()
    except KeyboardInterrupt:
        return ""
    return value or ""


def require_login():
    token = get_token()
    if not token:
        console.print(
            Panel(
                "[bold red]You are not logged in.[/bold red]\n\nRun [cyan]huggingface-cli login[/cyan] first.",
                border_style="red",
                title="Authentication Required",
            )
        )
        sys.exit(1)

    try:
        return api.whoami()
    except Exception:
        console.print(
            Panel(
                "[bold red]Unable to validate session.[/bold red]\n\nRun [cyan]huggingface-cli login[/cyan] again.",
                border_style="red",
                title="Session Error",
            )
        )
        sys.exit(1)


def header_panel(username: str):
    title = Text("🤗 Hugging Face Terminal Manager", style="bold white")
    version = Text("V2 Interactive Hub Console", style="bold bright_blue")
    subtitle = Text(f"Logged in as: {username}", style="cyan")
    help_line = Text("Arrow keys • Enter • Space • Esc/Ctrl+C = cancel/back", style="dim")
    return Panel(
        Align.center(Group(title, version, subtitle, help_line)),
        border_style="bright_blue",
        box=HEAVY,
        title="Dashboard",
    )


def stats_panel(username: str):
    try:
        models = len([repo.id for repo in api.list_models(author=username)])
        datasets = len([repo.id for repo in api.list_datasets(author=username)])
        spaces = len([repo.id for repo in api.list_spaces(author=username)])
    except Exception:
        models = datasets = spaces = "?"
    table = Table.grid(expand=True)
    table.add_column(justify="center")
    table.add_column(justify="center")
    table.add_column(justify="center")
    table.add_row(
        f"[bold magenta]{models}[/bold magenta]\nModels",
        f"[bold green]{datasets}[/bold green]\nDatasets",
        f"[bold yellow]{spaces}[/bold yellow]\nSpaces",
    )
    return Panel(table, border_style="blue", box=ROUNDED, title="My Hub Stats")


def render_home(username: str):
    clear()
    console.print(header_panel(username))
    console.print(stats_panel(username))


def render_message(title: str, body: str, style: str = "green"):
    console.print(Panel(body, title=title, border_style=style, box=ROUNDED))


def truncate_text(value, limit=100):
    text = str(value)
    if len(text) <= limit:
        return text
    return text[: limit - 3] + "..."


def select_repo_type() -> Optional[str]:
    selected = prompt_select(
        "Select repository type:",
        [
            Choice("model", name="🤖 Models"),
            Choice("dataset", name="📊 Datasets"),
            Choice("space", name="🚀 Spaces"),
            back_choice(),
        ],
    )
    if is_back(selected):
        return None
    return selected


def fetch_user_repos(username: str, repo_type: str) -> List[str]:
    if repo_type == "model":
        return [repo.id for repo in api.list_models(author=username)]
    if repo_type == "dataset":
        return [repo.id for repo in api.list_datasets(author=username)]
    if repo_type == "space":
        return [repo.id for repo in api.list_spaces(author=username)]
    return []


def fetch_public_repos(repo_type: str, search: str = "") -> List[str]:
    if repo_type == "model":
        return [repo.id for repo in api.list_models(search=search, limit=100)]
    if repo_type == "dataset":
        return [repo.id for repo in api.list_datasets(search=search, limit=100)]
    if repo_type == "space":
        return [repo.id for repo in api.list_spaces(search=search, limit=100)]
    return []


def render_repo_list_table(repos: Iterable[str], title: str):
    table = Table(title=title, header_style="bold bright_blue", box=SIMPLE_HEAVY)
    table.add_column("#", style="cyan", width=6)
    table.add_column("Repository", style="white")
    for index, repo in enumerate(repos, start=1):
        table.add_row(str(index), repo)
    console.print(table)


def repo_picker(username: str, repo_type: str, public_search: bool = False) -> Optional[str]:
    if public_search:
        query = prompt_text("Search public repos", allow_cancel=True)
        if is_back(query):
            return None
        repos = fetch_public_repos(repo_type, query)
        title = f"Public {repo_type.title()} Results"
    else:
        repos = fetch_user_repos(username, repo_type)
        title = f"My {repo_type.title()} Repositories"

    if not repos:
        render_message("No Results", "No repositories found.", "yellow")
        pause()
        return None

    clear()
    render_repo_list_table(repos[:50], title)

    selected = prompt_select(
        f"Select a {repo_type} repository:",
        repos[:200] + [back_choice()],
        long_instruction="Pick a repo to inspect or manage",
    )
    if is_back(selected):
        return None
    return selected


def render_repo_info(repo_id: str, repo_type: str):
    info = safe_execute("Fetching repo info", api.repo_info, repo_id=repo_id, repo_type=repo_type)
    if not info:
        pause()
        return

    table = Table(title=f"Repository Info • {repo_id}", header_style="bold magenta", box=ROUNDED)
    table.add_column("Field", style="cyan", no_wrap=True)
    table.add_column("Value", style="white")

    tags = getattr(info, "tags", []) or []
    rows = [
        ("ID", getattr(info, "id", repo_id)),
        ("Type", repo_type),
        ("Private", str(getattr(info, "private", "N/A"))),
        ("Author", str(getattr(info, "author", "N/A"))),
        ("SHA", str(getattr(info, "sha", "N/A"))),
        ("Last Modified", str(getattr(info, "lastModified", "N/A"))),
        ("Downloads", str(getattr(info, "downloads", "N/A"))),
        ("Likes", str(getattr(info, "likes", "N/A"))),
        ("Gated", str(getattr(info, "gated", "N/A"))),
        ("Disabled", str(getattr(info, "disabled", "N/A"))),
        ("Tags", ", ".join(tags) if tags else "—"),
    ]

    for field, value in rows:
        table.add_row(field, truncate_text(value, 160))

    console.print(table)

    card_data = getattr(info, "cardData", None)
    if card_data:
        console.print(
            Panel(
                truncate_text(card_data, 800),
                title="Card Data",
                border_style="blue",
                box=ROUNDED,
            )
        )
    pause()


def create_repo_flow(username: str):
    repo_type = select_repo_type()
    if not repo_type:
        return

    name = prompt_text(f"Enter new {repo_type} repo name", allow_cancel=True)
    if is_back(name):
        return

    private = prompt_confirm("Private repo?", default=False)

    kwargs = {
        "repo_id": f"{username}/{name.strip()}",
        "repo_type": repo_type,
        "private": private,
        "exist_ok": False,
    }

    if repo_type == "space":
        sdk = prompt_select(
            "Select Space SDK:",
            [
                Choice("gradio", name="Gradio"),
                Choice("streamlit", name="Streamlit"),
                Choice("docker", name="Docker"),
                Choice("static", name="Static"),
                back_choice(),
            ],
        )
        if is_back(sdk):
            return
        kwargs["space_sdk"] = sdk

    clear()
    render_message(
        "Create Repository",
        f"Repo ID: [cyan]{kwargs['repo_id']}[/cyan]\nType: [magenta]{repo_type}[/magenta]\nPrivate: [yellow]{private}[/yellow]",
        "blue",
    )

    if not prompt_confirm("Create this repository?", default=True):
        return

    result = safe_execute("Creating repo", api.create_repo, **kwargs)
    if result:
        render_message("Success", f"Created repository [cyan]{kwargs['repo_id']}[/cyan].", "green")
    pause()


def delete_repo_flow(repo_id: str, repo_type: str):
    render_message(
        "Danger Zone",
        f"You are about to permanently delete:\n[bold red]{repo_id}[/bold red]\nType: {repo_type}",
        "red",
    )
    if not prompt_confirm("Continue to delete?", default=False):
        return

    typed_value = prompt_text(f"Type the exact repo id to confirm: {repo_id}", allow_cancel=True)
    if is_back(typed_value):
        return

    if typed_value != repo_id:
        render_message("Cancelled", "Confirmation text did not match.", "yellow")
        pause()
        return

    safe_execute("Deleting repo", api.delete_repo, repo_id=repo_id, repo_type=repo_type)
    render_message("Deleted", f"Repository [red]{repo_id}[/red] deleted.", "red")
    pause()


def update_visibility_flow(repo_id: str, repo_type: str):
    action = prompt_select(
        "Choose visibility:",
        [
            Choice(True, name="🔒 Private"),
            Choice(False, name="🌍 Public"),
            back_choice(),
        ],
    )
    if is_back(action):
        return

    result = safe_execute(
        "Updating visibility",
        api.update_repo_visibility,
        repo_id=repo_id,
        repo_type=repo_type,
        private=action,
    )
    if result is not None:
        render_message("Updated", f"Visibility updated for [cyan]{repo_id}[/cyan].", "green")
    pause()


def move_repo_flow(repo_id: str, repo_type: str):
    new_id = prompt_text("Enter new repo id (example: username/new-name)", allow_cancel=True)
    if is_back(new_id):
        return

    if "/" not in new_id or len(new_id.strip()) < 4:
        render_message("Invalid Input", "Repository ID must look like `username/name`.", "yellow")
        pause()
        return

    if not prompt_confirm(f"Move or rename '{repo_id}' to '{new_id}'?", default=False):
        return

    result = safe_execute(
        "Moving repo",
        api.move_repo,
        from_id=repo_id,
        to_id=new_id.strip(),
        repo_type=repo_type,
    )
    if result is not None:
        render_message("Moved", f"Repository moved to [cyan]{new_id}[/cyan].", "green")
    pause()


def list_files_flow(repo_id: str, repo_type: str):
    files = safe_execute("Listing repo files", list_repo_files, repo_id=repo_id, repo_type=repo_type)
    if files is None:
        pause()
        return
    if not files:
        render_message("Empty Repository", "This repository has no files.", "yellow")
        pause()
        return

    table = Table(title=f"Files • {repo_id}", header_style="bold blue", box=ROUNDED)
    table.add_column("#", style="cyan", width=6)
    table.add_column("Path", style="white")

    for index, item in enumerate(files, start=1):
        table.add_row(str(index), item)

    console.print(table)
    render_message("Tip", "Use Upload / Delete / Download actions from the repo menu for file operations.", "blue")
    pause()


def readme_preview_flow(repo_id: str, repo_type: str):
    files = safe_execute("Listing repo files", list_repo_files, repo_id=repo_id, repo_type=repo_type)
    if not files:
        render_message("No Files", "No files found in the repository.", "yellow")
        pause()
        return

    candidates = [item for item in files if Path(item).name.lower() in {"readme.md", "readme"}]
    if not candidates:
        render_message("README Missing", "No README file found.", "yellow")
        pause()
        return

    readme_path = candidates[0]
    local_path = safe_execute(
        "Downloading README",
        hf_hub_download,
        repo_id=repo_id,
        repo_type=repo_type,
        filename=readme_path,
    )
    if not local_path:
        pause()
        return

    try:
        with open(local_path, "r", encoding="utf-8", errors="ignore") as file:
            content = file.read(5000)
        console.print(
            Panel(
                content or "(empty README)",
                title=f"README Preview • {readme_path}",
                border_style="green",
                box=ROUNDED,
            )
        )
        if len(content) >= 5000:
            console.print("[yellow]Preview truncated to first 5000 characters.[/yellow]")
    except Exception as error:
        render_message("Read Error", f"Could not read README.\n\n{error}", "red")
    pause()


def upload_file_flow(repo_id: str, repo_type: str):
    local_path = prompt_filepath("Select local file to upload")
    if is_back(local_path):
        return
    if not os.path.isfile(local_path):
        render_message("Invalid File", "Selected path is not a file.", "yellow")
        pause()
        return

    path_in_repo = prompt_text("Enter destination path in repo", default=os.path.basename(local_path), allow_cancel=True)
    if is_back(path_in_repo):
        return

    commit_message = prompt_text(
        "Commit message",
        default=f"Upload {os.path.basename(local_path)}",
        allow_cancel=True,
    )
    if is_back(commit_message):
        return

    clear()
    render_message(
        "Upload File",
        f"Local: [white]{local_path}[/white]\nRepo Path: [cyan]{path_in_repo}[/cyan]\nRepo: [magenta]{repo_id}[/magenta]",
        "blue",
    )

    if not prompt_confirm("Upload this file?", default=True):
        return

    result = safe_execute(
        "Uploading file",
        api.upload_file,
        path_or_fileobj=local_path,
        path_in_repo=path_in_repo,
        repo_id=repo_id,
        repo_type=repo_type,
        commit_message=commit_message,
    )
    if result:
        render_message("Uploaded", f"File uploaded to [cyan]{path_in_repo}[/cyan].", "green")
    pause()


def upload_folder_flow(repo_id: str, repo_type: str):
    folder_path = prompt_filepath("Select local folder to upload")
    if is_back(folder_path):
        return
    if not os.path.isdir(folder_path):
        render_message("Invalid Folder", "Selected path is not a folder.", "yellow")
        pause()
        return

    path_in_repo = prompt_text("Destination folder in repo", default="", allow_cancel=True)
    if is_back(path_in_repo) and path_in_repo != "":
        return

    commit_message = prompt_text(
        "Commit message",
        default=f"Upload folder {os.path.basename(folder_path)}",
        allow_cancel=True,
    )
    if is_back(commit_message):
        return

    clear()
    render_message(
        "Upload Folder",
        f"Local Folder: [white]{folder_path}[/white]\nRepo Folder: [cyan]{path_in_repo or '/'}[/cyan]\nRepo: [magenta]{repo_id}[/magenta]",
        "blue",
    )

    if not prompt_confirm("Upload this folder?", default=True):
        return

    result = safe_execute(
        "Uploading folder",
        api.upload_folder,
        folder_path=folder_path,
        path_in_repo=path_in_repo,
        repo_id=repo_id,
        repo_type=repo_type,
        commit_message=commit_message,
    )
    if result is not None:
        render_message("Uploaded", "Folder uploaded successfully.", "green")
    pause()


def download_file_flow(repo_id: str, repo_type: str):
    files = safe_execute("Listing repo files", list_repo_files, repo_id=repo_id, repo_type=repo_type)
    if not files:
        render_message("No Files", "No files found.", "yellow")
        pause()
        return

    file_choice = prompt_select(
        "Select file to download:",
        list(files) + [back_choice()],
        long_instruction="Pick a file to save locally",
    )
    if is_back(file_choice):
        return

    destination_dir = prompt_filepath("Select destination directory", default=str(Path.cwd()))
    if is_back(destination_dir):
        return
    if not os.path.isdir(destination_dir):
        render_message("Invalid Directory", "Destination must be a valid directory.", "yellow")
        pause()
        return

    try:
        downloaded_path = hf_hub_download(repo_id=repo_id, repo_type=repo_type, filename=file_choice)
        target_path = Path(destination_dir) / Path(file_choice).name
        shutil.copyfile(downloaded_path, target_path)
        render_message("Downloaded", f"Saved to [cyan]{target_path}[/cyan].", "green")
    except Exception as error:
        render_message("Download Failed", str(error), "red")
    pause()


def delete_files_flow(repo_id: str, repo_type: str):
    files = safe_execute("Listing repo files", list_repo_files, repo_id=repo_id, repo_type=repo_type)
    if not files:
        render_message("No Files", "No files found.", "yellow")
        pause()
        return

    selected_files = prompt_checkbox(
        f"Select files to delete from {repo_id}:",
        list(files) + [back_choice()],
        instruction="Space to select • Enter to confirm • Esc/Ctrl+C = cancel",
    )

    if not selected_files or "back" in selected_files:
        return

    preview = "\n".join(f"• {item}" for item in selected_files[:20])
    if len(selected_files) > 20:
        preview += f"\n... and {len(selected_files) - 20} more"

    render_message(
        "Delete Files",
        f"You selected [red]{len(selected_files)}[/red] file(s):\n{preview}",
        "red",
    )

    if not prompt_confirm("Delete selected files?", default=False):
        return

    for item in selected_files:
        safe_execute(
            f"Deleting {item}",
            api.delete_file,
            path_in_repo=item,
            repo_id=repo_id,
            repo_type=repo_type,
            commit_message=f"Delete {item}",
        )
        console.print(f"[red]Deleted:[/red] {item}")
    pause()


def create_folder_flow(repo_id: str, repo_type: str):
    folder_name = prompt_text("Folder path to create", allow_cancel=True)
    if is_back(folder_name):
        return

    placeholder_name = f"{folder_name.rstrip('/')}/.gitkeep"

    with tempfile.NamedTemporaryFile("w", delete=False, encoding="utf-8") as temp_file:
        temp_path = temp_file.name

    try:
        result = safe_execute(
            "Creating folder",
            api.upload_file,
            path_or_fileobj=temp_path,
            path_in_repo=placeholder_name,
            repo_id=repo_id,
            repo_type=repo_type,
            commit_message=f"Create folder {folder_name}",
        )
        if result:
            render_message("Folder Created", f"Created folder [cyan]{folder_name}[/cyan].", "green")
    finally:
        try:
            os.unlink(temp_path)
        except Exception:
            pass
    pause()


def list_discussions_flow(repo_id: str, repo_type: str):
    discussions = safe_execute("Listing discussions", api.get_repo_discussions, repo_id=repo_id, repo_type=repo_type)
    if discussions is None:
        pause()
        return

    discussions = list(discussions)
    if not discussions:
        render_message("No Discussions", "No discussions or PRs found.", "yellow")
        pause()
        return

    table = Table(title=f"Discussions • {repo_id}", header_style="bold magenta", box=ROUNDED)
    table.add_column("#", style="cyan", width=6)
    table.add_column("Title", style="white")
    table.add_column("Status", style="green")
    table.add_column("Author", style="yellow")

    for discussion in discussions:
        table.add_row(
            str(getattr(discussion, "num", "?")),
            truncate_text(getattr(discussion, "title", "No title"), 80),
            str(getattr(discussion, "status", "N/A")),
            str(getattr(discussion, "author", "N/A")),
        )

    console.print(table)
    pause()


def create_discussion_flow(repo_id: str, repo_type: str):
    title = prompt_text("Discussion title", allow_cancel=True)
    if is_back(title):
        return

    description = prompt_text("Discussion description", allow_cancel=True)
    if is_back(description) and description != "":
        return

    result = safe_execute(
        "Creating discussion",
        api.create_discussion,
        repo_id=repo_id,
        repo_type=repo_type,
        title=title,
        description=description,
    )
    if result:
        render_message("Discussion Created", f"Created discussion #[cyan]{getattr(result, 'num', '?')}[/cyan].", "green")
    pause()


def comment_discussion_flow(repo_id: str, repo_type: str):
    discussions = safe_execute("Listing discussions", api.get_repo_discussions, repo_id=repo_id, repo_type=repo_type)
    discussion_numbers = []
    if discussions is not None:
        discussions = list(discussions)
        for discussion in discussions:
            number = getattr(discussion, "num", None)
            title = getattr(discussion, "title", "No title")
            if number is not None:
                discussion_numbers.append(Choice(int(number), name=f"#{number} • {truncate_text(title, 80)}"))

    if discussion_numbers:
        selected = prompt_select(
            "Select a discussion to comment on:",
            discussion_numbers + [back_choice()],
        )
        if is_back(selected):
            return
        discussion_num = int(selected)
    else:
        number_text = prompt_text("Discussion number", allow_cancel=True)
        if is_back(number_text):
            return
        if not str(number_text).isdigit():
            render_message("Invalid Number", "Discussion number must be numeric.", "yellow")
            pause()
            return
        discussion_num = int(number_text)

    comment = prompt_text("Comment text", allow_cancel=True)
    if is_back(comment):
        return

    result = safe_execute(
        "Commenting on discussion",
        api.comment_discussion,
        repo_id=repo_id,
        repo_type=repo_type,
        discussion_num=discussion_num,
        comment=comment,
    )
    if result:
        render_message("Comment Added", f"Added comment to discussion #[cyan]{discussion_num}[/cyan].", "green")
    pause()


def space_runtime_info_flow(repo_id: str):
    if not hasattr(api, "get_space_runtime"):
        render_message("Not Supported", "Your installed `huggingface_hub` does not support Space runtime APIs.", "yellow")
        pause()
        return

    runtime = safe_execute("Fetching Space runtime", api.get_space_runtime, repo_id=repo_id)
    if not runtime:
        pause()
        return

    table = Table(title=f"Space Runtime • {repo_id}", header_style="bold green", box=ROUNDED)
    table.add_column("Field", style="cyan")
    table.add_column("Value", style="white")
    table.add_row("Stage", str(getattr(runtime, "stage", "N/A")))
    table.add_row("Hardware", str(getattr(runtime, "hardware", "N/A")))
    table.add_row("Requested Hardware", str(getattr(runtime, "requested_hardware", "N/A")))
    table.add_row("Sleep Time", str(getattr(runtime, "sleep_time", "N/A")))
    table.add_row("Storage", str(getattr(runtime, "storage", "N/A")))

    console.print(table)
    pause()


def restart_space_flow(repo_id: str):
    if not hasattr(api, "restart_space"):
        render_message("Not Supported", "Your installed `huggingface_hub` does not support restarting Spaces.", "yellow")
        pause()
        return

    if not prompt_confirm(f"Restart Space '{repo_id}'?", default=False):
        return

    result = safe_execute("Restarting Space", api.restart_space, repo_id=repo_id)
    if result is not None:
        render_message("Restart Requested", f"Restart requested for [cyan]{repo_id}[/cyan].", "green")
    pause()


def pause_space_flow(repo_id: str):
    if not hasattr(api, "pause_space"):
        render_message("Not Supported", "Your installed `huggingface_hub` does not support pausing Spaces.", "yellow")
        pause()
        return

    if not prompt_confirm(f"Pause Space '{repo_id}'?", default=False):
        return

    result = safe_execute("Pausing Space", api.pause_space, repo_id=repo_id)
    if result is not None:
        render_message("Paused", f"Space [cyan]{repo_id}[/cyan] paused.", "green")
    pause()


def set_space_hardware_flow(repo_id: str):
    if not hasattr(api, "request_space_hardware"):
        render_message("Not Supported", "Your installed `huggingface_hub` does not support Space hardware requests.", "yellow")
        pause()
        return

    hardware = prompt_select(
        "Select hardware tier:",
        [
            Choice("cpu-basic", name="CPU Basic"),
            Choice("cpu-upgrade", name="CPU Upgrade"),
            Choice("t4-small", name="T4 Small"),
            Choice("t4-medium", name="T4 Medium"),
            Choice("a10g-small", name="A10G Small"),
            Choice("a10g-large", name="A10G Large"),
            Choice("a100-large", name="A100 Large"),
            back_choice(),
        ],
    )
    if is_back(hardware):
        return

    result = safe_execute("Requesting hardware", api.request_space_hardware, repo_id=repo_id, hardware=hardware)
    if result is not None:
        render_message("Hardware Requested", f"Requested [cyan]{hardware}[/cyan] for [magenta]{repo_id}[/magenta].", "green")
    pause()


def set_space_sleep_time_flow(repo_id: str):
    if not hasattr(api, "set_space_sleep_time"):
        render_message("Not Supported", "Your installed `huggingface_hub` does not support sleep-time changes.", "yellow")
        pause()
        return

    seconds_text = prompt_text("Sleep time in seconds", allow_cancel=True)
    if is_back(seconds_text):
        return
    if not seconds_text.isdigit():
        render_message("Invalid Input", "Sleep time must be a whole number in seconds.", "yellow")
        pause()
        return

    result = safe_execute(
        "Setting sleep time",
        api.set_space_sleep_time,
        repo_id=repo_id,
        sleep_time=int(seconds_text),
    )
    if result is not None:
        render_message("Sleep Time Updated", f"Set sleep time to [cyan]{seconds_text}[/cyan] seconds.", "green")
    pause()


def add_space_secret_flow(repo_id: str):
    if not hasattr(api, "add_space_secret"):
        render_message("Not Supported", "Your installed `huggingface_hub` does not support Space secrets.", "yellow")
        pause()
        return

    key = prompt_text("Secret name", allow_cancel=True)
    if is_back(key):
        return

    value = prompt_secret("Secret value", allow_cancel=True)
    if is_back(value):
        return

    result = safe_execute("Adding Space secret", api.add_space_secret, repo_id=repo_id, key=key, value=value)
    if result is not None:
        render_message("Secret Added", f"Added secret [cyan]{key}[/cyan].", "green")
    pause()


def delete_space_secret_flow(repo_id: str):
    if not hasattr(api, "delete_space_secret"):
        render_message("Not Supported", "Your installed `huggingface_hub` does not support deleting Space secrets.", "yellow")
        pause()
        return

    key = prompt_text("Secret name to delete", allow_cancel=True)
    if is_back(key):
        return

    if not prompt_confirm(f"Delete secret '{key}'?", default=False):
        return

    result = safe_execute("Deleting Space secret", api.delete_space_secret, repo_id=repo_id, key=key)
    if result is not None:
        render_message("Secret Deleted", f"Deleted secret [cyan]{key}[/cyan].", "green")
    pause()


def add_space_variable_flow(repo_id: str):
    if not hasattr(api, "add_space_variable"):
        render_message("Not Supported", "Your installed `huggingface_hub` does not support Space variables.", "yellow")
        pause()
        return

    key = prompt_text("Variable name", allow_cancel=True)
    if is_back(key):
        return

    value = prompt_text("Variable value", allow_cancel=True)
    if is_back(value):
        return

    result = safe_execute("Adding Space variable", api.add_space_variable, repo_id=repo_id, key=key, value=value)
    if result is not None:
        render_message("Variable Added", f"Added variable [cyan]{key}[/cyan].", "green")
    pause()


def delete_space_variable_flow(repo_id: str):
    if not hasattr(api, "delete_space_variable"):
        render_message("Not Supported", "Your installed `huggingface_hub` does not support deleting Space variables.", "yellow")
        pause()
        return

    key = prompt_text("Variable name to delete", allow_cancel=True)
    if is_back(key):
        return

    if not prompt_confirm(f"Delete variable '{key}'?", default=False):
        return

    result = safe_execute("Deleting Space variable", api.delete_space_variable, repo_id=repo_id, key=key)
    if result is not None:
        render_message("Variable Deleted", f"Deleted variable [cyan]{key}[/cyan].", "green")
    pause()


def account_info_flow(user):
    token = get_token()
    masked = token[:6] + "..." + token[-4:] if token and len(token) > 12 else ("***" if token else "Not available")

    table = Table(title="Account Info", header_style="bold blue", box=ROUNDED)
    table.add_column("Field", style="cyan")
    table.add_column("Value", style="white")
    table.add_row("Name", str(user.get("name", "N/A")))
    table.add_row("Token", masked)
    table.add_row("User Data", truncate_text(user, 300))

    console.print(table)
    pause()


def search_public_flow():
    repo_type = select_repo_type()
    if not repo_type:
        return

    query = prompt_text("Search query", allow_cancel=True)
    if is_back(query):
        return

    repos = fetch_public_repos(repo_type, query)
    if not repos:
        render_message("No Results", "No public repositories found.", "yellow")
        pause()
        return

    clear()
    render_repo_list_table(repos[:100], f"Public {repo_type.title()} Search Results")
    pause()


def space_actions_menu(repo_id: str):
    while True:
        clear()
        console.print(
            Panel.fit(
                f"[bold green]🚀 Space Controls[/bold green]\n[cyan]{repo_id}[/cyan]",
                border_style="green",
                box=HEAVY,
            )
        )
        action = prompt_select(
            "Choose a Space action:",
            [
                Choice("runtime", name="📊 Runtime info"),
                Choice("restart", name="🔄 Restart Space"),
                Choice("pause", name="⏸ Pause Space"),
                Choice("hardware", name="🖥 Request hardware"),
                Choice("sleep", name="😴 Set sleep time"),
                Choice("add_secret", name="🔐 Add secret"),
                Choice("delete_secret", name="❌ Delete secret"),
                Choice("add_variable", name="🧩 Add variable"),
                Choice("delete_variable", name="🗑 Delete variable"),
                back_choice(),
            ],
        )

        if is_back(action):
            return
        if action == "runtime":
            space_runtime_info_flow(repo_id)
        elif action == "restart":
            restart_space_flow(repo_id)
        elif action == "pause":
            pause_space_flow(repo_id)
        elif action == "hardware":
            set_space_hardware_flow(repo_id)
        elif action == "sleep":
            set_space_sleep_time_flow(repo_id)
        elif action == "add_secret":
            add_space_secret_flow(repo_id)
        elif action == "delete_secret":
            delete_space_secret_flow(repo_id)
        elif action == "add_variable":
            add_space_variable_flow(repo_id)
        elif action == "delete_variable":
            delete_space_variable_flow(repo_id)


def repo_actions_menu(username: str, repo_id: str, repo_type: str):
    while True:
        clear()
        console.print(
            Panel.fit(
                f"[bold bright_blue]{repo_type.upper()} REPOSITORY[/bold bright_blue]\n[cyan]{repo_id}[/cyan]",
                border_style="bright_blue",
                box=HEAVY,
            )
        )
        action = prompt_select(
            "Choose an action:",
            [
                Choice("info", name="ℹ️ Repo info"),
                Choice("files", name="📂 List files"),
                Choice("readme", name="📖 Preview README"),
                Choice("upload_file", name="⬆ Upload file"),
                Choice("upload_folder", name="⬆ Upload folder"),
                Choice("download_file", name="⬇ Download file"),
                Choice("delete_files", name="🗑 Delete files"),
                Choice("create_folder", name="📁 Create folder"),
                Choice("visibility", name="🔒 Change visibility"),
                Choice("move", name="✏ Rename / move repo"),
                Choice("discussions", name="💬 List discussions"),
                Choice("new_discussion", name="📝 Create discussion"),
                Choice("comment_discussion", name="💭 Comment on discussion"),
                Choice("space_tools", name="🚀 Space controls" if repo_type == "space" else "🚫 Space controls (Spaces only)"),
                Choice("delete_repo", name="🧨 Delete repo"),
                back_choice(),
            ],
            long_instruction="Every flow supports Back / Cancel",
        )

        if is_back(action):
            return
        if action == "info":
            render_repo_info(repo_id, repo_type)
        elif action == "files":
            list_files_flow(repo_id, repo_type)
        elif action == "readme":
            readme_preview_flow(repo_id, repo_type)
        elif action == "upload_file":
            upload_file_flow(repo_id, repo_type)
        elif action == "upload_folder":
            upload_folder_flow(repo_id, repo_type)
        elif action == "download_file":
            download_file_flow(repo_id, repo_type)
        elif action == "delete_files":
            delete_files_flow(repo_id, repo_type)
        elif action == "create_folder":
            create_folder_flow(repo_id, repo_type)
        elif action == "visibility":
            update_visibility_flow(repo_id, repo_type)
        elif action == "move":
            move_repo_flow(repo_id, repo_type)
        elif action == "discussions":
            list_discussions_flow(repo_id, repo_type)
        elif action == "new_discussion":
            create_discussion_flow(repo_id, repo_type)
        elif action == "comment_discussion":
            comment_discussion_flow(repo_id, repo_type)
        elif action == "space_tools":
            if repo_type != "space":
                render_message("Spaces Only", "Space controls are only available for Space repositories.", "yellow")
                pause()
            else:
                space_actions_menu(repo_id)
        elif action == "delete_repo":
            delete_repo_flow(repo_id, repo_type)


def manage_my_repos_flow(username: str):
    repo_type = select_repo_type()
    if not repo_type:
        return

    repo_id = repo_picker(username, repo_type, public_search=False)
    if repo_id:
        repo_actions_menu(username, repo_id, repo_type)


def browse_public_flow(username: str):
    repo_type = select_repo_type()
    if not repo_type:
        return

    repo_id = repo_picker(username, repo_type, public_search=True)
    if repo_id:
        repo_actions_menu(username, repo_id, repo_type)


def main_menu():
    user = require_login()
    username = user["name"]

    while True:
        render_home(username)
        action = prompt_select(
            "Choose an action:",
            [
                Choice("account", name="👤 Account info"),
                Choice("my_repos", name="📦 Manage my repos"),
                Choice("create_repo", name="➕ Create repo"),
                Choice("search_public", name="🔎 Search public repos"),
                Choice("browse_public", name="🌍 Browse public repo and inspect"),
                Choice("exit", name="❌ Exit"),
            ],
            long_instruction="Interactive Hugging Face Hub terminal dashboard",
        )

        if action == "exit" or is_back(action):
            console.print("[bold green]Goodbye.[/bold green]")
            break
        if action == "account":
            account_info_flow(user)
        elif action == "my_repos":
            manage_my_repos_flow(username)
        elif action == "create_repo":
            create_repo_flow(username)
        elif action == "search_public":
            search_public_flow()
        elif action == "browse_public":
            browse_public_flow(username)


if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        console.print("\n[bold yellow]Exiting safely.[/bold yellow]")

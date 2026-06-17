# Contributing

Thanks for contributing to Hugging Face Terminal Manager V2.

## Development Setup

1. Clone the repository.
2. Create a virtual environment.
3. Install dependencies:

```bash
pip install -r requirements.txt
```
4. Login to Hugging Face if you want to test Hub actions:
```bash
huggingface-cli login
```
5. Run the app:
```bash
python hf_manager_v2.py
```
## Contribution Guidelines

- Keep changes focused and minimal.
- Preserve the interactive terminal-first UX.
- Prefer readable, simple code over clever abstractions.
- Maintain Back / Cancel behavior in every new flow.
- Add clear confirmation for destructive actions.
- Keep compatibility in mind for different huggingface_hub versions.

## Style
- Follow existing code style.
- Use descriptive variable names.
- Keep functions small and task-oriented.
- Use rich for user-facing visual output where appropriate.

## Pull Requests
Please include:
- a short summary of the change
- why the change is useful
- any dependency or compatibility notes
- screenshots or terminal output if the UI changed
- Good First Contributions
- improve menu layout
- add pagination
- improve error messages
- extend Space controls
- add export features
- improve README examples

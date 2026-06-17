# Security Policy

## Supported Use

This project interacts with the Hugging Face Hub and may use personal access tokens. Please handle credentials carefully.

## Reporting a Vulnerability

If you discover a security issue, please do not post secrets or exploit details publicly in an issue.

Instead:
- redact all tokens and private URLs
- provide reproduction steps without exposing credentials
- contact the maintainer privately if possible

## Token Safety

When using this project:

- Never commit Hugging Face tokens to the repository.
- Never paste tokens into screenshots.
- Prefer `huggingface-cli login` over hardcoding tokens in code.
- Use Space secrets for sensitive runtime credentials.
- Do not store secrets in tracked files like `.env` unless excluded properly.

## Recommended Practices

- Use least-privilege tokens where possible.
- Rotate tokens if you believe they were exposed.
- Double-check delete operations before confirming.
- Review repo visibility changes carefully.

## Scope

This tool relies on the public `huggingface_hub` API and local terminal execution. Security of third-party services, user environments, and Hugging Face platform infrastructure is outside the scope of this repository.

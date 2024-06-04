# TF Plan Analyzer

This is a simple tool to analyze the output of a `terraform plan` command.
It will show you the resources that will be created, updated, or deleted.

## Usage

Installation:

```bash
poetry install
```

Show the added, changed, and deleted resources:

```bash
poetry run python main.py added|changed|destroyed path/to/terraform/main.tfplan [--binary terraform]
```

## Development

```bash
# Install dependencies
poetry install

# Format code
poetry run ruff format .
ruff format .
```

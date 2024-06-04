``# TF Plan Analyzer

This is a simple tool to analyze the output of a `terraform plan` command. It will show you the resources that will be created, updated, or deleted, or the diff of a specific resource.

## Usage

Installation:

```bash
poetry install
```

Show the Added, Changed, and Deleted Resources:

```bash
poetry run python main.py added|changed|destroyed path/to/terraform/main.tfplan [--binary tofu|terraform]
```

Show the Diff of a Specific Resource:

```bash
poetry run python main.py diff path/to/terraform/main.tfplan resource.path.name [--binary tofu|terraform]
```

## Development

```bash
# Install dependencies
poetry install

# Format code
poetry run ruff format .
ruff format .
```

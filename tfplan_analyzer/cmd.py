import json
import subprocess
from pathlib import Path
from typing import List

import typer
from pydantic import ValidationError

from tfplan_analyzer.models import Plan


def load_plan(tfpath: str, binary: str):
    try:
        return get_plan(tfpath, binary)
    except Exception as e:
        print(f"Error loading plan: {e}")
        return None


def display_changes(plan, action_filter):
    for change in plan.resource_changes:
        if change.change.actions == [action_filter]:
            print(f"{change.address} ({change.type})")


def check_path(tfpath: str) -> Path:
    path_obj = Path(tfpath)
    if not path_obj.exists():
        typer.echo(f"Error: {tfpath} does not exist.")
        raise typer.Abort()
    return path_obj


def check_software_installed(command: str) -> bool:
    try:
        subprocess.run(
            [command, "--version"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def get_command(tfpath: Path, binary: str = "tofu") -> List[str]:
    commands = {
        "tofu": ["tofu", f"-chdir={tfpath.parent}", "show", "-json", tfpath],
        "terraform": [
            "terraform",
            f"-chdir={tfpath.parent}",
            "show",
            "-json",
            tfpath,
        ],
    }

    if binary not in commands:
        typer.echo(f"Error: {binary} is not a valid binary.")
        raise typer.Abort()

    if not check_software_installed(binary):
        typer.echo(f"Error: {binary} is not installed.")
        raise typer.Abort()

    return commands[binary]


def get_plan(tfpath: str, binary_used: str = "tofu") -> Plan:
    path = check_path(tfpath)
    command = get_command(path, binary_used)
    result = subprocess.run(
        command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    )

    if result.returncode != 0:
        typer.echo(f"Failed to run {binary_used}. Error: {result.stderr}")
        raise typer.Abort()

    plan_json = result.stdout
    try:
        plan_dict = json.loads(plan_json)
        return Plan(**plan_dict)
    except json.JSONDecodeError:
        typer.echo(f"Error: {binary_used} plan is not a valid JSON.")
        raise typer.Abort()
    except ValidationError as e:
        typer.echo(f"Error: JSON does not match the expected schema. {e}")
        raise typer.Abort()

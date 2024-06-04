import difflib
import json
from colorama import init, Fore

# Initialize colorama
init(autoreset=True)

# Constants for action symbols and color mapping
ACTION_SYMBOLS = {"create": "+", "update": "~", "delete": "-"}
COLOR_MAP = {"create": Fore.GREEN, "update": Fore.YELLOW, "delete": Fore.RED}


def format_diff(before, after):
    diff = difflib.unified_diff(
        before.splitlines(), after.splitlines(), lineterm=""
    )
    return "\n".join(diff)


def format_change(action, address, resource_type, before, after):
    symbol = ACTION_SYMBOLS.get(action, "?")
    color = COLOR_MAP.get(action, "")

    lines = []
    if action == "create":
        lines.append(
            f"{color}  {symbol} {resource_type}.{address} will be created"
        )
        lines.extend(format_json_lines(after, color))
    elif action == "delete":
        lines.append(
            f"{color}  {symbol} {resource_type}.{address} will be destroyed"
        )
        lines.extend(format_json_lines(before, color))
    elif action == "update":
        lines.append(
            f"{color}  {symbol} {resource_type}.{address} will be updated in-place"
        )
        diff = format_diff(
            json.dumps(before, indent=2), json.dumps(after, indent=2)
        )
        lines.extend(color_diff_lines(diff))

    return "\n".join(lines)


def format_json_lines(data, color):
    formatted_data = json.dumps(data, indent=2)
    return [f"{color}      {line}" for line in formatted_data.splitlines()]


def color_diff_lines(diff):
    lines = []
    for line in diff.splitlines():
        if line.startswith("+"):
            lines.append(Fore.GREEN + "      " + line)
        elif line.startswith("-"):
            lines.append(Fore.RED + "      " + line)
        else:
            lines.append(Fore.YELLOW + "      " + line)
    return lines

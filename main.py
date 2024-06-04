import typer

from tfplan_analyzer.cmd import load_plan, display_changes
from tfplan_analyzer.diff import format_change

app = typer.Typer()


@app.command()
def added(tfpath: str, binary: str = "tofu"):
    plan = load_plan(tfpath, binary)
    if plan:
        print("Added:\n")
        display_changes(plan, "create")


@app.command()
def changed(tfpath: str, binary: str = "tofu"):
    plan = load_plan(tfpath, binary)
    if plan:
        print("Changed:\n")
        display_changes(plan, "update")


@app.command()
def destroyed(tfpath: str, binary: str = "tofu"):
    plan = load_plan(tfpath, binary)
    if plan:
        print("Destroyed:\n")
        display_changes(plan, "delete")


@app.command()
def diff(tfpath: str, resource: str, binary: str = "tofu") -> None:
    plan = load_plan(tfpath, binary)
    if not plan:
        return

    resource_change = next(
        (
            change
            for change in plan.resource_changes
            if change.address == resource
        ),
        None,
    )
    if not resource_change:
        print(f"No changes found for resource: {resource}")
        return

    action = resource_change.change.actions[0]
    if action == "create":
        after = resource_change.change.after
        output = format_change(
            "create", resource_change.address, resource_change.type, None, after
        )
    elif action == "update":
        before = resource_change.change.before
        after = resource_change.change.after
        output = format_change(
            "update",
            resource_change.address,
            resource_change.type,
            before,
            after,
        )
    elif action == "delete":
        before = resource_change.change.before
        output = format_change(
            "delete",
            resource_change.address,
            resource_change.type,
            before,
            None,
        )
    else:
        output = f"Unsupported action: {resource_change.change.actions}"

    print(output)


if __name__ == "__main__":
    app()

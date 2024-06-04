import typer

from tfplan_analyzer.cmd import get_plan

app = typer.Typer()


@app.command()
def added(tfpath: str, binary: str = "tofu"):
    plan = get_plan(tfpath, binary)
    print("Added:\n")
    for change in plan.resource_changes:
        if change.change.actions == ["create"]:
            print(f"{change.address} ({change.type})")


@app.command()
def changed(tfpath: str):
    plan = get_plan(tfpath)
    print("Changed:\n")
    for change in plan.resource_changes:
        if change.change.actions == ["update"]:
            print(f"{change.address} ({change.type})")


@app.command()
def destroyed(tfpath: str):
    plan = get_plan(tfpath)
    print("Destroyed:\n")
    for change in plan.resource_changes:
        if change.change.actions == ["delete"]:
            print(f"{change.address} ({change.type})")


if __name__ == "__main__":
    app()

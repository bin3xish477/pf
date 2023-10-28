from pathlib import Path
from rich.console import Console

console = Console()


def parse_methods(dir: str, lang: str):
    target_method = None
    target_ext = None

    match lang:
        case "java":
            target_method, target_ext = _parse_java, ".java"
        case "go" | "golang":
            target_method, target_ext = _parse_go, ".go"
        case "rust":
            target_method, target_ext = _parse_rust, ".rs"
        case _:
            console.log(f"[[red]ERRO[/red]]invalid language specified => '{lang}'")
            return

    console.print(f"target_method = {target_method}")
    console.print(f"target_ext    = {target_ext}")

    for _file in Path(dir).rglob(f"*{target_ext}"):
        if _file.is_file():
            target_method(_file.name)


def _parse_java(_file: str):
    console.print(f"[[magenta]INFO[/magenta]] parsing methods in file => '{_file}'")


def _parse_go(_file: str):
    console.print(f"[[magenta]INFO[/magenta]] parsing methods in file => '{_file}'")


def _parse_rust(_file: str):
    console.print(f"[[magenta]INFO[/magenta]] parsing methods in file => '{_file}'")

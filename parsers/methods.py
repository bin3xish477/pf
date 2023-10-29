from pathlib import Path
from rich.console import Console
from concurrent.futures import ThreadPoolExecutor
from os.path import sep
from re import finditer, DOTALL, VERBOSE, MULTILINE

console = Console()

JAVA_METHOD_PROTOTYPE = r"""
    (?P<access_modifier>public|private|protected|default)\s
    ((?P<modifier>static|synchronized|final|abstract|native)\s)?
    (?P<return_type>[a-zA-Z\[\]<>]+)\s
    (?P<method_name>[a-zA-Z_$][a-zA-Z0-9_$]+)(\s+)?
    (?P<params>\(([^)]*)\))
"""


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

    console.log(f"target_method = {target_method}")
    console.log(f"target_ext    = {target_ext}")

    target_files = [
        f"{_file.parent}{sep}{_file.name}"
        for _file in Path(dir).rglob(f"*{target_ext}")
        if _file.is_file()
    ]
    console.log(f"total_files    = {len(target_files)}")

    with ThreadPoolExecutor(max_workers=5) as executor:
        executor.map(target_method, target_files)


def _parse_java(_file: str):
    with open(_file) as f:
        code = f.read()
        for match in finditer(
            JAVA_METHOD_PROTOTYPE, code, DOTALL | MULTILINE | VERBOSE
        ):
            access_modifier = match.group("access_modifier")
            modifier = match.group("modifier")
            return_type = match.group("return_type")
            method_name = match.group("method_name")
            params = match.group("params")
            console.print(
                f"{_file}::[red]{access_modifier}[/red] [yellow]{modifier}[/yellow] [blue]{return_type}[/blue] [green]{method_name}[/green]{params}"
                if modifier
                else f"{_file}::[red]{access_modifier}[/red] [blue]{return_type}[/blue] [green]{method_name}[/green]{params}"
            )


def _parse_go(_file: str):
    console.print(f"[[magenta]INFO[/magenta]] parsing methods in file => '{_file}'")


def _parse_rust(_file: str):
    console.print(f"[[magenta]INFO[/magenta]] parsing methods in file => '{_file}'")

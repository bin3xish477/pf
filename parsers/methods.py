from pathlib import Path
from types import MethodDescriptorType
from rich.console import Console
from concurrent.futures import ThreadPoolExecutor
from os.path import sep
from re import search, DOTALL

console = Console()

JAVA_METHOD_PROTOTYPE = r"(?P<access_modifier>public|private|protected|default)\s((?P<modifier>static|synchronized|final|abstract|native)\s)?(?P<return_type>[a-zA-Z\[\]<>]+)\s(?P<method_name>[a-zA-Z_$][a-zA-Z0-9_$]+)(\s+)?(?P<params>\(([^)]*)\))"

# print(
#    search(
#        JAVA_METHOD_PROTOTYPE,
#        "public static void myMethod(\nint param1,\nString param2\n)",
#        DOTALL,
#    ).group(0)
# )


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

    target_files = [
        f"{_file.parent}{sep}{_file.name}"
        for _file in Path(dir).rglob(f"*{target_ext}")
        if _file.is_file()
    ]
    console.print(f"total_files    = {len(target_files)}")

    with ThreadPoolExecutor(max_workers=5) as executor:
        executor.map(target_method, target_files)


def _parse_java(_file: str):
    with open(_file) as f:
        code = f.read()
        match = search(JAVA_METHOD_PROTOTYPE, code, DOTALL)
        if match:
            capture_groups = match.groupdict()
            access_modifier = capture_groups["access_modifier"]
            modifier = capture_groups["modifier"]
            return_type = capture_groups["return_type"]
            method_name = capture_groups["method_name"]
            params = capture_groups["params"]
            console.print(
                f"{_file}::[green]{access_modifier}[/green] [yellow]{modifier}[/yellow] [blue]{return_type}[/blue] [red]{method_name}[/red] {params}"
                if modifier
                else f"{_file}::[green]{access_modifier}[/green] [blue]{return_type}[/blue] [red]{method_name}[/red] {params}"
            )


def _parse_go(_file: str):
    console.print(f"[[magenta]INFO[/magenta]] parsing methods in file => '{_file}'")


def _parse_rust(_file: str):
    console.print(f"[[magenta]INFO[/magenta]] parsing methods in file => '{_file}'")

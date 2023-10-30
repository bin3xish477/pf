from pathlib import Path
from rich.console import Console
from concurrent.futures import ThreadPoolExecutor
from os.path import sep
from re import finditer, DOTALL, VERBOSE, MULTILINE

console = Console()

JAVA_METHOD_PROTOTYPE = r"""
    (?P<access_modifier>public|private|protected|default)\s+
    ((?P<modifier>static|synchronized|final|abstract|native)\s+)?
    (?P<return_type>[a-zA-Z\[\]<>]+)\s+
    (?P<method_name>[a-zA-Z_$][a-zA-Z0-9_$]+)(\s+)?
    (?P<params>\(([^)]*)\))
"""

GO_FUNC_PROTOTYPE = r"""
    func\s+\((?P<receiver_params>[^)]+)\)\s+
    (?P<function_name>[_a-zA-Z][_a-zA-Z0-9]+)\s+
"""


class Parser:
    def __init__(self, dir: str, lang: str, max_workers: int) -> None:
        self.dir = dir
        self.lang = lang
        self.max_workers = max_workers

    def parse_methods(self):
        target_method = None
        target_ext = None

        match self.lang:
            case "java":
                target_method, target_ext = self._parse_java, ".java"
            case "go" | "golang":
                target_method, target_ext = self._parse_go, ".go"
            case "rust":
                target_method, target_ext = self._parse_rust, ".rs"
            case _:
                console.log(f"[[red]ERRO[/red]]invalid language specified => '{lang}'")
                return

        console.log(f"target_method = {target_method}")
        console.log(f"target_ext    = {target_ext}")

        target_files = [
            f"{_file.parent}{sep}{_file.name}"
            for _file in Path(self.dir).rglob(f"*{target_ext}")
            if _file.is_file()
        ]
        console.log(f"total_files    = {len(target_files)}")

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            executor.map(target_method, target_files)

    def _parse_java(self, _file: str):
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

    # example function prototype
    # func FunctionName [T any] (a, b T) T {}
    # example receiver function
    # func (r Rectangle) Area() float64 {}
    # TODO: remember to account for when generics and return types are not used
    # and also that return can be more than one enclosed in paranthesis.
    def _parse_go(self, _file: str):
        pass

    def _parse_rust(self, _file: str):
        pass

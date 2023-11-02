from pathlib import Path
from rich.console import Console
from concurrent.futures import ThreadPoolExecutor
from os.path import sep
from re import finditer, DOTALL, VERBOSE, MULTILINE


JAVA_METHOD_PROTOTYPE = r"""
    (?P<access_modifier>public|private|protected|default)\s+
    ((?P<modifier>static|synchronized|final|abstract|native)\s+)?
    (?P<return_type>[a-zA-Z\[\]<>]+)\s+
    (?P<method_name>[a-zA-Z_$][a-zA-Z0-9_$]+)\s*
    (?P<params>\(([^):]*)\))
"""

GO_FUNC_PROTOTYPE = r"""
    func\s+(?P<receiver_params>\([^)]+\)\s+)?
    (?P<func_name>[_a-zA-Z][_a-zA-Z0-9]+)\s*
    (?P<type_param_list>[\[a-z\sA-Z\]]+)?\s*
    (?P<func_params>\([^)]*\))\s*
    (?P<return_types>\([^)]*\)|[\w*\[\]]*)?
"""


class Parser:
    def __init__(self, dir: str, lang: str, max_workers: int) -> None:
        self.dir = dir
        self.lang = lang
        self.max_workers = max_workers
        self.console = Console()

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
                self.console.log(
                    f"[[red]ERRO[/red]]invalid language specified => '{lang}'"
                )
                return

        self.console.log(f"target_method = {target_method}")
        self.console.log(f"target_ext    = {target_ext}")

        target_files = [
            f"{_file.parent}{sep}{_file.name}"
            for _file in Path(self.dir).rglob(f"*{target_ext}")
            if _file.is_file()
        ]
        self.console.log(f"total_files    = {len(target_files)}")

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
                self.console.print(
                    f"{_file}::[red]{access_modifier}[/red] [yellow]{modifier}[/yellow] [blue]{return_type}[/blue] [green]{method_name}[/green]{params} {{}}"
                    if modifier
                    else f"{_file}::[red]{access_modifier}[/red] [blue]{return_type}[/blue] [green]{method_name}[/green]{params} {{}}"
                )

    def _parse_go(self, _file: str):
        with open(_file) as f:
            code = f.read()
            for match in finditer(
                GO_FUNC_PROTOTYPE, code, DOTALL | MULTILINE | VERBOSE
            ):
                receiver_params = match.group("receiver_params") or ""
                func_name = match.group("func_name")
                type_param_list = match.group("type_param_list") or ""
                func_params = match.group("func_params")
                return_types = match.group("return_types") or ""
                s = f"{_file}::[red]func[/red] "
                if receiver_params:
                    s += f"[yellow]{receiver_params}[/yellow]"
                s += f"[magenta]{func_name}[/magenta]"
                if type_param_list:
                    s += f"[blue]{type_param_list}[/blue]"
                s += f"[green]{func_params}[/green]"
                if return_types:
                    s += f" [cyan]{return_types}[/cyan]"
                self.console.print(f"{s} {{}}")

    def _parse_rust(self, _file: str):
        pass

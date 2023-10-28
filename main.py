from argparse import ArgumentParser
from rich.console import Console

from parsers.methods import parse_methods


console = Console()


def _parse_args():
    parser = ArgumentParser()
    parser.add_argument("--dir", "-d", help="directory to search for `.java` files")
    parser.add_argument("--lang", "-l", help="language to parse methods for")
    return parser.parse_args()


def main():
    args = _parse_args()
    dir = args.dir
    lang = args.lang

    if not dir:
        console.log("<[red]ERRO[/red]> must provide directory to scan")
        return
    elif not lang:
        console.log("<[ red]ERRO[/ red]> must provide language to parse methods for")
    else:
        console.log(f"<[green]INFO[/green]> scanning {dir} for `.java` files...")
        parse_methods(dir, lang)


if __name__ == "__main__":
    main()

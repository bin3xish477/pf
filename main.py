from argparse import ArgumentParser
from rich.console import Console

from parsers.methods import Parser


console = Console()


def _parse_args():
    parser = ArgumentParser()
    parser.add_argument(
        "--dir", "-d", default=".", help="directory to search for source files"
    )
    parser.add_argument("--lang", "-l", help="language to parse methods for")
    parser.add_argument(
        "--max-workers", "-t", default=5, help="numbers of threads to use"
    )
    return parser.parse_args()


def main():
    args = _parse_args()
    dir = args.dir
    lang = args.lang
    max_workers = args.max_workers

    parser = Parser(dir, lang, max_workers)

    if not lang:
        console.log("<[red]ERRO[/red]> must provide language to parse methods for")
    else:
        console.log(f"<[magenta]INFO[/magenta]> scanning {dir} for `.{lang}` files...")
        parser.parse_methods()


if __name__ == "__main__":
    main()

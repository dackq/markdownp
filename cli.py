"""
Implements argument parsing for the markdownp command line interface. Uses 
argparse.

markdownp <option(s)> <file> 

arguments:
    <file>    :   The path of the file to be parsed.
                If the file is not provided then the file contents are 
                retrieved from stdin.

options:
    --verbose, -v               :   Enable verbose mode
    --encoding, -e <encoding>   :   Set the Unicode encoding to be used. The
                                    Default is UTF-8.
"""

from argparse import ArgumentParser, Namespace

def parse_args(args: list[str]) -> Namespace:
    parser: ArgumentParser = ArgumentParser(
            description="A simple markdown parser."
            )

    # arguments
    parser.add_argument("file",
            help="The path to the file to be parsed", 
            metavar="<file>"
            )

    # options
    parser.add_argument("--verbose", "-v",
            help="Enable verbose mode.",
            action="store_true"
            )

    return parser.parse_args(args)

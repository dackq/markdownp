#! /usr/bin/python3.10
"""
A simple command line program that parses markdown text into html.
"""

import cli
from parsing.parser import Parser
from dom.renderer import render, DOM
from argparse import Namespace
from sys import argv

def main():
    args: Namespace = cli.parse_args(argv[1:])
    
    # setup parsers and renders
    parser: Parser = Parser()

    # parse markdown and render html
    tree: DOM = parser.parse(args.file)
    html: str = render(tree)

    # write markdown to new file
    with open(args.output, "w") as output:
        output.write(html)

if __name__ == "__main__":
    main()

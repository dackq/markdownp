#! /usr/bin/python3.10
"""
A simple command line program that parses markdown text into html.
"""

import cli
from parser import Parser
from dom.renderer import Renderer
from dom.dom_builder import DOM
from argparse import Namespace
from sys import argv

def main():
    args: Namespace = cli.parse_args(argv[1:])
    
    # setup parsers and renders
    parser: Parser = Parser()
    renderer: Renderer = Renderer()

    # parse markdown and render html
    with open(args.file, "w") as file:
        tree: DOM = parser.parse(file)
        html: str = renderer.render(tree)

    # write markdown to new file
    with open(args.output, "w") as output:
        output.write(html)

if __name__ == "__main__":
    main()

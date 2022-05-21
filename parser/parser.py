"""
Simple parser for markdownp
"""
from io import TextIOBase
from block_parser import BlockParser
from inline_parser import InlineParser
from ..dom.renderer import DOM
# set path to parent directory so we can import other packages

class Parser(object):
    open("file")
    def parse(self, file: TextIOBase) -> DOM:
        file.readline()
        pass


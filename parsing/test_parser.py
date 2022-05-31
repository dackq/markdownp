"""
Tests for the markdownp parser module
"""

import unittest
from textwrap import dedent
from dom.renderer import render, DOM
from parsing.parser import BlockParser
from io import StringIO

class ParserTests(unittest.TestCase):
    def run_test(self, markdown, expected_dom):
        parser: BlockParser = BlockParser()
        stream: StringIO = StringIO(markdown)

        parsed_dom: DOM = parser.parse(stream)
        html = render(parsed_dom)

        self.assertEqual(html, expected_dom)


    def test_paragraph(self):
        markdown: str = """
This is a paragraph.
And this is another part of the paragraph
And this is the end.

This is a new paragraph, and this is the end of it.
        """
        expected: str = "<html><p>This is a paragraph.\nAnd this is another part of the paragraph\nAnd this is the end.</p><p>This is a new paragraph, and this is the end of it.</p></html>"

        self.run_test(markdown, expected)

        markdown: str = """
this is a paragraph
    with an indented line after it
        """
        expected: str = "<html><p>this is a paragraph\nwith an indented line after it</p></html>"
        self.run_test(markdown, expected)


    def test_atx_header(self):
        markdown: str = """
# header number 1
        """
        expected: str = "<html><h1>header number 1</h1></html>"
        self.run_test(markdown, expected)

        markdown: str = """
## header number 2
        """
        expected: str = "<html><h2>header number 2</h2></html>"
        self.run_test(markdown, expected)

        markdown: str = """
### header number 3
#### header number 4###     
##### header number 5 ##
###### header number 6 ###
        """
        expected: str = "<html><h3>header number 3</h3><h4>header number 4</h4><h5>header number 5</h5><h6>header number 6</h6></html>"
        self.run_test(markdown, expected)

        markdown: str = """
##this doesn't work
        """
        expected: str = "<html><p>##this doesn't work</p></html>"
        self.run_test(markdown, expected)

    def test_headers_and_paragraphs(self):
        markdown: str = """
this is a paragraph followed by a header
## header number 2
        """
        expected: str = "<html><p>this is a paragraph followed by a header</p><h2>header number 2</h2></html>"
        self.run_test(markdown, expected)


if __name__ == '__main__':
    unittest.main()

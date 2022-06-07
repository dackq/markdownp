"""
Simple parser for markdownp
"""
from io import TextIOBase
from dom.renderer import DOM
from parsing.tokenizer import BlockTokenizer
import re

class Parser(object):
    def parse(self, path: str) -> DOM:
        with open(path) as file:
            block_parser: BlockParser = BlockParser()
            inline_parser: InlineParser = InlineParser()
            dom: DOM = block_parser.parse(file)
            dom = inline_parser.parse(dom)
            return dom

class BlockParser(object):
    def parse(self, file: TextIOBase) -> DOM:
        self._tokenizer = BlockTokenizer(file)
        self._lookahead = self._tokenizer.get_next_token()

        return self._html()

    def _eat(self, expected_type: str) -> dict[str,str]:
        """
        Consume the lookahead and set the lookahead to the next token
        """
        if self._lookahead["type"] == expected_type:
            old_token = self._lookahead
            self._lookahead = self._tokenizer.get_next_token()
            return old_token

        raise SyntaxError(f"Received unexpected line {self._lookahead}, "
                f"expected {expected_type}")

    def _eat_rest_of_line(self) -> str:
        """
        Consume entire stream until the next '\\n' character.

        Used when token values for a line should be ignored.
        """
        # the line is the current token + any remaining text in the line
        line: str = self._lookahead["value"] + self._tokenizer.get_rest_of_line()
        self._lookahead = self._tokenizer.get_next_token()
        return line
    
    def _html(self) -> DOM:
        return DOM('html', children=self._element_list())
        
    def _element_list(self) -> list[DOM | str]:
        """
        ElementList:
            : ElementList Element
            | Element
            ;
        """
        elements: list[DOM | str] = []
        while self._lookahead["type"] != "EOF":
            next_element: DOM | None = self._element()
            if next_element:
                elements.append(next_element)

        return elements

    def _element(self) -> DOM | None:
        """
        Element
            :   AtxHeader
            |   Paragraph
            ;
        """
        if self._lookahead["type"] == "BLANK_LINE":
            # if there is a blank line here then skip it
            self._eat("BLANK_LINE")
            return
        if self._lookahead["type"] == "ATX_HEADER":
            return self._atx_header()
        if self._lookahead["type"] == "INDENT":
            return self._code_block()

        # otherwise treat as a paragraph
        return self._paragraph()

    def _code_block(self) -> DOM:
        """
        CodeBlock
            : CodeBlock IndentLine
            | IndentLine
            ;
        """
        contents: list[DOM | str] = [DOM('code', children=[self._indent_line()])]
        while self._lookahead["type"] == "INDENT":
            contents.append(DOM('code', children=[self._indent_line()]))

        return DOM('pre', children=contents)

    def _indent_line(self) -> str:
        """
        IndentLine
            : INDENT LINE
            ;

        LINE = the rest of the line it will not be analyzed as a token
        """
        self._eat("INDENT")
        return self._eat_rest_of_line()

    def _atx_header(self) -> DOM:
        """
        AtxHeader
            : ATX_HEADER
            ;
        """

        header:str = self._eat("ATX_HEADER")["value"]
        
        # we need to figure out how many '#'s there are
        matched: re.Match[str] | None = re.match("#{1,6}", header)
        if matched:
            header_level: int = len(matched.group())

            return DOM(f"h{header_level}", children=[header.strip(" \t#")])

        raise SyntaxError(f"Incorrect header format. Received {header}, "
                "expected 1-6 # characters leading")
        
    def _paragraph(self) -> DOM:
        # paragraph should end if it is followed by anything other than
        # TEXT_LINE, INDENT_LINE,  but it can have multiple of them.
        # I'm not sure the best way to write this but here is a stab
        # at it
        """
        Paragraph
            : TEXT_LINE Paragraph
            | ParagraphContinuationLine
            | None
            ;
        """
        contents: str = self._eat("TEXT_LINE")["value"]

        while (
            self._lookahead["type"] == "TEXT_LINE" 
            or self._lookahead["type"] == "INDENT"
                ):
            # we append the stripped contents of this line to the paragraph
            # contents and consume the token
            contents += f"\n{self._p_continuation_line().strip()}"

        return DOM('p', children=[contents])

    def _p_continuation_line(self) -> str:
        """
        ParagraphContinuationLine
            : TEXT_LINE
            | IndentLine
            ;
        """
        if self._lookahead["type"] == "TEXT_LINE":
            return self._eat("TEXT_LINE")["value"]
        else:
            return self._indent_line()
        

class InlineParser(object):
    def parse(self, dom: DOM):
        return dom

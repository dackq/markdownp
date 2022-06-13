"""
Simple parser for markdownp
"""
from io import TextIOBase
from dom.renderer import DOM
from parsing.tokenizer import BlockTokenizer
import re
from typing import Union

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
        self._open_block_stack: list[DOM] = []

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

    def _write_to_current_open_block(self, *items: Union['DOM', str]):
        """
        Writes the provided items to the children of the top element in the 
        open_block_stack.
        """
        self._open_block_stack[-1].children.extend(items)

    def _open_block(self, block_type: str):
        """
        Pushes given block to the open block stack and updates the current block
        pointer.
        """
        self._open_block_stack.append(DOM(block_type))

    def _close_block(self) -> DOM:
        """
        Pops the current block off of the stack and returns it
        """
        return self._open_block_stack.pop()
    
    def _html(self) -> DOM:
        self._open_block('html')
        self._write_to_current_open_block(self._body())
        return self._close_block()

    def _body(self) -> DOM:
        """
        Body
            : ElementList
            ;
        """
        self._open_block('body')
        self._write_to_current_open_block(*self._element_list())
        return self._close_block()


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
            |   CodeBlock
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
        self._open_block('pre')
        self._open_block('code')
        self._write_to_current_open_block(self._indent_line())
        while self._lookahead["type"] == "INDENT":
            self._write_to_current_open_block('\n'+self._indent_line())
        self._write_to_current_open_block(self._close_block())
        return self._close_block()

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
        self._open_block('p')
        self._write_to_current_open_block(self._eat("TEXT_LINE")["value"])

        while (
            self._lookahead["type"] == "TEXT_LINE" 
            or self._lookahead["type"] == "INDENT"
                ):
            # we append the stripped contents of this line to the paragraph
            # contents and consume the token
            self._write_to_current_open_block(f"\n{self._p_continuation_line().strip()}")

        return self._close_block()

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

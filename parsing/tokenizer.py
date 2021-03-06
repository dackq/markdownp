"""
Tokenizers for markdownp
"""
from io import TextIOBase
import re

block_spec: tuple[tuple[str, str], ...] = (
    # indent (four spaces)
    ("( {4})", "INDENT"),
    # whitespace (any amount of spaces less than four (INDENT))
    ("( *)", "WHITESPACE"),
    # ordered
    (" *\\d+\\. .*", "OL_LINE"),
    # headers
    ("#{1,6} .+", "ATX_HEADER"),
)


class BlockTokenizer(object):
    """
    Lazily returns token based on the block structures of a markdown
    document.
    """

    def __init__(self, stream: TextIOBase):
        self._stream: TextIOBase = stream
        self._current_line: str = ""
        self._cursor: int = 0

    def _match_line(self, regexp: str, string: str):
        matched: re.Match[str] | None = re.compile(regexp).match(
            string, pos=self._cursor
        )

        if matched == None:
            return None

        # if there was a match then advance the cursor
        self._cursor += len(matched.group())

        return matched.group()

    def get_rest_of_line(self) -> str:
        """
        Returns the rest of the line as a string without trying to analyze any
        tokens.

        This is used when a specific structure ignores the token value of a line
        and just returns a string of plane text. (For example, in a code block)
        """
        line: str = self._current_line[
            self._cursor : -1
        ]  # skip the new line at the end
        self._cursor = len(self._current_line)
        return line

    def get_next_token(self) -> dict[str, str]:
        """
        Grab the next token off the stream
        """
        # lazily load the next line
        # if the entire current line has been tokenized
        # subtract 1 from length 1 for the new line at the end
        if self._cursor >= len(self._current_line) - 1:
            # get the next line from the stream
            self._current_line = self._stream.readline()
            self._cursor = 0  # reset cursor

            # if there are no more lines in the stream return EOF
            if self._current_line == "":
                return {"type": "EOF"}

            # check if the line is blank
            if re.match("^([ \\t]*)$", self._current_line):
                self._cursor = len(self._current_line)
                return {"type": "BLANK_LINE"}

            # replace all \t with four spaces
            self._current_line = self._current_line.replace("\t", "    ")

        # try to match with each pattern in block_spec
        for pattern in block_spec:
            token: str | None = self._match_line(pattern[0], self._current_line)

            # if there is a match then return it
            if token != None:
                # special case tokens
                if pattern[1] == "WHITESPACE":
                    # skip whitespace
                    continue
                elif pattern[1] == "INDENT":
                    return {"type": pattern[1], "value": "\t"}
                elif pattern[1] == "BLOCK":
                    return {"type": pattern[1], "value": ""}

                # all other token types are returned here
                return {"type": pattern[1], "value": token.strip()}

        # if the line does not match any pattern then we just return a normal
        # text line
        text_line = {
            "type": "TEXT_LINE",
            "value": self._current_line[self._cursor :].strip(),
        }

        # and advance the cursor
        self._cursor = len(self._current_line)
        return text_line

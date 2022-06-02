"""
Tokenizers for markdownp
"""
from io import TextIOBase
import re

block_spec: tuple[tuple[str, str], ...] = (
    # blank lines
    ('[ \\t]*', 'BLANK_LINE'),

    # indented lines
    ('(?: {4,}|\t).*', 'INDENT_LINE'),

    # list lines
    # unordered
    (' *[-*] .*', 'UL_LINE'),

    # ordered
    (' *\\d+\\. .*', 'OL_LINE'),

    # headers
    (' *(#{1,6} .+)', 'ATX_HEADER'),
)

class BlockTokenizer(object):
    """
    Lazily returns token based on the block structures of a markdown 
    document. Each token is equivalent to an entire line in the 
    markdown file.
    """
    def __init__(self, stream: TextIOBase):
        self._stream = stream

    def _match_line(self, regexp: str, string: str):
        matched: re.Match[str] | None = re.compile('^' + regexp + '$').match(string)

        if matched == None:
            return None
        
        return matched.group(0)

    def get_next_token(self) -> dict[str, str]:
        # get the next line from the stream
        next_line: str = self._stream.readline()

        # if there are no more lines in the stream return none
        if next_line == "":
            return {
                "type": "EOF"
            }

        # try to match with each pattern in block_spec
        for pattern in block_spec:
            token: str | None = self._match_line(pattern[0], next_line)

            # if there is a match then return it
            if token != None:
                if pattern[1] == 'BLANK_LINE':
                    # no need for value if line is blank
                    return {
                        "type": "BLANK_LINE"
                    }
                return {
                    "type": pattern[1],
                    "value": token
            }

        # if the line does not meatch any pattern then we just return a normal
        # text line
        return {
                "type": "TEXT_LINE",
                "value": next_line.strip()
        }

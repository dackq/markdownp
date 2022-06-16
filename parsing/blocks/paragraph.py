"""
Definition of the paragraph block.

TODO
[Insert Definition Here]
"""
from parsing.blocks.default_blocks import BlockDefinition
from dom.renderer import DOM

def _can_continue(next_token: str) -> bool:
    if next_token == "INDENT" or next_token == "NEXT_LINE":
        return True
    return False

def _can_contain(next_token: str) -> bool:
    return False

def _finalize(block: DOM):
    pass

def _start(next_token: str) -> bool:
    """
    Paragraph start. A paragraph will only be started if the line is not blank and no other line can be parsed.
    """
    return False

paragraph: BlockDefinition = BlockDefinition(
    block_type='paragraph', 
    can_continue=_can_continue,
    can_contain=_can_contain,
    finalize=_finalize,
    start=_start
    )
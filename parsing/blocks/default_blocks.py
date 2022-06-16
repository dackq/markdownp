"""
Dictionary of all default blocks used by the parser
"""

from typing import Callable
from dom.renderer import DOM
from parsing.blocks.paragraph import paragraph


class BlockDefinition(object):
    def __init__(
        self,
        *,
        block_type: str,
        can_continue: Callable[[str], bool],
        can_contain: Callable[[str], bool],
        start: Callable[[str], bool],
        finalize: Callable[[DOM], None]
    ):
        self.type = block_type
        self.can_continue = can_continue
        self.can_contain = can_contain
        self.start = start
        self.finalize = finalize


default_blocks: dict[str, BlockDefinition] = {"paragraph": paragraph}

default_block_starts: list[Callable[[str], bool]] = [paragraph.start]

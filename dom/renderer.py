"""
Renderer for html files from DOM objects
"""

from typing import Union

class DOM(object):
    """
    Used to represent a node in an HTML document object model
    """
    def __init__(self: 'DOM', element: str, *, children: list[Union['DOM', str]]=[]):
        self.element: str = element
        self.children: list[Union[DOM, str]] = [*children]

    def __str__(self):
        return _build_node(self)

def render(tree: DOM) -> str:
    return _build_node(tree)
    
def _build_node(node: DOM) -> str:
    """
    Recursively builds html elements from a DOM until there are no
    children left
    """
    element = node.element
    children = node.children

    html: str = f"<{element}>"
    for next_node in children: 
        # if next_node is a str then it will be appeneded
        # if it is a DOM then _build node is called again
        html = f"{html}{next_node}"

    html += f"</{element}>"

    return html

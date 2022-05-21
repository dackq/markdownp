"""
Renderer for html files from DOM objects
"""
class DOM(object):
    """
    Used to represent a node in an HTML document object model
    """

    def __init__(self: 'DOM', element: str, *, children: list['DOM']=[], text: str=""):
        self.element: str = element
        self.children: list[DOM] = children

        # The text field is a special case used to contain actual text not html 
        # For example the text in <p>text</p>. It should be used with the 
        # element name "text".
        #
        # So <p>text</p> would be a DOM object more or less like this: 
        # (written in json)
        #   DOM = {
        #       "element": "p",
        #       "children": {
        #           "element": "text",
        #           "children": [].
        #           "text": "text"
        #        }
        #       "text": ""
        #   }
        #
        # It is implemented this way so that children can be type list['DOM']
        # rather than list['DOM' | str], as list['DOM' | str] was 
        # causing problems with the type checker.
        self.text: str = text

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
        if next_node.element == "text":
            html += next_node.text
        else:
            html += _build_node(next_node)
    html += f"</{element}>"

    return html

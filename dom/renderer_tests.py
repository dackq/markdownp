import unittest

from renderer import DOM, render


class Tests(unittest.TestCase):
    def setup(self):
        pass

    def test_paragraph(self):
        paragraph: DOM = DOM("p", children=["Hello there"])

        html = render(paragraph)

        expected = "<p>Hello there</p>"

        self.assertEquals(html, expected)

    def test_html_object(self):
        paragraph: DOM = DOM("p", children=["Hello there"])
        html: DOM = DOM("html", children=[paragraph, paragraph])

        actual = render(html)
        expected = "<html><p>Hello there</p><p>Hello there</p></html>"

        self.assertEquals(actual, expected)


if __name__ == "__main__":
    unittest.main()

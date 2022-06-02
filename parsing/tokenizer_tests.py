"""
Unit test cases for markdownp tokenizer
"""
from unittest import TestCase, main
from tokenizer import BlockTokenizer
from io import StringIO

class BlockTokenizerTests(TestCase):
    def setup(self):
        pass

    def run_test(self, text: str, expected: tuple[dict[str,str], ...], tokenizer_type: str = ...):
        stream: StringIO = StringIO(text)

        if tokenizer_type == 'block':
            tokenizer = BlockTokenizer(stream)
        # elif tokenizer_type == 'inline':
            # TODO put inline tokenizer here
             # pass
        else:
            self.fail("Can only run test with 'block' or 'inline' tokenizer")
        
        for i in range(0, len(expected)):
            self.assertEqual(expected[i], tokenizer.get_next_token())

        # assert there are no more tokens left
        self.assertEqual(None, tokenizer.get_next_token())


    def test_blank_line(self):
        text: str = "\n"
        expected: tuple[dict[str, str], ...] = (
                {"type": "BLANK_LINE"},
        )
        self.run_test(text, expected, tokenizer_type='block')


        text: str = " \n"
        expected: tuple[dict[str, str], ...] = (
                {"type": "BLANK_LINE"},
        )
        self.run_test(text, expected, tokenizer_type='block')

        text: str = "\t\n"
        expected: tuple[dict[str, str], ...] = (
                {"type": "BLANK_LINE"},
        )
        self.run_test(text, expected, tokenizer_type='block')

        text: str = "\t  \t\n\n"
        expected: tuple[dict[str, str], ...] = (
                {"type": "BLANK_LINE"},
                {"type": "BLANK_LINE"},
        )
        self.run_test(text, expected, tokenizer_type='block')

    def test_indent(self):
        text: str = "    indented line"
        expected: tuple[dict[str, str], ...] = (
                {"type": "INDENT"},
                {"type": "TEXT_LINE", "value": "indented line"}
        )
        self.run_test(text, expected, tokenizer_type='block')


    def test_text_line(self):
        text: str = "hello there"
        expected: tuple[dict[str, str], ...] = (
                {"type": "TEXT_LINE", "value": "hello there"},
        )
        self.run_test(text, expected, tokenizer_type='block')

        text: str = "hello there\n"
        expected: tuple[dict[str, str], ...] = (
                {"type": "TEXT_LINE", "value": "hello there"},
        )
        self.run_test(text, expected, tokenizer_type='block')
        
        text: str = "hello there\n   Nice to see you"
        expected: tuple[dict[str, str], ...] = (
                {"type": "TEXT_LINE", "value": "hello there"},
                {"type": "TEXT_LINE", "value": "Nice to see you"},
        )
        self.run_test(text, expected, tokenizer_type='block')

        text: str = "#hello there\n Tortoise\n"
        expected: tuple[dict[str, str], ...] = (
                {"type": "TEXT_LINE", "value": "#hello there"},
                {"type": "TEXT_LINE", "value": "Tortoise"},
        )
        self.run_test(text, expected, tokenizer_type='block')

    def test_atx_header_lines(self):
        text: str = "## hello there\n"
        expected: tuple[dict[str, str], ...] = (
                {"type": "ATX_HEADER", "value": "## hello there"},
        )
        self.run_test(text, expected, tokenizer_type='block')
        

    def test_mixed_lines(self):
        text: str = "hello there\n\n"
        expected: tuple[dict[str, str], ...] = (
                {"type": "TEXT_LINE", "value": "hello there"},
                {"type": "BLANK_LINE"},
        )
        self.run_test(text, expected, tokenizer_type='block')

        text: str = "\nhello there\nanother line    \n\n"
        expected: tuple[dict[str, str], ...] = (
                {"type": "BLANK_LINE"},
                {"type": "TEXT_LINE", "value": "hello there"},
                {"type": "TEXT_LINE", "value": "another line"},
                {"type": "BLANK_LINE"},
        )
        self.run_test(text, expected, tokenizer_type='block')

        text: str = "this is a line\n\tthis is indented"
        expected: tuple[dict[str, str], ...] = (
                {"type": "TEXT_LINE", "value": "this is a line"},
                {"type": "INDENT"},
                {"type": "TEXT_LINE", "value": "this is indented"},
                )
        self.run_test(text, expected, tokenizer_type='block')
        

if __name__ == '__main__':
    main()

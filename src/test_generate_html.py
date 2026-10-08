# static-sitegen src/generate_html
#
#
#
#
#
#
#
#
#

import unittest

from generate_html import extract_title

class TestGeneratePages(unittest.TestCase):

    def test_extract_title(self):
        markdown = ["# first heading", "#first heading\n\n# second heading", "#first heading\n\n## second heading\n\n# third", "## first heading\n\n# second heading"]
        markdown.append("""
    # not this one
        # or this one
            # not this other one
# but this one
#and not this one
# and not this one either

""")
        markdown.append("""
    # not this one
## or this one
**or this **# one
            # not this other one
_# nor this one I put here_
# but this one
#and not this one
# and not this one either

""")
        test_escape = '# &"' + "'<>test"
        markdown.extend(["#        hihi        ", "not this\n\n#      but this one                      ", test_escape])
        extracted = list(map(extract_title, markdown))
        expected = ['first heading', 'second heading', 'third', 'second heading', 'but this one', 'but this one', 'hihi', 'but this one', "&amp;&quot;&#039;&lt;&gt;test"]
        self.assertEqual(extracted, expected)

    def test_extract_title_error(self):
        with self.assertRaises(ValueError) as raised:
            markdown = '#one\n\n**# two**\n\n     # three\n\n## four'
            extracted = extract_title(markdown)
        self.assertEqual(str(raised.exception), 'top level header is missing from markdown')

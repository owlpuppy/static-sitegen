#static-sitegen src/text_convert_markdown
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
from textnode import TextType, TextNode, text_node_to_html_node
from convert_markdown_block import BlockType, markdown_to_blocks, block_to_block_type, markdown_to_html_node

class TestConvertMarkdownBlock(unittest.TestCase):

    # convert markdown to blocks

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_long(self):
        md_long = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line
This is another paragraph.


- This is a list
- with items






    This shouldn't have a tab. And this sentence should be included too, with [a link.](http://address.fake)
And this sentence should be a part of the same paragraph.


This one should not.
        And this should be here.
"""
        blocks = markdown_to_blocks(md_long)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line\nThis is another paragraph.",
                "- This is a list\n- with items",
                "This shouldn't have a tab. And this sentence should be included too, with [a link.](http://address.fake)\nAnd this sentence should be a part of the same paragraph.",
                "This one should not.\n        And this should be here."
            ],
        )

    # block to block type tests

    def test_block_to_block_type_headings(self):
        blocks = [
            "# text",
            "## moretext//\4fghjddv q",
            "### stillmoretext",
            "#### b",
            "##### five",
            "###### six",
            "####### seven",
            "### ",
            "#3",
            " #",
            "`# one",
            "> # sssss",
            "\n# sssss"
        ]
        results = []
        for block in blocks:
            results.append(block_to_block_type(block))
        expected = [
            BlockType.HEADING,
            BlockType.HEADING,
            BlockType.HEADING,
            BlockType.HEADING,
            BlockType.HEADING,
            BlockType.HEADING,
            BlockType.PARA,
            BlockType.PARA,
            BlockType.PARA,
            BlockType.PARA,
            BlockType.PARA,
            BlockType.QUOTE,
            BlockType.PARA
        ]
        self.assertEqual(results, expected)

    def test_block_to_block_type_code(self):
        blocks = [
            "```\nsometest```",
            "```\nsometest``",
            "``\nsometest```",
            "```sometest```",
            " ```\nsometest```",
            "```\nsometest``` ",
            "```\nsometest\nsomemoretest```",
            "```\n   sometest   ```",
            "```\nsometest   ``   ```",
            "```\n### heading```",
            "# one",
            ">```sometest``` # sssss"
        ]
        results = []
        for block in blocks:
            results.append(block_to_block_type(block))
        expected = [
            BlockType.PRE,
            BlockType.PARA,
            BlockType.PARA,
            BlockType.PARA,
            BlockType.PARA,
            BlockType.PARA,
            BlockType.PRE,
            BlockType.PRE,
            BlockType.PRE,
            BlockType.PRE,
            BlockType.HEADING,
            BlockType.QUOTE
        ]
        self.assertEqual(results, expected)

    def test_block_to_block_type_quote(self):
        blocks = [
            "```\n> quote```",
            "```\n>quote``",
            "## >me",
            "> ",
            ">text ",
            ">   text",
            "> text",
            "\n> text"
        ]
        results = []
        for block in blocks:
            results.append(block_to_block_type(block))
        expected = [
            BlockType.PRE,
            BlockType.PARA,
            BlockType.HEADING,
            BlockType.PARA,
            BlockType.QUOTE,
            BlockType.QUOTE,
            BlockType.QUOTE,
            BlockType.PARA
        ]
        self.assertEqual(results, expected)

    def test_block_to_block_type_ul(self):
        blocks = [
            "\n- an item",
            "- an item",
            "- an item\n- an item",
            "- an item\n- an item\n- an item",
            " - an item\n- an item\n- an item",
            "- an item\n- an item\n - an item",
            "- an item\n - an item\n- an item",
            "- an item\n\n- an item\n- an item"
        ]
        results = []
        for block in blocks:
            results.append(block_to_block_type(block))
        expected = [
            BlockType.PARA,
            BlockType.UL,
            BlockType.UL,
            BlockType.UL,
            BlockType.PARA,
            BlockType.PARA,
            BlockType.PARA,
            BlockType.PARA
        ]
        self.assertEqual(results, expected)

    def test_block_to_block_type_ol(self):
        blocks = [
            "\n- an item",
            "1- an item",
            "1.- an item",
            "1. an item\n- an item\n- an item",
            "1. an item\n2. an item\n3. an item",
            "\n1. an item\n2. an item\n3. an item",
            "1. an item\n3. an item\n2. an item",
            "2. an item\n3. an item",
            "1. an item\n2. an item\n"
        ]
        results = []
        for block in blocks:
            results.append(block_to_block_type(block))
        expected = [
            BlockType.PARA,
            BlockType.PARA,
            BlockType.PARA,
            BlockType.PARA,
            BlockType.OL,
            BlockType.PARA,
            BlockType.PARA,
            BlockType.PARA,
            BlockType.OL
        ]
        self.assertEqual(results, expected)

    # markdown to htmlnode tests

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <strong>bolded</strong> paragraph text in a p tag here</p><p>This is another paragraph with <em>italic</em> text and <code>code</code> here</p></div>",
        )


    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_all(self):
        md = """
#  first heading

This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

- _first_
- second ![alt](address)

## second heading

### third

```
This is text that _should_ remain
the **same** even with inline stuff
```

1. one
2. two
3. three **and** more
4. [four](no)

>one
>two
>three

#### fourth **with a link?** [four](yes) maybe

"""
        compare = "<div>"
        compare += "<h1>first heading</h1>"
        compare += "<p>This is <strong>bolded</strong> paragraph text in a p tag here</p>"
        compare += "<p>This is another paragraph with <em>italic</em> text and <code>code</code> here</p>"
        compare += '<ul><li><em>first</em></li><li>second <img src="address" alt="alt"></li></ul>'
        compare += '<h2>second heading</h2><h3>third</h3>'
        compare += "<pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre>"
        compare += '<ol><li>one</li><li>two</li><li>three <strong>and</strong> more</li><li><a href="no">four</a></li></ol>'
        compare += '<blockquote>one two three</blockquote>'
        compare += '<h4>fourth <strong>with a link?</strong> <a href="yes">four</a> maybe</h4>'
        compare += "</div>"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, compare)

           # "<div><p>This is <strong>bolded</strong> paragraph text in a p tag here</p><p>This is another paragraph with <em>italic</em> text and <code>code</code> here</p><ul><li>first</li><li>second</li></ul><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",

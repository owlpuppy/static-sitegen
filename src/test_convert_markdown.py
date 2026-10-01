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
from convert_markdown import split_nodes_delimiter


class TestConvertMarkdown(unittest.TestCase):
    def test_convert_markdown_long(self):
        node = TextNode("`This is a test`, and `only` a `test`. This is text with a `code block` word. Wow this `might be hard. `", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        node2 = [TextNode('This is a test', TextType.CODE),
            TextNode(', and ', TextType.TEXT),
            TextNode('only', TextType.CODE),
            TextNode(' a ', TextType.TEXT),
            TextNode('test', TextType.CODE),
            TextNode('. This is text with a ', TextType.TEXT),
            TextNode('code block', TextType.CODE),
            TextNode(' word. Wow this ', TextType.TEXT),
            TextNode('might be hard. ', TextType.CODE)]
        self.assertEqual(new_nodes, node2)

    def test_convert_markdown_only_codeblocks(self):
        node = TextNode("`block1``block2``block3`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        node2 = [TextNode('block1', TextType.CODE), TextNode('block2', TextType.CODE), TextNode('block3', TextType.CODE)]
        self.assertEqual(new_nodes, node2)

    def test_convert_markdown_italic_mixed(self):
        node = TextNode("block0_block1_block2_block3__block4_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        node2 = [TextNode('block0', TextType.TEXT), TextNode('block1', TextType.ITALIC), TextNode('block2', TextType.TEXT), TextNode('block3', TextType.ITALIC), TextNode('block4', TextType.ITALIC)]
        self.assertEqual(new_nodes, node2)

    def test_convert_markdown_italic_multi(self):
        nodes = [TextNode("block0_block1_", TextType.TEXT), TextNode("block2", TextType.TEXT), TextNode("_block3__block4_", TextType.TEXT)]
        new_nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
        node2 = [TextNode('block0', TextType.TEXT), TextNode('block1', TextType.ITALIC), TextNode('block2', TextType.TEXT),
            TextNode('block3', TextType.ITALIC), TextNode('block4', TextType.ITALIC)]
        self.assertEqual(new_nodes, node2)

    def test_convert_markdown_multi_prev_parsed(self):
        nodes = [TextNode("block0_block1_hmm**hmm**", TextType.TEXT), TextNode("block2", TextType.BOLD), TextNode("_block3__block4`block5`_", TextType.TEXT)]
        new_nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
        node2 = [TextNode('block0', TextType.TEXT), TextNode('block1', TextType.ITALIC), TextNode('hmm**hmm**', TextType.TEXT),
            TextNode('block2', TextType.BOLD), TextNode('block3', TextType.ITALIC), TextNode('block4`block5`', TextType.ITALIC)]
        self.assertEqual(new_nodes, node2)

    def test_convert_to_markdown_typerrror(self):
        with self.assertRaises(TypeError) as raised:
            node = TextNode("**block1****block2block3", TextType.TEXT)
            new_node = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(str(raised.exception), 'syntax error, closing "**" not found')

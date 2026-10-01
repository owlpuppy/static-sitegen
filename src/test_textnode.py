#static-sitegen src/text_textnode
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


class TestTextNode(unittest.TestCase):
    def test_textnode_is_bold(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_textnode_is_text(self):
        node = TextNode("This is another text node", TextType.TEXT)
        node2 = TextNode("This is another text node", TextType.TEXT)
        self.assertEqual(node, node2)

    def test_textnode_link_different(self):
        node = TextNode("link1", TextType.LINK)
        node2 = TextNode("link1", TextType.LINK, 'url')
        self.assertNotEqual(node, node2)

    def test_textnode_link_vs_url(self):
        node = TextNode("link2", TextType.LINK, 'url')
        node2 = TextNode("link2", TextType.IMG, 'url')
        self.assertNotEqual(node, node2)

    def test_textnode_italic_notequal(self):
        node = TextNode("This is a text node", TextType.ITALIC, 'url')
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_textnode_img_equal(self):
        node = TextNode("This is another text node", TextType.IMG, 'url')
        node2 = TextNode("This is another text node", TextType.IMG, 'url')
        self.assertEqual(node, node2)

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
        self.assertEqual(html_node.to_html(), "This is a text node")

    def test_bold(self):
        node = TextNode("Am I Bold?", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.value, "Am I Bold?")
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.to_html(), "<b>Am I Bold?</b>")

    def test_link(self):
        node = TextNode("Am I LINKED?", TextType.LINK, "the_url")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Am I LINKED?")
        self.assertEqual(html_node.props, {'href': 'the_url'})
        self.assertEqual(html_node.to_html(), '<a href="the_url">Am I LINKED?</a>')

    def test_parentnode_to_html_props_no_tag(self):
        with self.assertRaises(TypeError) as raised:
            node = TextNode("Am I LINKED?", 42, "the_url")
            html_node = text_node_to_html_node(node)
        self.assertEqual(str(raised.exception), "invalid TextType")

    def test_image(self):
        node = TextNode("Am I AN IMAGE?", TextType.IMG, "the_src")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, '')
        self.assertEqual(html_node.props, {'src': 'the_src', 'alt': 'Am I AN IMAGE?'})
        self.assertEqual(html_node.to_html(), '<img src="the_src" alt="Am I AN IMAGE?">')

if __name__ == "__main__":
    unittest.main()

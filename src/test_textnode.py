#static-sitegen src/text_textnode

import unittest
from textnode import TextType, TextNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq2(self):
        node = TextNode("This is another text node", TextType.PLAIN)
        node2 = TextNode("This is another text node", TextType.PLAIN)
        self.assertEqual(node, node2)

    def test_noteq1(self):
        node = TextNode("link1", TextType.LINK)
        node2 = TextNode("link1", TextType.LINK, 'url')
        self.assertNotEqual(node, node2)

    def test_noteq2(self):
        node = TextNode("link2", TextType.LINK, 'url')
        node2 = TextNode("link2", TextType.IMG, 'url')
        self.assertNotEqual(node, node2)

    def test_noteq3(self):
        node = TextNode("This is a text node", TextType.ITALIC, 'url')
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_eq3(self):
        node = TextNode("This is another text node", TextType.IMG, 'url')
        node2 = TextNode("This is another text node", TextType.IMG, 'url')
        self.assertEqual(node, node2)


if __name__ == "__main__":
    unittest.main()

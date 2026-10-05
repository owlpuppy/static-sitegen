# static-sitegen src/text_htmlnode
#
#  Notes: add more parentnode texts, add exception tests to all 30 09 2026
#
#
#
#
#
#
#

import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    #tag, value, children-> list obj, props -> dict str str
    # htmlnode tests using eq

    def test_with_properties(self):
        node = HTMLNode("z", "aValue", None, {"one": "property", "two": "property"})
        node2 = HTMLNode("z", "aValue", None, {"one": "property", "two": "property"})
        self.assertEqual(node, node2)

    def test_plain(self):
        node = HTMLNode(None, "This is another text node", None, None)
        node2 = HTMLNode(None, "This is another text node", None, None)
        self.assertEqual(node, node2)

    def test_different_tag(self):
        node = HTMLNode("hmmm", None, [HTMLNode(None, "someText"), HTMLNode('a_tag')], None)
        node2 = HTMLNode("hmm", None, [HTMLNode(None, "someText"), HTMLNode('a_tag')], None)
        self.assertNotEqual(node, node2)

    def test_different_children(self):
        node = HTMLNode("hmmm", None, [HTMLNode('h1', 'someText'), HTMLNode(None, 'SomeText')], None)
        node2 = HTMLNode("hmmm", None, [HTMLNode(None, 'someText'), HTMLNode(None, 'SomeText')], None)
        self.assertNotEqual(node, node2)

    def test_different_children_2(self):
        node = HTMLNode("hmmm", None, [HTMLNode(None, 'someText'), HTMLNode(None, 'SomeText')], None)
        node2 = HTMLNode("hmmm", None, [HTMLNode(None, 'someText'), HTMLNode(None, 'someText')], None)
        self.assertNotEqual(node, node2)

    def test_different_tags(self):
        node = HTMLNode("z", "aValue", None, None)
        node2 = HTMLNode("Z", "aValue", None, None)
        self.assertNotEqual(node, node2)

    def test_tag_only(self):
        node = HTMLNode("b")
        node2 = HTMLNode("b")
        self.assertEqual(node, node2)

    # htmlnode tests using repr

    def test_repr_with_properties(self):
        node = repr(HTMLNode("z", "aValue", None, {"one": "property", "two": "property"}))
        text = "HTMLNode(z, aValue, children: None, {'one': 'property', 'two': 'property'}, False)"
        self.assertEqual(node, text)

    def test_repr_with_children(self):
        node = repr(HTMLNode("hmmm", None, [HTMLNode(None, 'someText'), HTMLNode(None, 'SomeText')], None))
        text = "HTMLNode(hmmm, None, children: [HTMLNode(None, someText, children: None, None, False), HTMLNode(None, SomeText, children: None, None, False)], None, False)"
        self.assertEqual(node, text)

    # leafnode tests

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_p_with_props(self):
        node = LeafNode("p", "Hello, world!", {"class": "three", "id": "main"})
        self.assertEqual(node.to_html(), '<p class="three" id="main">Hello, world!</p>')

    def test_leaf_to_html_a_with_props(self):
        node = LeafNode("a", "Google sucks!", {"href": "address", "class": "hated"})
        self.assertEqual(node.to_html(), '<a href="address" class="hated">Google sucks!</a>')

    def test_leaf_to_html_plain(self):
        node = LeafNode(None, "Google Sucks!")
        self.assertEqual(node.to_html(), 'Google Sucks!')

    def test_leaf_to_html_img(self):
        node = LeafNode("img", '', {"src": "address", "alt": "test"}, True)
        self.assertEqual(node.to_html(), '<img src="address" alt="test">')

    #parentnode tests

    def test_parentnode_to_html_nested(self):
        node = ParentNode("p",
            [LeafNode(None, "I have tried to be nice, and I can honestly say: "), ParentNode("b", [LeafNode("i", "Google Sucks!")])],
            {"class": "five", "id": "mean"})
        self.assertEqual(node.to_html(), '<p class="five" id="mean">I have tried to be nice, and I can honestly say: <b><i>Google Sucks!</i></b></p>')

    def test_parentnode_to_html_with_span(self):
        corelist = ParentNode("i", [LeafNode("a", "Google", {"href": "google_address", "target": "_blank"}), LeafNode(None, " sucks!")])
        spanlist = ParentNode("span", [LeafNode(None, "honestly say: "), corelist], {"class": "angry"})
        wrapperlist = ParentNode("p", [LeafNode(None, "I have tried to be nice, and I can "), spanlist], {"class": "one", "id" : "mean"})
        self.assertEqual(wrapperlist.to_html(), '<p class="one" id="mean">I have tried to be nice, and I can <span class="angry">honestly say: <i><a href="google_address" target="_blank">Google</a> sucks!</i></span></p>')

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")


    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_parentnode_to_html_no_tag(self):
        with self.assertRaises(ValueError) as raised:
            node = ParentNode(None, None, None)
            cause_error = node.to_html()
        self.assertEqual(str(raised.exception), "parent nodes must have a tag of type str")

    def test_parentnode_to_html_no_children(self):
        with self.assertRaises(ValueError) as raised:
            node = ParentNode("p", None, None)
            cause_error = node.to_html()
        self.assertEqual(str(raised.exception), "parent nodes must have children")

    def test_parentnode_to_html_wrong_children(self):
        with self.assertRaises(TypeError) as raised:
            node = ParentNode("p", [1, 2, 3], None)
            cause_error = node.to_html()
        self.assertEqual(str(raised.exception), "child must be ParentNode or LeafNode")

    def test_parentnode_to_html_props_no_tag(self):
        with self.assertRaises(TypeError) as raised:
            node = ParentNode("p", [LeafNode(None, "yes")], [1, 2, 3, 4])
            cause_error = node.to_html()
        self.assertEqual(str(raised.exception), "props must be dict")

if __name__ == "__main__":
    unittest.main()

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
from convert_markdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes


class TestConvertMarkdown(unittest.TestCase):

#split nodes delimiter tests

    def test_convert_markdown_long(self):
        node = TextNode("`This is a test`, and `only` a `test`. This is text with a `code block` word. Wow this `might be hard. `", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], TextType.CODE)
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
        new_nodes = split_nodes_delimiter([node], TextType.CODE)
        node2 = [TextNode('block1', TextType.CODE), TextNode('block2', TextType.CODE), TextNode('block3', TextType.CODE)]
        self.assertEqual(new_nodes, node2)

    def test_convert_markdown_italic_mixed(self):
        node = TextNode("block0_block1_block2_block3__block4_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], TextType.ITALIC)
        node2 = [TextNode('block0', TextType.TEXT), TextNode('block1', TextType.ITALIC), TextNode('block2', TextType.TEXT), TextNode('block3', TextType.ITALIC), TextNode('block4', TextType.ITALIC)]
        self.assertEqual(new_nodes, node2)

    def test_convert_markdown_italic_multi(self):
        nodes = [TextNode("block0_block1_", TextType.TEXT), TextNode("block2", TextType.TEXT), TextNode("_block3__block4_", TextType.TEXT)]
        new_nodes = split_nodes_delimiter(nodes, TextType.ITALIC)
        node2 = [TextNode('block0', TextType.TEXT), TextNode('block1', TextType.ITALIC), TextNode('block2', TextType.TEXT),
            TextNode('block3', TextType.ITALIC), TextNode('block4', TextType.ITALIC)]
        self.assertEqual(new_nodes, node2)

    def test_convert_markdown_multi_prev_parsed(self):
        nodes = [TextNode("block0_block1_hmm**hmm**", TextType.TEXT), TextNode("block2", TextType.BOLD), TextNode("_block3__block4`block5`_", TextType.TEXT)]
        new_nodes = split_nodes_delimiter(nodes, TextType.ITALIC)
        node2 = [TextNode('block0', TextType.TEXT), TextNode('block1', TextType.ITALIC), TextNode('hmm**hmm**', TextType.TEXT),
            TextNode('block2', TextType.BOLD), TextNode('block3', TextType.ITALIC), TextNode('block4`block5`', TextType.ITALIC)]
        self.assertEqual(new_nodes, node2)

    def test_convert_to_markdown_typerrror(self):
        with self.assertRaises(TypeError) as raised:
            node = TextNode("**block1****block2block3", TextType.TEXT)
            new_node = split_nodes_delimiter([node], TextType.BOLD)
        self.assertEqual(str(raised.exception), 'syntax error, closing "**" not found')

    def test_convert_to_markdown_typerrror2(self):
        with self.assertRaises(TypeError) as raised:
            node2 = TextNode("**block1****block2block3", TextType.TEXT)
            new_node2 = split_nodes_delimiter([node2], TextType.LINK)
        self.assertEqual(str(raised.exception), 'TextType TextType.LINK not implemented for split_nodes_delimiter')

    # extract images and links tests

    def test_extract_images(self):
        text = []
        text.append("![This is alt text.](http://address.org/image.gif) I wish I didn't have to write so many ![more](path/to/image.jpg) tests. This [link](to-this-address)![shouldn't get picked up](another.png).")
        text.append("I wonder if this will also work. ![This is alt text.](http://address.org/image.gif) I wish I didn't have to write so many ![more](path/to/image.jpg) tests. This [link](to-this-address)![shouldn't get picked up](another.png). Neither Should this.")
        text.append("![This is alt text.](http://address.org/image.gif)![more](path/to/image.jpg)[link](to-this-address)![shouldn't get picked up](another.png)")
        text.append("![This is alt text.](http://address.org/image.gif)![more](path/to/image.jpg)![shouldn't get picked up](another.png)")
        results = []
        for text_string in text:
            results.append(extract_markdown_images(text_string))
        expected = [('This is alt text.', 'http://address.org/image.gif'), ('more', 'path/to/image.jpg'), ("shouldn't get picked up", 'another.png')]
        for result in results:
            self.assertEqual(result, expected)

    def test_extract_links(self):
        text = []
        text.append("[This is alt text.](http://address.org/image.gif) I wish I didn't have to write so many ![more](path/to/image.jpg) tests. This [link](to-this-address)![shouldn't get picked up](another.png).")
        text.append("I wonder if this will also work. [This is alt text.](http://address.org/image.gif) I wish I didn't have to write so many ![more](path/to/image.jpg) tests. This [link](to-this-address)![shouldn't get picked up](another.png). Neither Should this.")
        text.append("[This is alt text.](http://address.org/image.gif)![more](path/to/image.jpg)[link](to-this-address)![shouldn't get picked up](another.png)")
        text.append("[This is alt text.](http://address.org/image.gif)[link](to-this-address)")
        results = []
        for text_string in text:
            results.append(extract_markdown_links(text_string))
        expected = [('This is alt text.', 'http://address.org/image.gif'), ('link', 'to-this-address')]
        for result in results:
                self.assertEqual(result, expected)

    def test_extract_links_and_images_single(self):
        extracted_link = extract_markdown_links("[Test](address)")
        extracted_img = extract_markdown_images("![Test](address)")
        expected = [('Test', 'address')]
        self.assertEqual(extracted_link, extracted_img, expected)

    # split nodes tests

    def test_split_nodes_images(self):
        splitnodes = []
        splitnodes.append(TextNode("![This is alt text.](http://address.org/image.gif) I wish I didn't have to write so many ![more](path/to/image.jpg) tests. This [link](to-this-address)![shouldn't get picked up](another.png).", TextType.TEXT))
        splitnodes.append(TextNode("I wonder if this will also work. ![This is alt text.](http://address.org/image.gif) I wish I didn't have to write so many ![more](path/to/image.jpg) tests. This [link](to-this-address)![shouldn't get picked up](another.png). Neither Should this.", TextType.TEXT))
        splitnodes.append(TextNode("![This is alt text.](http://address.org/image.gif)![more](path/to/image.jpg)[link](to-this-address)![shouldn't get picked up](another.png)", TextType.TEXT))
        splitnodes.append(TextNode("![This is alt text.](http://address.org/image.gif)![more](path/to/image.jpg)![shouldn't get picked up](another.png)", TextType.TEXT))
        splitnodes.append(TextNode("This is a test of a TextNode that needs no processing.", TextType.TEXT))
        results = split_nodes_image(splitnodes)
        expected = [TextNode("This is alt text.", TextType.IMG, "http://address.org/image.gif"),
                    TextNode(" I wish I didn't have to write so many ", TextType.TEXT),
                    TextNode("more", TextType.IMG, "path/to/image.jpg"),
                    TextNode(" tests. This [link](to-this-address)", TextType.TEXT),
                    TextNode("shouldn't get picked up", TextType.IMG, "another.png"),
                    TextNode(".", TextType.TEXT, None),
                    TextNode("I wonder if this will also work. ", TextType.TEXT),
                    TextNode("This is alt text.", TextType.IMG, "http://address.org/image.gif"),
                    TextNode(" I wish I didn't have to write so many ", TextType.TEXT),
                    TextNode("more", TextType.IMG, "path/to/image.jpg"),
                    TextNode(" tests. This [link](to-this-address)", TextType.TEXT),
                    TextNode("shouldn't get picked up", TextType.IMG, "another.png"),
                    TextNode(". Neither Should this.", TextType.TEXT),
                    TextNode("This is alt text.", TextType.IMG, "http://address.org/image.gif"),
                    TextNode("more", TextType.IMG, "path/to/image.jpg"),
                    TextNode("[link](to-this-address)", TextType.TEXT),
                    TextNode("shouldn't get picked up", TextType.IMG, "another.png"),
                    TextNode("This is alt text.", TextType.IMG, "http://address.org/image.gif"),
                    TextNode("more", TextType.IMG, "path/to/image.jpg"),
                    TextNode("shouldn't get picked up", TextType.IMG, "another.png"),
                    TextNode("This is a test of a TextNode that needs no processing.", TextType.TEXT)
        ]
        self.assertEqual(results, expected)

    def test_split_nodes_links(self):
        splitnodes2 = []
        splitnodes2.append(TextNode("[This is alt text.](http://address.org/image.gif) I wish I didn't have to write so many ![more](path/to/image.jpg) tests. This [link](to-this-address)![shouldn't get picked up](another.png).", TextType.TEXT))
        splitnodes2.append(TextNode("I wonder if this will also work. [This is alt text.](http://address.org/image.gif) I wish I didn't have to write so many ![more](path/to/image.jpg) tests. This [link](to-this-address)![shouldn't get picked up](another.png). Neither Should this.", TextType.TEXT))
        splitnodes2.append(TextNode("[This is alt text.](http://address.org/image.gif)![more](path/to/image.jpg)[link](to-this-address)![shouldn't get picked up](another.png)", TextType.TEXT))
        splitnodes2.append(TextNode("[This is alt text.](http://address.org/image.gif)[link](to-this-address)", TextType.TEXT))
        splitnodes2.append(TextNode("This is a test of a TextNode that needs no processing.", TextType.TEXT))
        result2 = split_nodes_link(splitnodes2)
        expecte2 = [TextNode("This is alt text.", TextType.LINK, "http://address.org/image.gif"),
                    TextNode(" I wish I didn't have to write so many ![more](path/to/image.jpg) tests. This ", TextType.TEXT),
                    TextNode("link", TextType.LINK, "to-this-address"),
                    TextNode("![shouldn't get picked up](another.png).", TextType.TEXT),
                    TextNode("I wonder if this will also work. ", TextType.TEXT),
                    TextNode("This is alt text.", TextType.LINK, "http://address.org/image.gif"),
                    TextNode(" I wish I didn't have to write so many ![more](path/to/image.jpg) tests. This ", TextType.TEXT),
                    TextNode("link", TextType.LINK, "to-this-address"),
                    TextNode("![shouldn't get picked up](another.png). Neither Should this.", TextType.TEXT),
                    TextNode("This is alt text.", TextType.LINK, "http://address.org/image.gif"),
                    TextNode("![more](path/to/image.jpg)", TextType.TEXT),
                    TextNode("link", TextType.LINK, "to-this-address"),
                    TextNode("![shouldn't get picked up](another.png)", TextType.TEXT),
                    TextNode("This is alt text.", TextType.LINK, "http://address.org/image.gif"),
                    TextNode("link", TextType.LINK, "to-this-address"),
                    TextNode("This is a test of a TextNode that needs no processing.", TextType.TEXT)
        ]
        self.assertEqual(result2, expecte2)

        # text to textnode tests

    def test_text_to_textnode_example(self):
        ttt_result = text_to_textnodes("This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)")
        ttt_expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMG, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertEqual(ttt_result, ttt_expected)

    def test_text_to_textnode_2(self):
        text_to_input = "This is **a lot** of text that I _really do not want to do_. `I do not like this.` It takes a [really long time](http://example_to_a_long_time.fake) _because_ the design is not ![image of me](address_to_image) **mine!**"
        text_to_input_result = text_to_textnodes(text_to_input)
        expected_result = [
            TextNode("This is ", TextType.TEXT),
            TextNode("a lot", TextType.BOLD),
            TextNode(" of text that I ", TextType.TEXT),
            TextNode("really do not want to do", TextType.ITALIC),
            TextNode(". ", TextType.TEXT),
            TextNode("I do not like this.", TextType.CODE),
            TextNode(" It takes a ", TextType.TEXT),
            TextNode("really long time", TextType.LINK, "http://example_to_a_long_time.fake"),
            TextNode(" ", TextType.TEXT),
            TextNode("because", TextType.ITALIC),
            TextNode(" the design is not ", TextType.TEXT),
            TextNode("image of me", TextType.IMG, "address_to_image"),
            TextNode(" ", TextType.TEXT),
            TextNode("mine!", TextType.BOLD)
        ]
        self.assertEqual(text_to_input_result, expected_result)

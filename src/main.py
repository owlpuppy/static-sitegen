# static-sitegen main

import os

from textnode import TextType, TextNode, text_node_to_html_node
from htmlnode import HTMLNode, ParentNode, LeafNode
from convert_markdown_inline import extract_markdown_images, extract_markdown_links
from convert_markdown_inline import split_nodes_delimiter, split_nodes_image, split_nodes_link, text_to_textnodes
from convert_markdown_block import BlockType, markdown_to_blocks, block_to_block_type, markdown_to_html_node
from file_operations import duplicate_files

def main():

    objects_test = []
    one = TextNode('bold', TextType.BOLD)
    objects_test.append(one)
    two = TextNode('anchor text', TextType.LINK, 'http://fake_address')
    objects_test.append(two)
    three = TextNode('some plain text, like a phrase', TextType.TEXT)
    objects_test.append(three)

    for item in objects_test:
        print(item)

    nodes = [HTMLNode("z", "aValue", None, {"one": "property", "two": "property"}),
        HTMLNode("z", "aValue", None, {"one": "property", "two": "property"})]

    for node in nodes:
        print(node.props_to_html())

    corelist = ParentNode("i", [LeafNode("a", "Google", {"href": "google_address", "target": "_blank"}), LeafNode(None, " sucks!")])
    spanlist = ParentNode("span", [LeafNode(None, "honestly say: "), corelist], {"class": "angry"})
    wrapperlist = ParentNode("p", [LeafNode(None, "I have tried to be nice, and I can "), spanlist], {"class": "one", "id" : "mean"})
    print(wrapperlist.to_html())

    node = TextNode("This is text with a `code block` word", TextType.TEXT)
    new_nodes = split_nodes_delimiter([node], TextType.CODE)
    print(new_nodes)

    text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
    print(f'images: {extract_markdown_images(text)}')

    text2 = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
    print(f'links: {extract_markdown_links(text2)}')

    splitnodes = []
    splitnodes.append(TextNode("![This is alt text.](http://address.org/image.gif) I wish I didn't have to write so many ![more](path/to/image.jpg) tests. This [link](to-this-address)![shouldn't get picked up](another.png).", TextType.TEXT))
    splitnodes.append(TextNode("I wonder if this will also work. ![This is alt text.](http://address.org/image.gif) I wish I didn't have to write so many ![more](path/to/image.jpg) tests. This [link](to-this-address)![shouldn't get picked up](another.png). Neither Should this.", TextType.TEXT))
    splitnodes.append(TextNode("![This is alt text.](http://address.org/image.gif)![more](path/to/image.jpg)[link](to-this-address)![shouldn't get picked up](another.png)", TextType.TEXT))
    splitnodes.append(TextNode("![This is alt text.](http://address.org/image.gif)![more](path/to/image.jpg)![shouldn't get picked up](another.png)", TextType.TEXT))
    result = split_nodes_image(splitnodes)
    for item in result:
        print(f'{item}')

    text_to_textnodes_result = text_to_textnodes("This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)")
    for textnode in text_to_textnodes_result:
        print(textnode)

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
    for block in blocks:
            print(block_to_block_type(block))

    md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

    node = markdown_to_html_node(md)
    html = node.to_html()
    print(f"\nHTML:\n\n{html}")


#    print(os.listdir("static/"))

#    source_files = get_source_files_list()
#    source_files_2 = get_source_files_list2()

#    print(source_files)
#    print(source_files_2)
    duplicate_files()



if __name__ == "__main__":
    main()

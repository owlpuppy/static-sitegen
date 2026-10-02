# static-sitegen main
#
from textnode import TextType, TextNode, text_node_to_html_node
from htmlnode import HTMLNode, ParentNode, LeafNode
from convert_markdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes

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

if __name__ == "__main__":
    main()

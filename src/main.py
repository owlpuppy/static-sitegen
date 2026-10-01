# static-sitegen main
#
from textnode import TextType, TextNode, text_node_to_html_node
from htmlnode import HTMLNode, ParentNode, LeafNode
from convert_markdown import split_nodes_delimiter

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
    new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
    print(new_nodes)

if __name__ == "__main__":
    main()

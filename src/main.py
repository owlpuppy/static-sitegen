# static-sitegen main
#
from textnode import TextType, TextNode
from htmlnode import HTMLNode, ParentNode, LeafNode

def main():

    objects_test = []
    one = TextNode('bold', TextType.BOLD)
    objects_test.append(one)
    two = TextNode('anchor text', TextType.LINK, 'http://fake_address')
    objects_test.append(two)
    three = TextNode('some plain text, like a phrase', TextType.PLAIN)
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

if __name__ == "__main__":
    main()

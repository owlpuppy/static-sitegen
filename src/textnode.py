# static-sitegen src/textnode

from enum import Enum

import common

from htmlnode import HTMLNode, LeafNode, ParentNode

class TextType(Enum):
    TEXT = 'text'
    BOLD = 'bold'
    ITALIC = 'italic'
    CODE = 'code'
    LINK = 'link'
    IMG =  'img'

class TextNode:
    def __init__(self, text: str, text_type: TextType, url: str|None = None) -> None:
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        if isinstance(other, TextNode):
            if (self.text == other.text and
                self.text_type is other.text_type and
                self.url == other.url):

                return True
        return False

    def __repr__(self):
        representation = f'TextNode({self.text}, {self.text_type.value}, {self.url})'
        return representation


def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD: #change to strong
            return LeafNode("b", text_node.text)
        case TextType.ITALIC: #change to em
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMG:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text}, True)
        case _:
            raise TypeError("invalid TextType")

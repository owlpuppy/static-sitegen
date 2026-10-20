# static-sitegen src/textnode

import html
from enum import Enum
from urllib.parse import quote, urlparse, urlunparse

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


def encode_address(address: str) -> str:
    # scheme, netloc, path, params, query, fragment
    # this is simple and imperfect, and is only to assist, not protect
    allowed_schemes = ['http', 'https']
    encoded = []
    placeholder = 'please replace this text with a valid address'
    placeholder_warn = f', replace "{placeholder}" in generated file'

    if not address:
        common.logger.warning(f'url or href attribute missing{placeholder_warn}')
        return placeholder

    parsed = urlparse(address)

    if parsed.username or parsed.password:
        common.logger.warning(f'username or password present in address{placeholder_warn}')
        return placeholder

    if parsed.scheme and parsed.netloc:
        # assume url
        if parsed.scheme.lower() not in allowed_schemes:
            common.logger.warning(f'{allowed_schemes} allowed, {parsed.scheme} given{placeholder_warn}')
            return placeholder

        encoded.append(parsed.scheme) # already checked earlier
        encoded.append(parsed.netloc) # does not encode non-ascii hostnames, cannot be encoded only with % encoding
        encoded.append('/'.join(quote(part, safe='-_.~') for part in parsed.path.split('/'))) # allowed in path A–Z a–z 0–9 - . _ ~ ! $ & ' ( ) * + , ; = : @
        encoded.append(quote(parsed.params, safe='-_.~')) # might be okay
        encoded.append(quote(parsed.query, safe='=&-_.~')) # might be okay
        encoded.append(quote(parsed.fragment, safe='-_.~')) # might be okay
        return urlunparse(encoded)
    else:
        # not a full url
        return quote(address, safe="/:?&=")


def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, html.escape(text_node.text))
        case TextType.BOLD: #change to strong
            return LeafNode("strong", html.escape(text_node.text))
        case TextType.ITALIC: #change to em
            return LeafNode("em", html.escape(text_node.text))
        case TextType.CODE:
            return LeafNode("code", text_node.text) # code, not escaped
        case TextType.LINK:
            return LeafNode("a", html.escape(text_node.text), {"href": encode_address(text_node.url)})
        case TextType.IMG:
            return LeafNode("img", "", {"src": encode_address(text_node.url), "alt": html.escape(text_node.text)}, True)
        case _:
            raise TypeError("invalid TextType")

# static-sitegen src/textnode

from enum import Enum

class TextType(Enum):
    PLAIN = 'inline_txt'
    BOLD = 'inline_bold'
    ITALIC = 'inline_italic'
    CODE = 'inline_code'
    LINK = 'inline_link'
    IMG =  'inline_img'

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
        if self.url is not None and self.text_type is not (TextType.LINK or TextType.url):
            representation = representation + 'Error: url present\n'
        elif self.url is None and self.text_type is (TextType.LINK or TextType.url):
            representation = representation + 'Error: url missing\n'
        return representation

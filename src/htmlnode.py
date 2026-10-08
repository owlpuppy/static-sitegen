# static-sitegen src/htmlnode

from typing import override

import common

class HTMLNode:
    def __init__(self, tag: str|None = None,
        value: str|None = None,
        children: list[HTMLNode]|None = None,
        props: dict[str, str]|None = None,
        no_close: bool = False) -> None:

        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
        self.no_close = no_close

    def to_html(self):
        # should raise a not implemented errror if not overridden
        raise NotImplementedError("to_html method not implemented")

    def props_to_html(self):
        formatted = ''

        if self.props is None or not self.props:
            return formatted

        for prop in self.props:
            formatted = formatted + f' {prop}="{self.props[prop]}"'

        return formatted

    def close_tag_to_html(self):
        if self.no_close == True:
            return ''
        else:
            return f'</{self.tag}>'

    def __eq__(self, other):
        if isinstance(other, HTMLNode):
            if (self.tag == other.tag and
                self.value == other.value and
                self.children == other.children and
                self.props == other.props):

                return True
        return False

    def __repr__(self):
        return f'HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props}, {self.no_close})'

class LeafNode(HTMLNode):
    def __init__(self, tag: str|None,
        value: str,
        props: dict[str, str]|None = None,
        no_close: bool = False) -> None:

        super().__init__(tag, value, None, props, no_close)

    @override
    def to_html(self):
        if self.value is None or not isinstance(self.value, str):
            raise ValueError("leaf nodes must have a value of type str")

        if self.props is not None and self.tag is None:
            raise ValueError("tag required if props exist")

        if self.props is not None and not isinstance(self.props, dict):
            raise ValueError("props must be dict")

        if self.tag is None:
            return self.value
        else:
            props = self.props_to_html()
            end_html = self.close_tag_to_html()
            return f'<{self.tag}{props}>{self.value}{end_html}'

    @override
    def __repr__(self):
        return f'LeafNode(HTMLNode)({self.tag}, {self.value}, {self.props}, {self.no_close})'

class ParentNode(HTMLNode):
    def __init__(self, tag: str,
        children: list[HTMLNode],
        props: dict[str, str]|None = None) -> None:

        super().__init__(tag, None, children, props)

    @ override
    def to_html(self):
        if self.tag is None or not isinstance(self.tag, str):
            raise ValueError("parent nodes must have a tag of type str")

        if self.children is None or not isinstance(self.children, list):
            raise ValueError("parent nodes must have children")

        if self.props is not None and not isinstance(self.props, dict):
            raise TypeError("props must be dict")

        props = self.props_to_html()
        start_html = f'<{self.tag}{props}>'
        end_html = self.close_tag_to_html()
        child_html = ''

        # recursive
        # all child nodes should be ParentNode or LeafNode
        for child in self.children:
            if isinstance(child, ParentNode) or isinstance(child, LeafNode):
                child_html = child_html + child.to_html()
            else:
                raise TypeError("child must be ParentNode or LeafNode")

        return start_html + child_html + end_html

    @override
    def __repr__(self):
        return f'ParentNode(HTMLNode)({self.tag}, children: {self.children}, {self.props}, {self.no_close})'
